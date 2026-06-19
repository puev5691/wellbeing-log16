#!/usr/bin/env bash
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO"

root="README.md"
draft="docs/public/github-root-readme-draft-v02.md"

missing=0
for path in "$root" "$draft"; do
  if [ -f "$path" ]; then
    echo "OK: $path"
  else
    echo "MISSING: $path"
    missing=$((missing + 1))
  fi
done

if ! cmp -s "$root" "$draft"; then
  echo "FAIL: README.md differs from draft v02"
  missing=$((missing + 1))
else
  echo "OK: README.md matches draft v02"
fi

checks=(
  "большими массивами текстовой информации"
  "БЛАГОПОЛУЧИЕ выступает первым живым полигоном"
  "любому большому текстовому массиву"
  "рабочую систему знания"
  "не является готовым публичным продуктом"
)

for needle in "${checks[@]}"; do
  if grep -q "$needle" "$root"; then
    echo "OK: contains: $needle"
  else
    echo "FAIL: missing phrase: $needle"
    missing=$((missing + 1))
  fi
done

if [ "$missing" -gt 0 ]; then
  echo "ROOT_README_ACTIVE_V02: FAIL"
  exit 2
fi

echo "ROOT_README_ACTIVE_V02: OK"
