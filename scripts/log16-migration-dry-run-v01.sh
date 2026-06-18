#!/usr/bin/env bash
set -Eeuo pipefail

LEGACY_RUNTIME="/data/wellbeing/obs/consultant/outbox/log16-kernel"
TARGET_RUNTIME="/data/wellbeing/obs/log16"

echo "# log16 migration dry-run v01"
echo
echo "legacy_runtime: $LEGACY_RUNTIME"
echo "target_runtime: $TARGET_RUNTIME"
echo

echo "## Existence"
echo "legacy_exists: $([ -d "$LEGACY_RUNTIME" ] && echo YES || echo NO)"
echo "target_exists: $([ -d "$TARGET_RUNTIME" ] && echo YES || echo NO)"
echo

echo "## File counts"
echo "legacy_files: $(find "$LEGACY_RUNTIME" -type f 2>/dev/null | wc -l)"
echo "legacy_dirs: $(find "$LEGACY_RUNTIME" -type d 2>/dev/null | wc -l)"
echo "target_files: $(find "$TARGET_RUNTIME" -type f 2>/dev/null | wc -l || echo 0)"
echo "target_dirs: $(find "$TARGET_RUNTIME" -type d 2>/dev/null | wc -l || echo 0)"
echo

echo "## Size"
echo "legacy_size: $(du -sh "$LEGACY_RUNTIME" 2>/dev/null | awk '{print $1}')"
if [ -d "$TARGET_RUNTIME" ]; then
  echo "target_size: $(du -sh "$TARGET_RUNTIME" 2>/dev/null | awk '{print $1}')"
else
  echo "target_size: NOT_EXISTS"
fi
echo

echo "## Critical legacy files"
for f in \
  "$LEGACY_RUNTIME/bin/log16-pult" \
  "$LEGACY_RUNTIME/bin/log16-pult.py" \
  "$LEGACY_RUNTIME/bin/log16-dashboard.py" \
  "$LEGACY_RUNTIME/bin/log16-agent-runner.py"
do
  if [ -f "$f" ]; then
    echo "OK: $f"
  else
    echo "MISSING: $f"
  fi
done
echo

echo "## Top-level legacy layout"
find "$LEGACY_RUNTIME" -maxdepth 2 -type d | sort
echo

echo "## Target non-empty warning"
if [ -d "$TARGET_RUNTIME" ] && [ "$(find "$TARGET_RUNTIME" -mindepth 1 -maxdepth 1 | wc -l)" -gt 0 ]; then
  echo "WARNING: target runtime is not empty."
  echo "Actual migration must use merge/copy policy, not blind overwrite."
else
  echo "OK: target runtime empty or only skeleton."
fi
echo

echo "## Symlink feasibility"
if [ -L "$LEGACY_RUNTIME" ]; then
  echo "legacy_is_symlink: YES"
  echo "legacy_points_to: $(readlink "$LEGACY_RUNTIME")"
else
  echo "legacy_is_symlink: NO"
  echo "To create compatibility symlink later, migration must:"
  echo "1. backup legacy runtime"
  echo "2. copy legacy -> target"
  echo "3. rename legacy to backup"
  echo "4. ln -s target legacy"
fi
echo

echo "## Rsync dry-run"
if command -v rsync >/dev/null 2>&1; then
  rsync -a --dry-run --itemize-changes "$LEGACY_RUNTIME"/ "$TARGET_RUNTIME"/ | head -n 300
else
  echo "rsync not installed; fallback file list:"
  find "$LEGACY_RUNTIME" -type f | sed "s#^$LEGACY_RUNTIME/##" | sort | head -n 300
fi
