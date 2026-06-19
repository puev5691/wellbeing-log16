#!/usr/bin/env bash
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO"

required=(
  "docs/public/github-root-readme-draft-v01.md"
  "docs/public/github-root-readme-activation-note-v01.md"
  "docs/public/README.md"
  "docs/public/navigation.md"
  "docs/public/publication-boundary.md"
  "docs/public/knowledge-base/answers/index.md"
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

if ! grep -q "v0.3.0-lab" docs/public/github-root-readme-draft-v01.md; then
  echo "FAIL: root README draft does not mention v0.3.0-lab"
  missing=$((missing + 1))
fi

if ! grep -q "not ready" docs/public/github-root-readme-draft-v01.md; then
  echo "FAIL: root README draft does not state limitations"
  missing=$((missing + 1))
fi

if ! grep -q "publication-boundary" docs/public/github-root-readme-draft-v01.md; then
  echo "FAIL: root README draft does not reference publication boundary"
  missing=$((missing + 1))
fi

if [ "$missing" -gt 0 ]; then
  echo "PUBLIC_ROOT_README_DRAFT: FAIL"
  exit 2
fi

echo "PUBLIC_ROOT_README_DRAFT: OK"
