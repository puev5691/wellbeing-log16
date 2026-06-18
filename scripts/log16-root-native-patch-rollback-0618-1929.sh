#!/usr/bin/env bash
set -Eeuo pipefail

TARGET_RUNTIME="/data/wellbeing/obs/log16"
BACKUP_BIN="/data/wellbeing/obs/log16/backups/bin-before-root-native-patch-0618-1929"

echo "Rollback log16 root native patch"
echo "target: $TARGET_RUNTIME"
echo "backup_bin: $BACKUP_BIN"

if [ ! -d "$BACKUP_BIN" ]; then
  echo "ERROR: backup bin not found: $BACKUP_BIN" >&2
  exit 20
fi

rm -rf "$TARGET_RUNTIME/bin"
cp -a "$BACKUP_BIN" "$TARGET_RUNTIME/bin"

echo "Rollback done."
