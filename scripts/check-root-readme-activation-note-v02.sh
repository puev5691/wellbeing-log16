#!/usr/bin/env bash
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO"

file="docs/productization/log16-root-readme-activation-v02.md"
missing=0

if [ -f "$file" ]; then
  echo "OK: $file"
else
  echo "MISSING: $file"
  exit 2
fi

checks=(
  "docs/public/github-root-readme-draft-v02.md"
  "README.md"
  "unquoted heredoc"
  "Permission denied"
  "command not found"
  "СТАТУС: fixed"
)

for needle in "${checks[@]}"; do
  if grep -q "$needle" "$file"; then
    echo "OK: contains: $needle"
  else
    echo "FAIL: missing phrase: $needle"
    missing=$((missing + 1))
  fi
done

if [ "$missing" -gt 0 ]; then
  echo "ROOT_README_ACTIVATION_NOTE_V02: FAIL"
  exit 2
fi

echo "ROOT_README_ACTIVATION_NOTE_V02: OK"
