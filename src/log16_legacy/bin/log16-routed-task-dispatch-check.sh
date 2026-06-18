#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="/data/wellbeing/obs/log16"

echo "LOG16 ROUTED TASK DISPATCH CHECK"
echo "root: $ROOT"
echo "python: $(command -v python3 || true)"

for f in \
  "$ROOT/bin/log16-extend-entity-registry-v01.py" \
  "$ROOT/bin/log16-dispatch-routed-tasks.py" \
  "$ROOT/bin/log16-dispatch-routed-tasks.sh"
do
  if [ -e "$f" ]; then
    echo "exists: $f"
  else
    echo "missing: $f"
  fi
done

python3 -m py_compile "$ROOT/bin/log16-extend-entity-registry-v01.py"
python3 -m py_compile "$ROOT/bin/log16-dispatch-routed-tasks.py"
echo "py_compile: OK"

echo "routed tasks:"
find "$ROOT/derived-tasks/routed" -maxdepth 1 -type f -name '*.json' 2>/dev/null | wc -l

echo "pending entity requests:"
find "$ROOT/entity-requests/pending" -maxdepth 1 -type f -name '*.json' 2>/dev/null | wc -l
