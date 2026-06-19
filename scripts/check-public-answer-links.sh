#!/usr/bin/env bash
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO"

python3 - <<'PY_CHECK'
import json
from pathlib import Path

cards = sorted(Path("docs/public/knowledge-base/answers").glob("*.json"))
errors = 0

for path in cards:
    data = json.loads(path.read_text(encoding="utf-8"))

    related_docs = data.get("related_docs", [])
    if not related_docs:
        print(f"FAIL: {path}: related_docs empty")
        errors += 1

    for doc in related_docs:
        if not Path(doc).exists():
            print(f"FAIL: {path}: related_doc missing: {doc}")
            errors += 1

    routing = data.get("routing", {})
    next_docs = routing.get("next_docs", [])
    if not next_docs:
        print(f"FAIL: {path}: routing.next_docs empty")
        errors += 1

    for doc in next_docs:
        if not Path(doc).exists():
            print(f"FAIL: {path}: routing next_doc missing: {doc}")
            errors += 1

    print(f"OK: {path}")

if errors:
    raise SystemExit("PUBLIC_ANSWER_LINKS: FAIL")

print(f"PUBLIC_ANSWER_LINKS: OK count={len(cards)}")
PY_CHECK
