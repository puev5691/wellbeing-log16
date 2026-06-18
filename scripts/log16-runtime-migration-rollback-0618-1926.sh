#!/usr/bin/env bash
set -Eeuo pipefail

LEGACY_RUNTIME="/data/wellbeing/obs/consultant/outbox/log16-kernel"
TARGET_RUNTIME="/data/wellbeing/obs/log16"
BACKUP_RUNTIME="/data/wellbeing/obs/consultant/outbox/log16-kernel.backup-0618-1926"

echo "Rollback log16 runtime migration"
echo "legacy: $LEGACY_RUNTIME"
echo "target: $TARGET_RUNTIME"
echo "backup: $BACKUP_RUNTIME"

if [ ! -L "$LEGACY_RUNTIME" ]; then
  echo "ERROR: legacy runtime is not a symlink, refusing rollback." >&2
  exit 20
fi

if [ ! -d "$BACKUP_RUNTIME" ]; then
  echo "ERROR: backup runtime not found: $BACKUP_RUNTIME" >&2
  exit 21
fi

rm "$LEGACY_RUNTIME"
mv "$BACKUP_RUNTIME" "$LEGACY_RUNTIME"

echo "Rollback done."
echo "NOTE: target runtime remains at: $TARGET_RUNTIME"
