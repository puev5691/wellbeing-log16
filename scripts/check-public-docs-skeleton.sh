#!/usr/bin/env bash
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO"

required=(
  "docs/public/README.md"
  "docs/public/publication-boundary.md"
  "docs/public/project/what-is-wellbeing.md"
  "docs/public/project/what-is-log16.md"
  "docs/public/faq/index.md"
  "docs/public/participation/how-to-start.md"
  "docs/public/tasks/open-task-classes.md"
  "docs/public/glossary/index.md"
  "docs/public/status/current-stage.md"
  "docs/public/knowledge-base/answer-card-template.json"
  "schemas/public-answer-card-v01.schema.json"
  "examples/public-answer-card-example.json"
)

missing=0
for path in "${required[@]}"; do
  if [ -f "$path" ]; then
    echo "OK: $path"
  else
    echo "MISSING: $path"
    missing=$((missing + 1))
  fi
done

if [ "$missing" -gt 0 ]; then
  echo "PUBLIC_DOCS_SKELETON: FAIL"
  exit 2
fi

python3 -m json.tool schemas/public-answer-card-v01.schema.json >/dev/null
python3 -m json.tool examples/public-answer-card-example.json >/dev/null
python3 -m json.tool docs/public/knowledge-base/answer-card-template.json >/dev/null

echo "PUBLIC_DOCS_SKELETON: OK"
