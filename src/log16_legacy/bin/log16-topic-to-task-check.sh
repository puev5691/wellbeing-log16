#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="/data/wellbeing/obs/log16"

echo "LOG16 TOPIC-TO-TASK CORE CHECK"
echo "root: $ROOT"
echo "python: $(command -v python3 || true)"

for f in \
  "$ROOT/bin/log16-topic-to-task-core.py" \
  "$ROOT/bin/log16-topic-to-task.sh" \
  "$ROOT/bin/log16-topic-to-task-demo.sh" \
  "$ROOT/schemas/theme-card.schema.json" \
  "$ROOT/schemas/derived-task-card.schema.json" \
  "$ROOT/schemas/task-batch.schema.json"
do
  if [ -e "$f" ]; then
    echo "exists: $f"
  else
    echo "missing: $f"
  fi
done

python3 -m py_compile "$ROOT/bin/log16-topic-to-task-core.py"
echo "py_compile: OK"
