#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="/data/wellbeing/obs/log16"
echo "LOG16 PULT V02 CHECK"
python3 -m py_compile "$ROOT/bin/log16-pult.py"
echo "py_compile: OK"
"$ROOT/bin/log16-pult" status --cleanup
