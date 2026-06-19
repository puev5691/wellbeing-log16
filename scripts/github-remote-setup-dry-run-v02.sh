#!/usr/bin/env bash
set -Eeuo pipefail

REPO="/data/wellbeing/repos/wellbeing-log16"
RUNTIME="/data/wellbeing/obs/log16"
REMOTE_URL="git@github.com:puev5691/wellbeing-log16.git"
EXPECTED_REPO_NAME="wellbeing-log16"
EXPECTED_VISIBILITY="public"
PUBLISH_BRANCH="master"

cd "$REPO"

fail=0

note() { printf '%s\n' "$*"; }

status="$(git status --short)"
if [ -n "$status" ]; then
  note "FAIL: git status is not clean"
  note "$status"
  exit 2
fi
note "OK: git status clean"

current_branch="$(git branch --show-current)"
if [ "$current_branch" != "$PUBLISH_BRANCH" ]; then
  note "FAIL: current branch is $current_branch, expected $PUBLISH_BRANCH"
  exit 2
fi
note "OK: current branch $PUBLISH_BRANCH"

if git tag --list 'v0.3.3-lab' | grep -qx 'v0.3.3-lab'; then
  note "OK: tag exists: v0.3.3-lab"
else
  note "FAIL: missing tag: v0.3.3-lab"
  exit 2
fi

note "===== publication prep check ====="
scripts/check-github-publication-prep.sh

note "===== remote setup ====="
if git remote get-url origin >/tmp/log16-origin-url.txt 2>/dev/null; then
  existing="$(cat /tmp/log16-origin-url.txt)"
  if [ "$existing" = "$REMOTE_URL" ]; then
    note "OK: origin already matches expected remote"
  else
    note "FAIL: origin exists but differs"
    note "existing: $existing"
    note "expected: $REMOTE_URL"
    exit 2
  fi
else
  git remote add origin "$REMOTE_URL"
  note "OK: origin added: $REMOTE_URL"
fi

git remote -v

note "===== remote reachability ====="
if git ls-remote --heads origin >/tmp/log16-ls-remote-heads.txt 2>/tmp/log16-ls-remote-error.txt; then
  note "OK: git ls-remote origin succeeded"
  cat /tmp/log16-ls-remote-heads.txt
else
  note "FAIL: git ls-remote origin failed"
  cat /tmp/log16-ls-remote-error.txt
  note "This usually means repo does not exist yet on GitHub or SSH access is not configured."
  exit 2
fi

note "===== dry-run push branch ====="
git push --dry-run origin "$PUBLISH_BRANCH"

note "===== dry-run push tags ====="
git push --dry-run origin --tags

note "===== visibility note ====="
note "Expected visibility: $EXPECTED_VISIBILITY"
note "Visibility is a GitHub repo setting and is not verified by plain git over SSH."

note "GITHUB_REMOTE_SETUP_DRY_RUN_V02: OK"
note "No real push performed."
