#!/usr/bin/env bash
set -Eeuo pipefail

REPO="/data/wellbeing/repos/wellbeing-log16"
cd "$REPO"

echo "Checking suspicious runtime paths..."
find . \( -path './runtime' -o -path './var' -o -path './entity-responses' -o -path './entity-requests' -o -path './dashboard-runs' -o -path './runner-reports' \) -print

echo
echo "Checking archives/logs/secrets..."
find . \( -name '*.tgz' -o -name '*.tar.gz' -o -name '*.log' -o -name '.env' -o -iname '*secret*' -o -iname '*token*' -o -iname '*key*' \) -print

echo
echo "Done."
