#!/usr/bin/env bash
set -Eeuo pipefail

REPO="/data/wellbeing/repos/wellbeing-log16"
PATTERN="/data/wellbeing/obs/consultant/outbox/log16-kernel"

cd "$REPO"
echo "# Hardcoded path audit"
echo
echo "Pattern:"
echo "$PATTERN"
echo
echo "Matches:"
grep -RIn --exclude-dir=.git --exclude='*.tgz' --exclude='*.tar.gz' "$PATTERN" . || true
