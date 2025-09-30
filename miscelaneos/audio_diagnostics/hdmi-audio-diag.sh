#!/usr/bin/env bash
set -euo pipefail

LOG="$HOME/hdmi-audio-diag.log"
INTERVAL_VOL=0.25      # seg
INTERVAL_STREAM=1      # seg
DIP_TH=0.05            # 5% de cambio
HEARTBEAT=5            # meta HDMI cada N seg (subílo si querés menos log)

need(){ command -v "$1" >/dev/null || { echo "Falta $1"; exit 1; }; }
need jq; need pw-dump; need wpctl; need dmesg

echo "=== $(date) :: HDMI Audio Diagnostic START (v3) ===" | tee -a "$LOG"

DEFAULT_SINK="@DEFAULT_AUDIO_SINK@"
HDMI_SINK_ID="$(wpctl status | sed -n '/Audio/,/Video/p' | awk '/HDMI|hdmi/ {print $1; exit}' | tr -d '.' || true)"
[[ -z "${HDMI_SINK_ID:-}" ]] && echo "[WARN] No se encontró sink HDMI" | tee -a "$LOG"

dump_hdmi_node_meta() {
  [[ -z "${HDMI_SINK_ID:-}" ]] && return 0
  pw-dump | jq -r --arg id "$HDMI_SINK_ID" '
    .[] | select(.type=="PipeWire:Interface:Node")
    | select((.id|tostring)==$id)
    | {id, name:.info.props["node.name"], desc:.info.props["node.description"],
       media_class:.info.props["media.class"],
       suspend:.info.props["session.suspend-timeout-seconds"],
       suspend_quiet:.info.props["session.suspend-timeout-seconds.quiet"],
       device:.info.props["device.name"], api:.info.props["api.alsa.path"]}
  '
}

get_vol(){ wpctl get-volume "$DEFAULT_SINK" 2>/dev/null | awk '{print $2}' | tr -cd '0-9.'; }

echo "[SNAPSHOT] Audio:" | tee -a "$LOG"
wpctl status | sed -n '/Audio/,/Video/p' | tee -a "$LOG"
echo "[SNAPSHOT] flat-volumes:" | tee -a "$LOG"
grep -R "flat-volumes" "$HOME/.config/pipewire/pipewire-pulse.conf.d"/* 2>/dev/null || echo "  (sin override)" | tee -a "$LOG"
[[ -n "${HDMI_SINK_ID:-}" ]] && { echo "[SNAPSHOT] HDMI node meta:" | tee -a "$LOG"; dump_hdmi_node_meta | tee -a "$LOG"; }

PIDS=()

# --- dmesg watcher (ELD/HDMI/NVIDIA)
stdbuf -oL dmesg -w | grep -i -E 'hdmi|eld|hda|audio|nvidia|snd_hda_intel' >> "$LOG" &
PIDS+=($!)

# --- streams watcher
(
  prev="/dev/null"
  while sleep "$INTERVAL_STREAM"; do
    out="$(pw-dump | jq -r '
      .[] | select(.type=="PipeWire:Interface:Node")
      | select(.info.props["media.class"]=="Stream/Output/Audio")
      | "\(.id)\t\(.info.props["application.name"] // .info.props["node.name"] // "unknown")\t\(.info.props["media.role"] // "-")\t\(.info.props["media.category"] // "-")"
    ' | sort -n)"
    tmp="$(mktemp)"; printf "%s\n" "$out" > "$tmp"
    added="$(comm -13 "${prev:-/dev/null}" "$tmp" 2>/dev/null || true)"
    removed="$(comm -23 "${prev:-/dev/null}" "$tmp" 2>/dev/null || true)"
    ts="$(date '+%F %T')"
    [[ -n "$added" ]] && while IFS=$'\t' read -r id app role cat; do
      [[ -z "${id:-}" ]] && continue
      echo "[$ts] STREAM+ OUT id=$id app=$app role=$role cat=$cat" | tee -a "$LOG"
    done <<< "$added"
    [[ -n "$removed" ]] && while IFS=$'\t' read -r id app role cat; do
      [[ -z "${id:-}" ]] && continue
      echo "[$ts] STREAM- OUT id=$id app=$app role=$role cat=$cat" | tee -a "$LOG"
    done <<< "$removed"
    [[ -f "$prev" ]] && rm -f "$prev"; prev="$tmp"
  done
) &
PIDS+=($!)

# --- loop principal: dips + heartbeat
last="$(get_vol)"; [[ -z "$last" ]] && last=0
echo "[INIT] sink volume=$last" | tee -a "$LOG"

t0=$(date +%s)
while true; do
  sleep "$INTERVAL_VOL"
  vol="$(get_vol)"; [[ -z "$vol" ]] && vol="$last"
  diff=$(awk -v a="$last" -v b="$vol" 'BEGIN{print b-a}')
  absdiff=$(awk -v d="$diff" 'BEGIN{print (d<0)?-d:d}')
  if awk -v x="$absdiff" -v th="$DIP_TH" 'BEGIN{exit (x>th)?0:1}'; then
    ts="$(date '+%F %T')"
    echo "[$ts] VOL change: $last -> $vol (Δ=$(printf "%.3f" "$absdiff"))" | tee -a "$LOG"
    echo "[$ts] Streams OUT activos:" | tee -a "$LOG"
    pw-dump | jq -r '
      .[] | select(.type=="PipeWire:Interface:Node")
      | select(.info.props["media.class"]=="Stream/Output/Audio"])
      | "  id=\(.id) app=\(.info.props["application.name"] // .info.props["node.name"] // "unknown") role=\(.info.props["media.role"] // "-") cat=\(.info.props["media.category"] // "-")"
    ' 2>/dev/null | tee -a "$LOG"
    [[ -n "${HDMI_SINK_ID:-}" ]] && { echo "[$ts] HDMI node meta:" | tee -a "$LOG"; dump_hdmi_node_meta | tee -a "$LOG"; }
  fi
  last="$vol"

  now=$(date +%s)
  if (( now - t0 >= HEARTBEAT )); then
    ts="$(date '+%F %T')"
    echo "[$ts] HDMI meta heartbeat:" | tee -a "$LOG"
    [[ -n "${HDMI_SINK_ID:-}" ]] && dump_hdmi_node_meta | tee -a "$LOG"
    t0=$now
  fi
done &

PIDS+=($!)

# --- parada limpia con Ctrl+C (una sola vez)
stop() {
  echo "=== $(date) :: STOP ===" | tee -a "$LOG"
  for pid in "${PIDS[@]}"; do kill "$pid" 2>/dev/null || true; done
  wait 2>/dev/null || true
  exit 0
}
trap stop INT TERM EXIT

wait

