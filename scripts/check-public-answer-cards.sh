#!/usr/bin/env bash
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO"

python3 - <<'PY_CHECK'
import json
from pathlib import Path

schema = json.loads(Path("schemas/public-answer-card-v01.schema.json").read_text(encoding="utf-8"))
required = schema["required"]
status_values = set(schema["status_values"])
source_status_values = set(schema["source_status_values"])
review_level_values = set(schema["review_level_values"])

cards_dir = Path("docs/public/knowledge-base/answers")
cards = sorted(cards_dir.glob("*.json"))

if not cards:
    raise SystemExit("PUBLIC_ANSWER_CARDS: FAIL no cards found")

errors = 0
for path in cards:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"FAIL: {path}: invalid JSON: {exc}")
        errors += 1
        continue

    for key in required:
        if key not in data:
            print(f"FAIL: {path}: missing {key}")
            errors += 1

    if data.get("status") not in status_values:
        print(f"FAIL: {path}: invalid status {data.get('status')}")
        errors += 1

    if data.get("source_status") not in source_status_values:
        print(f"FAIL: {path}: invalid source_status {data.get('source_status')}")
        errors += 1

    if data.get("review_level") not in review_level_values:
        print(f"FAIL: {path}: invalid review_level {data.get('review_level')}")
        errors += 1

    print(f"OK: {path}")

if errors:
    raise SystemExit("PUBLIC_ANSWER_CARDS: FAIL")

print(f"PUBLIC_ANSWER_CARDS: OK count={len(cards)}")
PY_CHECK
