#!/usr/bin/env bash
# Guarded GitHub publisher for wellbeing-log16.
# This script performs real external actions ONLY after explicit environment confirmation.

set -Eeuo pipefail

REPO="/data/wellbeing/repos/wellbeing-log16"
cd "$REPO"

if [ "${LOG16_CONFIRM_GITHUB_PUBLISH:-}" != "YES_I_REALLY_MEAN_IT" ]; then
  echo "REFUSING: set LOG16_CONFIRM_GITHUB_PUBLISH=YES_I_REALLY_MEAN_IT to publish." >&2
  exit 20
fi

OWNER="${LOG16_GITHUB_OWNER:-}"
NAME="${LOG16_GITHUB_REPO:-wellbeing-log16}"
VISIBILITY="${LOG16_GITHUB_VISIBILITY:-private}"

if [ -z "$OWNER" ]; then
  echo "REFUSING: set LOG16_GITHUB_OWNER, for example puev5691." >&2
  exit 21
fi

case "$VISIBILITY" in
  private|public) ;;
  *)
    echo "REFUSING: LOG16_GITHUB_VISIBILITY must be private or public." >&2
    exit 22
    ;;
esac

if ! command -v gh >/dev/null 2>&1; then
  echo "REFUSING: gh CLI not found." >&2
  exit 23
fi

scripts/github-prepublish-check.sh

if [ -n "$(git status --short)" ]; then
  echo "REFUSING: git status is not clean after prepublish-check." >&2
  git status --short >&2
  exit 24
fi

REMOTE_URL="https://github.com/${OWNER}/${NAME}.git"

echo "Publishing target:"
echo "  owner: $OWNER"
echo "  repo:  $NAME"
echo "  visibility: $VISIBILITY"
echo "  remote: $REMOTE_URL"
echo

if gh repo view "${OWNER}/${NAME}" >/dev/null 2>&1; then
  echo "GitHub repo already exists: ${OWNER}/${NAME}"
else
  if [ "$VISIBILITY" = "private" ]; then
    gh repo create "${OWNER}/${NAME}" --private
  else
    gh repo create "${OWNER}/${NAME}" --public
  fi
fi

if git remote get-url origin >/dev/null 2>&1; then
  CURRENT_ORIGIN="$(git remote get-url origin)"
  if [ "$CURRENT_ORIGIN" != "$REMOTE_URL" ]; then
    echo "REFUSING: origin exists and differs:"
    echo "  current: $CURRENT_ORIGIN"
    echo "  target:  $REMOTE_URL"
    exit 25
  fi
else
  git remote add origin "$REMOTE_URL"
fi

git remote -v

git push -u origin master
git push origin --tags

echo
echo "PUBLISH_DONE"
