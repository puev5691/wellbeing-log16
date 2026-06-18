#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="/data/wellbeing/obs/log16"

echo "LOG16 AGENT RUNNER GENERIC CHECK"
echo "root: $ROOT"
python3 -m py_compile "$ROOT/bin/log16-agent-runner.py"
echo "py_compile: OK"
echo "pending topic_to_task_system:"
grep -l '"source_case": "topic_to_task_system"' "$ROOT"/entity-requests/pending/*.json 2>/dev/null | wc -l
echo "pending participant_communication:"
grep -l '"source_case": "participant_communication"' "$ROOT"/entity-requests/pending/*.json 2>/dev/null | wc -l
echo "registry entities:"
python3 - <<'PY'
import json
from pathlib import Path
p=Path("/data/wellbeing/obs/log16/entity-registry/entity-registry.json")
d=json.loads(p.read_text(encoding="utf-8"))
print(", ".join(e.get("entity_id","?") for e in d.get("entities",[])))
PY
