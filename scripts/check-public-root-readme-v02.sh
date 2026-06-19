#!/usr/bin/env bash
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO"

file="docs/public/github-root-readme-draft-v02.md"
note="docs/public/github-root-readme-draft-v02-reading-note.md"

missing=0
for path in "$file" "$note"; do
  if [ -f "$path" ]; then
    echo "OK: $path"
  else
    echo "MISSING: $path"
    missing=$((missing + 1))
  fi
done

checks=(
  "большими массивами текстовой информации"
  "БЛАГОПОЛУЧИЕ выступает первым живым полигоном"
  "любому большому текстовому массиву"
  "рабочую систему знания"
  "не является готовым публичным продуктом"
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
  echo "PUBLIC_ROOT_README_V02: FAIL"
  exit 2
fi

echo "PUBLIC_ROOT_README_V02: OK"
