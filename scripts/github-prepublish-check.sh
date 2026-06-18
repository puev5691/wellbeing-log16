#!/usr/bin/env bash
# Read-only GitHub prepublish sanitation check.
# Does not modify repo.
# Does not add remote.
# Does not push.

set -Eeuo pipefail

REPO="${1:-/data/wellbeing/repos/wellbeing-log16}"
cd "$REPO"

FAIL=0

say() { printf '%s\n' "$*"; }
fail() { say "FAIL: $*"; FAIL=1; }
ok() { say "OK: $*"; }
warn() { say "WARN: $*"; }

status="$(git status --short)"
if [ -n "$status" ]; then
  fail "git status is not clean"
  printf '%s\n' "$status"
else
  ok "git status clean"
fi

tracked_runtime="$(git ls-files | grep -E '^(runtime|var|archives|dashboard-runs|runner-reports|pult-runs|entity-responses|entity-requests|derived-tasks|themes|reviews|reviewed-docs|backups)/' || true)"
if [ -n "$tracked_runtime" ]; then
  fail "runtime-like tracked paths found"
  printf '%s\n' "$tracked_runtime"
else
  ok "no runtime-like tracked root paths"
fi

tracked_archives="$(git ls-files | grep -E '\.(tgz|tar|tar\.gz|zip|7z|rar)$' || true)"
if [ -n "$tracked_archives" ]; then
  fail "tracked archive files found"
  printf '%s\n' "$tracked_archives"
else
  ok "no tracked archive files"
fi

large_files="$(git ls-files -z | xargs -0 -r du -b 2>/dev/null | awk '$1 > 1048576 {print $0}' || true)"
if [ -n "$large_files" ]; then
  warn "tracked files over 1 MiB found"
  printf '%s\n' "$large_files"
else
  ok "no tracked files over 1 MiB"
fi

python3 - <<'PY_SECRET'
from __future__ import annotations

import re
from pathlib import Path
import subprocess
import sys

repo = Path.cwd()
tracked = subprocess.check_output(["git", "ls-files"], text=True).splitlines()

skip_files = {
    ".gitignore",
    "scripts/check-no-runtime-in-repo.sh",
    "scripts/github-prepublish-check.sh",
    "docs/log16-github-sanitation-audit-v01-review.md",
}

skip_suffixes = {
    ".png", ".jpg", ".jpeg", ".webp", ".gif", ".pdf",
    ".tgz", ".tar", ".gz", ".zip", ".7z", ".rar",
    ".pyc", ".sqlite", ".db",
}

fatal_patterns = [
    ("private_key_block", re.compile(r"BEGIN [A-Z ]*PRIVATE KEY")),
    ("bearer_auth", re.compile(r"Authorization\s*:\s*Bearer\s+\S+", re.I)),
    ("github_token_value", re.compile(r"\b(ghp_|github_pat_)[A-Za-z0-9_]{20,}")),
    ("openai_key_value", re.compile(r"\bsk-[A-Za-z0-9]{20,}\b")),
    ("api_key_assignment", re.compile(r"\b(OPENAI_API_KEY|ANTHROPIC_API_KEY|GITHUB_TOKEN|GH_TOKEN)\s*=\s*[^\s#]+")),
]

hits = []
for rel in tracked:
    if rel in skip_files:
        continue
    if any(rel.endswith(s) for s in skip_suffixes):
        continue
    path = repo / rel
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        continue
    for lineno, line in enumerate(text.splitlines(), start=1):
        for name, rx in fatal_patterns:
            if rx.search(line):
                hits.append((rel, lineno, name))

if hits:
    print("FAIL: fatal secret-like values found")
    for rel, lineno, name in hits:
        print(f"{rel}:{lineno}:{name}")
    sys.exit(2)

print("OK: no fatal secret-like values found")
PY_SECRET
secret_rc=$?
if [ "$secret_rc" -ne 0 ]; then
  FAIL=1
fi

if [ "$FAIL" -eq 0 ]; then
  say "READY_FOR_GITHUB_PREP"
else
  say "NOT_READY_FOR_PUSH"
fi

exit "$FAIL"
