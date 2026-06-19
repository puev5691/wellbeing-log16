#!/usr/bin/env bash
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO"

required=(
  "CONTRIBUTING.md"
  ".github/ISSUE_TEMPLATE/config.yml"
  ".github/ISSUE_TEMPLATE/documentation_feedback.md"
  ".github/ISSUE_TEMPLATE/question_or_gap.md"
  ".github/ISSUE_TEMPLATE/local_diagnostics_report.md"
  ".github/ISSUE_TEMPLATE/task_proposal.md"
  ".github/PULL_REQUEST_TEMPLATE.md"
)

missing=0
for path in "${required[@]}"; do
  if [ -f "$path" ]; then
    echo "OK: $path"
  else
    echo "MISSING: $path"
    missing=$((missing + 1))
  fi
done

checks=(
  "CONTRIBUTING.md:private credentials"
  "CONTRIBUTING.md:local lab"
  ".github/PULL_REQUEST_TEMPLATE.md:private credentials"
  ".github/ISSUE_TEMPLATE/documentation_feedback.md:documentation"
  ".github/ISSUE_TEMPLATE/question_or_gap.md:knowledge-gap"
  ".github/ISSUE_TEMPLATE/local_diagnostics_report.md:diagnostics"
  ".github/ISSUE_TEMPLATE/task_proposal.md:task-proposal"
)

for item in "${checks[@]}"; do
  file="${item%%:*}"
  needle="${item#*:}"
  if grep -q "$needle" "$file"; then
    echo "OK: $file contains: $needle"
  else
    echo "FAIL: $file missing: $needle"
    missing=$((missing + 1))
  fi
done

if [ "$missing" -gt 0 ]; then
  echo "GITHUB_PUBLIC_TEMPLATES: FAIL"
  exit 2
fi

echo "GITHUB_PUBLIC_TEMPLATES: OK"
