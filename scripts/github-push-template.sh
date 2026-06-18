#!/usr/bin/env bash
# TEMPLATE ONLY.
# This script refuses to run unless explicit env flags are set.
# It is intentionally hostile to accidental publishing.

set -Eeuo pipefail

if [ "${LOG16_CONFIRM_GITHUB_PUSH:-}" != "YES_I_REALLY_MEAN_IT" ]; then
  echo "REFUSING: set LOG16_CONFIRM_GITHUB_PUSH=YES_I_REALLY_MEAN_IT to continue." >&2
  exit 20
fi

if [ -z "${LOG16_GITHUB_REMOTE_URL:-}" ]; then
  echo "REFUSING: set LOG16_GITHUB_REMOTE_URL." >&2
  exit 21
fi

REPO="/data/wellbeing/repos/wellbeing-log16"
cd "$REPO"

scripts/github-prepublish-check.sh

if git remote get-url origin >/dev/null 2>&1; then
  echo "origin already exists:"
  git remote -v
else
  git remote add origin "$LOG16_GITHUB_REMOTE_URL"
fi

git remote -v
git push -u origin master
git push origin --tags
