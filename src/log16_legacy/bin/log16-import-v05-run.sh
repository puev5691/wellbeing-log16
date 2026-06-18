#!/usr/bin/env bash
set -Eeuo pipefail
if [ $# -lt 1 ]; then
  echo "Usage: log16-import-v05-run.sh /path/to/CONS__consultant-pipeline-v05.2-run-....tgz" >&2
  exit 2
fi
python3 /data/wellbeing/obs/log16/bin/log16-import-v05-run.py "$1"
