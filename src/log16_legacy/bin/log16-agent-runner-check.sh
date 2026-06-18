#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="/data/wellbeing/obs/log16"

echo "LOG16 AGENT RUNNER CHECK"
echo "root: $ROOT"
echo "python: $(command -v python3 || true)"

for f in \
  "$ROOT/bin/log16-agent-runner.py" \
  "$ROOT/bin/log16-create-participant-pathway-requests.py" \
  "$ROOT/bin/log16-runner-participant-pathway.sh" \
  "$ROOT/entity-registry/entity-registry.json"
do
  if [ -e "$f" ]; then
    echo "exists: $f"
  else
    echo "missing: $f"
  fi
done

python3 -m py_compile "$ROOT/bin/log16-agent-runner.py"
python3 -m py_compile "$ROOT/bin/log16-create-participant-pathway-requests.py"
echo "py_compile: OK"

echo
echo "ollama tags:"
if command -v curl >/dev/null 2>&1; then
  curl -s http://127.0.0.1:11434/api/tags | head -c 1000 || true
  echo
else
  python3 - <<'PY'
import urllib.request
try:
    print(urllib.request.urlopen("http://127.0.0.1:11434/api/tags", timeout=5).read().decode()[:1000])
except Exception as e:
    print("ollama check failed:", e)
PY
fi
