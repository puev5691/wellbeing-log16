#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="/data/wellbeing/obs/log16"
need_dirs=(schemas answers/draft answers/needs_review answers/approved answers/deprecated gaps/detected gaps/routed gaps/resolved tasks/proposed tasks/routed tasks/done reviews reports indexes bin)
for d in "${need_dirs[@]}"; do
  [ -d "$ROOT/$d" ] || { echo "FAIL missing dir: $ROOT/$d"; exit 1; }
done
need_files=(schemas/answer-card.schema.json schemas/approved-answer-card.schema.json schemas/gap-card.schema.json schemas/task-card.schema.json schemas/review-card.schema.json README.md)
for f in "${need_files[@]}"; do
  [ -f "$ROOT/$f" ] || { echo "FAIL missing file: $ROOT/$f"; exit 1; }
done
echo "PASS log16 kernel smoke test"
echo "ROOT: $ROOT"
