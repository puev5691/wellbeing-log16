#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="/data/wellbeing/obs/log16"
latest="$(find "$ROOT/reports" -type f -name '*.md' -printf '%T@ %p\n' 2>/dev/null | sort -n | tail -n 1 | cut -d' ' -f2- || true)"

if [ -z "$latest" ]; then
  echo "No log16 reports found."
  exit 1
fi

echo "LATEST LOG16 REPORT:"
echo "$latest"
echo
cat "$latest"
