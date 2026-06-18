#!/usr/bin/env bash
set -Eeuo pipefail

REPO="/data/wellbeing/repos/wellbeing-log16"
LEGACY="/data/wellbeing/obs/consultant/outbox/log16-kernel"
TARGET="/data/wellbeing/obs/log16"

echo "# log16 root usage report"
echo
echo "repo: $REPO"
echo "legacy runtime: $LEGACY"
echo "target runtime: $TARGET"
echo
echo "Legacy exists:"
[ -d "$LEGACY" ] && echo "YES" || echo "NO"
echo
echo "Target exists:"
[ -d "$TARGET" ] && echo "YES" || echo "NO"
echo
echo "Legacy bin files:"
find "$LEGACY/bin" -maxdepth 1 -type f 2>/dev/null | sort || true
echo
echo "Repo legacy bin files:"
find "$REPO/src/log16_legacy/bin" -maxdepth 1 -type f 2>/dev/null | sort || true
