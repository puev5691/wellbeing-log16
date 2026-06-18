#!/usr/bin/env bash
set -Eeuo pipefail
URL="http://127.0.0.1:8898/"
if command -v xdg-open >/dev/null 2>&1; then
  xdg-open "$URL" >/dev/null 2>&1 || true
fi
echo "$URL"
