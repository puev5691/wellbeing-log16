#!/usr/bin/env bash
set -Eeuo pipefail

echo "STEP 1: creating participant_pathway entity requests"
/data/wellbeing/obs/log16/bin/log16-create-participant-pathway-requests.py

echo
echo "STEP 2: running local agent runner"
/data/wellbeing/obs/log16/bin/log16-agent-runner.py --case participant_pathway
