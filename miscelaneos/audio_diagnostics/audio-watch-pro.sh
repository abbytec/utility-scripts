#!/usr/bin/env bash
set -euo pipefail

LOG="$HOME/audio-watch-pro.log"
INTERVAL="0.25"      # segundos
DIP_THRESHOLD=0.05   # 5%

echo "=== $(date) :: start ===" | tee -a "$LOG"

get_sink_vol() {
  wpctl get-volume @DEFAULT_AUDIO_SINK@ 2>/dev/null | awk '{print $2}' | sed 's/[^0-9.]//g'
}

list_output_nodes() {
  # id, app, role, category
  pw-dump | jq -r '
    .[] 
    | select(.type=="PipeWire:Interface:Node")
    | select(.info.props["media.class"]=="Stream/Output/Audio")
    | "\(.id)\t\(.info.props["application.name"] // .info.props["node.name"] // "unknown")\t\(.info.props["media.role"] // "-")\t\(.info.props["media.category"] // "-")"
  ' | sort -n
}

prev_nodes="$(mktemp)"
curr_nodes="$(mktemp)"
trap 'rm -f "$prev_nodes" "$curr_nodes"' EXIT

list_output_nodes > "$prev_nodes"

last_vol="$(get_sink_vol)"
[[ -z "${last_vol}" ]] && last_vol=0

notify() { command -v notify-send >/dev/null && notify-send "$1" "$2" || true; }

echo "[INIT] sink volume=$last_vol" | tee -a "$LOG"

while true; do
  # 1) Track nuevos/removidos streams de salida
  list_output_nodes > "$curr_nodes"
  added=$(comm -13 "$prev_nodes" "$curr_nodes" || true)
  removed=$(comm -23 "$prev_nodes" "$curr_nodes" || true)

  ts="$(date '+%F %T')"

  if [[ -n "$added" ]]; then
    while IFS=$'\t' read -r id app role cat; do
      [[ -z "${id:-}" ]] && continue
      msg="Nuevo stream OUT id=$id app=$app role=$role cat=$cat"
      echo "[$ts] + $msg" | tee -a "$LOG"
      notify "Audio" "$msg"
    done <<< "$added"
  fi
  if [[ -n "$removed" ]]; then
    while IFS=$'\t' read -r id app role cat; do
      [[ -z "${id:-}" ]] && continue
      msg="Stream OUT removido id=$id app=$app role=$role cat=$cat"
      echo "[$ts] - $msg" | tee -a "$LOG"
      notify "Audio" "$msg"
    done <<< "$removed"
  fi
  cp "$curr_nodes" "$prev_nodes"

  # 2) Detectar dips bruscos del sink
  vol="$(get_sink_vol)"
  if [[ -n "$vol" ]]; then
    # si cambia más de 5% respecto al último muestreo, loggear
    diff=$(awk -v a="$last_vol" -v b="$vol" 'BEGIN{print b-a}')
    absdiff=$(awk -v d="$diff" 'BEGIN{print (d<0)?-d:d}')
    if awk -v x="$absdiff" -v th="$DIP_THRESHOLD" 'BEGIN{exit (x>th)?0:1}'; then
      echo "[$ts] VOL change: $last_vol -> $vol (Δ=$(printf "%.3f" "$absdiff"))" | tee -a "$LOG"
      # Dump rápido de streams actuales
      echo "[$ts] Streams OUT activos:" | tee -a "$LOG"
      list_output_nodes | sed 's/^/  /' | tee -a "$LOG"
      notify "Audio" "Cambio de volumen detectado: $(printf "%.0f" "$(awk -v v="$vol" 'BEGIN{print v*100}')")%"
    fi
    last_vol="$vol"
  fi

  sleep "$INTERVAL"
done

