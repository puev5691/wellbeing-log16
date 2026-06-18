#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="/data/wellbeing/obs/log16"
echo "LOG16 DASHBOARD V03 CHECK"
python3 -m py_compile "$ROOT/bin/log16-dashboard.py"
echo "py_compile: OK"
echo "IMPORTANT:"
echo "  If old dashboard is running, stop it with Ctrl+C and restart."
echo "Run:"
echo "  $ROOT/bin/log16-dashboard.sh"
echo "Open:"
echo "  http://127.0.0.1:8898/"
echo "Review page:"
echo "  http://127.0.0.1:8898/review"
