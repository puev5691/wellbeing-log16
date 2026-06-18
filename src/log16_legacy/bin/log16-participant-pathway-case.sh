#!/usr/bin/env bash
set -Eeuo pipefail
exec /data/wellbeing/obs/log16/bin/log16-case-summary.py --pattern participant_pathway "$@"
