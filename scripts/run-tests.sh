#!/usr/bin/env bash
set -Eeuo pipefail

REPO="/data/wellbeing/repos/wellbeing-log16"
cd "$REPO"

PYTHONPATH="$REPO/src" python3 -m unittest discover -s tests -v
