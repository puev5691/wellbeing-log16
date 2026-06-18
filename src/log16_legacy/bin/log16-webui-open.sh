#!/usr/bin/env bash
set -Eeuo pipefail
PORT="${LOG16_WEBUI_PORT:-8896}"
URL="http://127.0.0.1:${PORT}/"

if command -v xdg-open >/dev/null 2>&1; then
  xdg-open "$URL" >/dev/null 2>&1 &
fi

echo "$URL"
