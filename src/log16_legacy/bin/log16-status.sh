#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="/data/wellbeing/obs/log16"

count_files() {
  local dir="$1"
  if [ -d "$dir" ]; then
    find "$dir" -type f -name '*.json' 2>/dev/null | wc -l
  else
    echo 0
  fi
}

latest_file() {
  local dir="$1"
  if [ -d "$dir" ]; then
    find "$dir" -type f \( -name '*.json' -o -name '*.md' \) -printf '%T@ %p\n' 2>/dev/null | sort -n | tail -n 1 | cut -d' ' -f2-
  fi
}

echo "LOG16 STATUS"
echo "root: $ROOT"
echo
echo "cards:"
echo "  answers needs_review: $(count_files "$ROOT/answers/needs_review")"
echo "  answers approved:     $(count_files "$ROOT/answers/approved")"
echo "  gaps detected:        $(count_files "$ROOT/gaps/detected")"
echo "  tasks proposed:       $(count_files "$ROOT/tasks/proposed")"
echo "  reviews:              $(count_files "$ROOT/reviews")"
echo "  reports:              $(find "$ROOT/reports" -type f -name '*.md' 2>/dev/null | wc -l)"
echo
echo "latest by mtime:"
echo "  answer: $(latest_file "$ROOT/answers/needs_review")"
echo "  gap:    $(latest_file "$ROOT/gaps/detected")"
echo "  task:   $(latest_file "$ROOT/tasks/proposed")"
echo "  review: $(latest_file "$ROOT/reviews")"
echo "  report: $(latest_file "$ROOT/reports")"
echo
echo "case hints:"
echo "  participant pathway: $ROOT/bin/log16-participant-pathway-case.sh"
echo "  generic case:        $ROOT/bin/log16-case-summary.sh --pattern participant_pathway"
