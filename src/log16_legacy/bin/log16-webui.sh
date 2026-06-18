#!/usr/bin/env bash
set -Eeuo pipefail
PORT="${LOG16_WEBUI_PORT:-8896}"
exec python3 /data/wellbeing/obs/log16/bin/log16-webui.py --host 127.0.0.1 --port "$PORT"
