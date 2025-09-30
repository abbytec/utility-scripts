#!/usr/bin/env bash
set -euo pipefail

LOG="$HOME/communication-watch.log"
INTERVAL="0.5"   # segundos

echo "=== $(date) :: start ===" | tee -a "$LOG"

get_comm_nodes() {
  # Lista: "<id>\t<app>"
  pw-dump | jq -r '
    .[] 
    | select(.type=="PipeWire:Interface:Node")
    | select(.info.props["media.role"]=="communication")
    | "\(.id)\t\(.info.props["application.name"] // .info.props["node.name"] // "unknown")"
  ' | sort -n
}

prev="$(mktemp)"
curr="$(mktemp)"
trap 'rm -f "$prev" "$curr"' EXIT

get_comm_nodes > "$prev"

while true; do
  get_comm_nodes > "$curr"

  # Nuevos
  comm_added=$(comm -13 "$prev" "$curr" || true)
  # Removidos
  comm_removed=$(comm -23 "$prev" "$curr" || true)

  ts="$(date '+%F %T')"

  if [[ -n "$comm_added" ]]; then
    while IFS=$'\t' read -r id app; do
      [[ -z "${id:-}" ]] && continue
      msg="Communication stream INICIADO (id=$id, app=$app)"
      echo "[$ts] + $msg" | tee -a "$LOG"
      notify-send "Audio: comunicación detectada" "$msg"
    done <<< "$comm_added"
  fi

  if [[ -n "$comm_removed" ]]; then
    while IFS=$'\t' read -r id app; do
      [[ -z "${id:-}" ]] && continue
      msg="Communication stream FINALIZADO (id=$id, app=$app)"
      echo "[$ts] - $msg" | tee -a "$LOG"
      notify-send "Audio: comunicación finalizada" "$msg"
    done <<< "$comm_removed"
  fi

  cp "$curr" "$prev"
  sleep "$INTERVAL"
done

