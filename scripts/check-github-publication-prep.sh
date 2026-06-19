#!/usr/bin/env bash
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUNTIME="/data/wellbeing/obs/log16"
cd "$REPO"

fail=0

require_clean() {
  local status
  status="$(git status --short)"
  if [ -n "$status" ]; then
    echo "FAIL: git status is not clean"
    echo "$status"
    fail=$((fail + 1))
  else
    echo "OK: git status clean"
  fi
}

require_tag() {
  local tag="$1"
  if git tag --list "$tag" | grep -qx "$tag"; then
    echo "OK: tag exists: $tag"
  else
    echo "FAIL: missing tag: $tag"
    fail=$((fail + 1))
  fi
}

run_check() {
  local name="$1"
  shift
  echo "===== $name ====="
  if "$@"; then
    echo "OK: $name"
  else
    echo "FAIL: $name"
    fail=$((fail + 1))
  fi
}

require_clean
require_tag "v0.3.3-lab"

run_check "root README active v02" scripts/check-root-readme-active-v02.sh
run_check "root README activation note" scripts/check-root-readme-activation-note-v02.sh
run_check "GitHub public templates" scripts/check-github-public-templates.sh
run_check "public docs skeleton" scripts/check-public-docs-skeleton.sh
run_check "public answer cards" scripts/check-public-answer-cards.sh
run_check "public answer links" scripts/check-public-answer-links.sh
run_check "unit tests" scripts/run-tests.sh
run_check "prepublish" scripts/github-prepublish-check.sh

if [ -x "$RUNTIME/bin/log16" ]; then
  echo "===== doctor ====="
  if "$RUNTIME/bin/log16" doctor --json >/tmp/log16-publication-prep-doctor.json; then
    if grep -q '"ok": true' /tmp/log16-publication-prep-doctor.json; then
      echo "OK: doctor JSON ok true"
    else
      echo "FAIL: doctor JSON did not report ok true"
      cat /tmp/log16-publication-prep-doctor.json
      fail=$((fail + 1))
    fi
  else
    echo "FAIL: doctor command failed"
    fail=$((fail + 1))
  fi
else
  echo "FAIL: log16 runtime command missing: $RUNTIME/bin/log16"
  fail=$((fail + 1))
fi

echo "===== remote status ====="
if git remote -v | grep -q .; then
  git remote -v
  echo "INFO: remote exists; this script does not push"
else
  echo "OK: no remote configured; publication prep remains local"
fi

if [ "$fail" -gt 0 ]; then
  echo "GITHUB_PUBLICATION_PREP: FAIL failures=$fail"
  exit 2
fi

echo "GITHUB_PUBLICATION_PREP: OK"
