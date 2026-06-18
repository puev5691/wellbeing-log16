#!/usr/bin/env bash
set -Eeuo pipefail

echo "LOG16 WEB UI CHECK"
echo "python: $(command -v python3 || true)"
python3 - <<'PY'
import http.server
import urllib.parse
import html
print("stdlib http/html/urllib: OK")
PY

for f in \
  /data/wellbeing/obs/log16/bin/log16-webui.py \
  /data/wellbeing/obs/log16/bin/log16-webui.sh \
  /data/wellbeing/obs/log16/bin/log16-webui-open.sh \
  /data/wellbeing/obs/log16/bin/log16-ask-import-v05-2.sh \
  /data/wellbeing/obs/log16/bin/log16-case-summary.sh
do
  if [ -e "$f" ]; then
    echo "exists: $f"
  else
    echo "missing: $f"
  fi
done

python3 -m py_compile /data/wellbeing/obs/log16/bin/log16-webui.py
echo "py_compile: OK"
