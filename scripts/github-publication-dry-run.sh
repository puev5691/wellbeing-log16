#!/usr/bin/env bash
# Read-only GitHub publication dry-run.
# Does not add remote.
# Does not push.

set -Eeuo pipefail

REPO="${1:-/data/wellbeing/repos/wellbeing-log16}"
cd "$REPO"

echo "# GitHub publication dry-run"
echo
echo "repo: $REPO"
echo "branch: $(git branch --show-current)"
echo "head: $(git rev-parse --short HEAD)"
echo

echo "## git status"
git status --short
echo

echo "## tags"
git tag --list 'v*' | sort
echo

echo "## remotes"
git remote -v || true
echo

echo "## prepublish check"
scripts/github-prepublish-check.sh
echo

echo "## gh CLI"
if command -v gh >/dev/null 2>&1; then
  gh --version | head -n 1 || true
  gh auth status || true
else
  echo "gh CLI not installed or not in PATH"
fi
echo

echo "## command templates, NOT EXECUTED"
cat <<'EOF_CMDS'
# Variant A: create repo manually on GitHub, then add remote locally:
git remote add origin <GITHUB_REMOTE_URL>
git remote -v
git push -u origin master
git push origin --tags

# Variant B: if gh CLI is installed and authenticated:
gh repo create <OWNER>/wellbeing-log16 --private --source=. --remote=origin --push
git push origin --tags

# Before any real push:
scripts/github-prepublish-check.sh
git status --short
EOF_CMDS

echo
echo "DRY_RUN_ONLY"
