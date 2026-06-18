#!/usr/bin/env bash
set -Eeuo pipefail
exec /data/wellbeing/obs/log16/bin/log16-agent-runner.py --case topic_to_task_system "$@"
