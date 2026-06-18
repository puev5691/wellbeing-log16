#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="/data/wellbeing/obs/log16"

echo "LOG16 TOPIC TASK TRIAGE CHECK"
echo "root: $ROOT"
echo "python: $(command -v python3 || true)"

for f in \
  "$ROOT/bin/log16-topic-task-triage.py" \
  "$ROOT/bin/log16-topic-task-triage.sh"
do
  if [ -e "$f" ]; then
    echo "exists: $f"
  else
    echo "missing: $f"
  fi
done

python3 -m py_compile "$ROOT/bin/log16-topic-task-triage.py"
echo "py_compile: OK"

echo "proposed tasks:"
find "$ROOT/derived-tasks/proposed" -maxdepth 1 -type f -name '*.json' 2>/dev/null | wc -l
