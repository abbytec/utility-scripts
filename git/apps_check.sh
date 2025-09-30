#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

usage() {
  echo "Uso: $0 <url_pr_github> [--apps-root apps] [--json]"
  exit 2
}

[[ $# -lt 1 ]] && usage

PR_URL="$1"; shift || true
APPS_ROOT="apps"
AS_JSON="0"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --apps-root)
      shift
      [[ $# -eq 0 ]] && { echo "Falta valor para --apps-root" >&2; exit 1; }
      APPS_ROOT="${1#/}"; APPS_ROOT="${APPS_ROOT%/}"
      ;;
    --json) AS_JSON="1" ;;
    -h|--help) usage ;;
    *) echo "Argumento desconocido: $1" >&2; usage ;;
  esac
  shift || true
done

if ! command -v gh >/dev/null 2>&1; then
  echo "Necesito GitHub CLI (gh). Instalá: https://cli.github.com/" >&2
  exit 1
fi

if ! gh auth status >/dev/null 2>&1; then
  echo "No hay sesión autenticada en gh. Ejecutá: gh auth login" >&2
  exit 1
fi

if ! [[ "$PR_URL" =~ ^https?://github\.com/[^/]+/[^/]+/pull/[0-9]+ ]]; then
  echo "URL no reconocida como PR de GitHub (esperado: https://github.com/<owner>/<repo>/pull/<n>)" >&2
  exit 1
fi

# Obtiene paths cambiados del PR y extrae subcarpetas directas bajo /$APPS_ROOT
readarray -t SUBS < <(
  gh pr view "$PR_URL" --json files --jq '.files[].path' \
  | awk -v root="$APPS_ROOT" 'index($0, root"/")==1 { n=split($0,a,"/"); if (n>=2) print a[2] }' \
  | awk 'NF' \
  | sort -u
)

if [[ "$AS_JSON" == "1" ]]; then
  # Salida JSON simple sin depender de jq
  printf '{\"apps_root\":\"%s\",\"affected_apps\":[' "$APPS_ROOT"
  for i in "${!SUBS[@]}"; do
    s="${SUBS[$i]//\"/\\\"}"
    if [[ $i -gt 0 ]]; then printf ','; fi
    printf '\"%s\"' "$s"
  done
  printf ']}\n'
else
  if [[ ${#SUBS[@]} -eq 0 ]]; then
    echo "(sin subcarpetas afectadas bajo /$APPS_ROOT)"
  else
    printf "%s\n" "${SUBS[@]}"
  fi
fi

