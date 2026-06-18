#!/usr/bin/env bash
set -Eeuo pipefail

APP="/data/wellbeing/obs/consultant/bin/consultant-pipeline-v05.2"
IMPORTER="/data/wellbeing/obs/log16/bin/log16-import-v05-run.sh"
STATUS="/data/wellbeing/obs/log16/bin/log16-status.sh"

if [ $# -lt 1 ]; then
  echo "Usage:"
  echo "  $0 \"Вопрос для КОНСУЛЬТАНТА\""
  exit 2
fi

question="$*"

if [ ! -x "$APP/bin/run-once.sh" ]; then
  echo "ERROR: v05.2 run-once not found: $APP/bin/run-once.sh" >&2
  exit 10
fi

tmp="$(mktemp)"
trap 'rm -f "$tmp"' EXIT

echo "QUESTION:"
echo "$question"
echo
echo "STEP 1: running consultant-pipeline-v05.2..."
"$APP/bin/run-once.sh" "$question" | tee "$tmp"

archive="$(grep -E '^ARCHIVE:' "$tmp" | tail -n 1 | sed 's/^ARCHIVE:[[:space:]]*//' || true)"

if [ -z "$archive" ] || [ ! -f "$archive" ]; then
  echo
  echo "ERROR: could not find ARCHIVE line or archive file after run." >&2
  echo "Look at output above. Apparently the machine hid the sausage again." >&2
  exit 30
fi

echo
echo "STEP 2: importing run into log16..."
echo "run archive: $archive"
"$IMPORTER" "$archive"

echo
echo "STEP 3: log16 status..."
"$STATUS"
