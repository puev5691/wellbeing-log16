#!/usr/bin/env bash
set -Eeuo pipefail

RUNS_DIR="/data/wellbeing/obs/consultant/outbox/consultant-pipeline-v05.2-runs"
IMPORTER="/data/wellbeing/obs/log16/bin/log16-import-v05-run.sh"

latest="$(ls -t "$RUNS_DIR"/CONS__consultant-pipeline-v05.2-run-*__OPR.tgz 2>/dev/null | head -n 1 || true)"

if [ -z "$latest" ]; then
  echo "ERROR: no v05.2 run archive found in $RUNS_DIR" >&2
  exit 20
fi

echo "LOG16 IMPORT LATEST"
echo "run: $latest"
echo

"$IMPORTER" "$latest"

echo
echo "friendly status:"
/data/wellbeing/obs/log16/bin/log16-status.sh
