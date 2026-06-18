#!/usr/bin/env bash
set -Eeuo pipefail

echo "LOG16 GUI CHECK"
echo "python: $(command -v python3 || true)"
python3 - <<'PY'
try:
    import tkinter
    print("tkinter: OK")
except Exception as e:
    print("tkinter: FAIL")
    print(e)
    raise SystemExit(2)
PY

for f in \
  /data/wellbeing/obs/log16/bin/log16-gui.py \
  /data/wellbeing/obs/log16/bin/log16-gui.sh \
  /data/wellbeing/obs/log16/bin/log16-ask-import-v05-2.sh \
  /data/wellbeing/obs/log16/bin/log16-case-summary.sh
do
  if [ -e "$f" ]; then
    echo "exists: $f"
  else
    echo "missing: $f"
  fi
done
