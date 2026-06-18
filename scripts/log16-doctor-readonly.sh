#!/usr/bin/env bash
# Read-only environment diagnostics for log16.
# Does not modify repo/runtime.
# Does not start services.
# Does not pull models.

set -uo pipefail

REPO="${LOG16_REPO:-/data/wellbeing/repos/wellbeing-log16}"
RUNTIME="${LOG16_RUNTIME:-/data/wellbeing/obs/log16}"
OLLAMA_URL="${LOG16_OLLAMA_URL:-http://127.0.0.1:11434}"
MODEL="${LOG16_MODEL:-qwen3:8b}"

FAIL=0
WARN=0

section() {
  printf '\n## %s\n\n' "$1"
}

ok() {
  printf 'OK: %s\n' "$1"
}

warn() {
  printf 'WARN: %s\n' "$1"
  WARN=$((WARN + 1))
}

fail() {
  printf 'FAIL: %s\n' "$1"
  FAIL=$((FAIL + 1))
}

has_cmd() {
  command -v "$1" >/dev/null 2>&1
}

echo "# log16 doctor readonly"
echo
echo "repo: $REPO"
echo "runtime: $RUNTIME"
echo "ollama_url: $OLLAMA_URL"
echo "model: $MODEL"

section "Core commands"

for cmd in bash git python3 curl; do
  if has_cmd "$cmd"; then
    ok "$cmd found: $(command -v "$cmd")"
  else
    fail "$cmd not found"
  fi
done

if has_cmd bash; then
  echo "bash version: ${BASH_VERSION:-unknown}"
fi

if has_cmd git; then
  git --version || true
fi

if has_cmd python3; then
  python3 --version || true
fi

section "Repository"

if [ -d "$REPO/.git" ]; then
  ok "git repo exists"
  (
    cd "$REPO" || exit 1
    echo "branch: $(git branch --show-current 2>/dev/null || true)"
    echo "head: $(git rev-parse --short HEAD 2>/dev/null || true)"
    status="$(git status --short 2>/dev/null || true)"
    if [ -z "$status" ]; then
      ok "git status clean"
    else
      warn "git status not clean"
      printf '%s\n' "$status"
    fi
    if [ -x scripts/github-prepublish-check.sh ]; then
      echo
      echo "prepublish-check:"
      scripts/github-prepublish-check.sh || warn "prepublish-check returned non-zero"
    else
      warn "scripts/github-prepublish-check.sh not executable"
    fi
  )
else
  fail "git repo missing: $REPO"
fi

section "Runtime layout"

if [ -d "$RUNTIME" ]; then
  ok "runtime root exists"
else
  fail "runtime root missing: $RUNTIME"
fi

for p in \
  "$RUNTIME/bin/log16" \
  "$RUNTIME/bin/log16-pult" \
  "$RUNTIME/bin/log16-dashboard.sh" \
  "$RUNTIME/bin/log16-dashboard.py" \
  "$RUNTIME/entity-responses/needs_review" \
  "$RUNTIME/entity-requests/pending" \
  "$RUNTIME/runner-reports" \
  "$RUNTIME/reviews" \
  "$RUNTIME/reviewed-docs"
do
  if [ -e "$p" ]; then
    ok "exists: $p"
  else
    warn "missing: $p"
  fi
done

if [ -x "$RUNTIME/bin/log16" ]; then
  echo
  echo "log16 check --json:"
  "$RUNTIME/bin/log16" check --json || warn "log16 check returned non-zero"
else
  warn "runtime log16 CLI not executable"
fi

section "Ollama"

if has_cmd curl; then
  tags_tmp="$(mktemp)"
  if curl -fsS "$OLLAMA_URL/api/tags" > "$tags_tmp" 2>/dev/null; then
    ok "Ollama API responding: $OLLAMA_URL/api/tags"
    python3 - "$tags_tmp" "$MODEL" <<'PY_TAGS' || true
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
target = sys.argv[2]

try:
    data = json.loads(path.read_text(encoding="utf-8"))
except Exception as exc:
    print(f"WARN: cannot parse Ollama tags JSON: {exc}")
    sys.exit(0)

models = []
for item in data.get("models", []):
    name = item.get("name") or item.get("model")
    if name:
        models.append(name)

print("models:")
for name in models:
    print(f"  {name}")

if target in models:
    print(f"OK: required model found: {target}")
else:
    print(f"WARN: required model not found: {target}")
PY_TAGS
  else
    warn "Ollama API not responding: $OLLAMA_URL/api/tags"
  fi
  rm -f "$tags_tmp"
else
  warn "curl not available, Ollama API not checked"
fi

section "Ports"

if has_cmd ss; then
  echo "listening ports related to 11434/8898/8794:"
  ss -ltn 2>/dev/null | grep -E '(:11434|:8898|:8794)' || true
else
  warn "ss not available, port check skipped"
fi

section "Disk"

df -h "$REPO" "$RUNTIME" 2>/dev/null || df -h 2>/dev/null || true

section "Summary"

echo "failures: $FAIL"
echo "warnings: $WARN"

if [ "$FAIL" -gt 0 ]; then
  echo "DOCTOR_STATUS: FAIL"
  exit 2
fi

if [ "$WARN" -gt 0 ]; then
  echo "DOCTOR_STATUS: WARN"
  exit 0
fi

echo "DOCTOR_STATUS: OK"
exit 0
