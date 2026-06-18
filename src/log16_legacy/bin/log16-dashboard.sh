#!/usr/bin/env bash
set -Eeuo pipefail
export PYTHONPATH="/data/wellbeing/repos/wellbeing-log16/src:${PYTHONPATH:-}"
exec /data/wellbeing/obs/log16/bin/log16-dashboard.py
