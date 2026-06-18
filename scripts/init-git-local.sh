#!/usr/bin/env bash
set -Eeuo pipefail

REPO="/data/wellbeing/repos/wellbeing-log16"
cd "$REPO"

git init
git add README.md pyproject.toml .gitignore src schemas docs scripts tests examples
git status

echo
echo "Review git status before commit."
echo "If clean and safe:"
echo "  git commit -m 'Initial lab assembly of wellbeing-log16'"
