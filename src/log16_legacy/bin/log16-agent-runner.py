#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import tarfile
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path("/data/wellbeing/obs/log16")
REGISTRY = ROOT / "entity-registry" / "entity-registry.json"
PENDING = ROOT / "entity-requests" / "pending"
RUNNING = ROOT / "entity-requests" / "running"
DONE = ROOT / "entity-requests" / "done"
FAILED = ROOT / "entity-requests" / "failed"
RESPONSES = ROOT / "entity-responses" / "needs_review"
RESPONSES_FAILED = ROOT / "entity-responses" / "failed"
REPORTS = ROOT / "runner-reports"
OUTBOX = Path("/data/wellbeing/obs/consultant/outbox")
OLLAMA_URL = "http://127.0.0.1:11434"

def now():
    return time.strftime("%Y-%m-%dT%H:%M:%S")

def stamp():
    return time.strftime("%Y%m%d-%H%M%S")

def slug(s: str) -> str:
    s = (s or "").lower().replace("ё", "е")
    s = re.sub(r"[^a-z0-9а-я_-]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s[:80] or "case"

def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))

def save_json(path: Path, data: dict[str, Any]):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def load_registry() -> dict[str, Any]:
    if not REGISTRY.exists():
        raise SystemExit(f"ERROR: registry not found: {REGISTRY}")
    data = load_json(REGISTRY)
    return {e["entity_id"]: e for e in data.get("entities", [])}

def ollama_tags() -> list[str]:
    try:
        with urllib.request.urlopen(f"{OLLAMA_URL}/api/tags", timeout=5) as r:
            data = json.loads(r.read().decode("utf-8"))
        return [m.get("name", "") for m in data.get("models", []) if m.get("name")]
    except Exception:
        return []

def choose_model(preferred: str, available: list[str]) -> tuple[str, str | None]:
    if preferred in available:
        return preferred, None
    prefix = preferred.split(":")[0] if preferred else ""
    if prefix:
        for m in available:
            if m.startswith(prefix):
                return m, f"preferred_model_not_found_used_prefix_match:{m}"
    if available:
        return available[0], f"preferred_model_not_found_used_first_available:{available[0]}"
    return preferred or "qwen3:8b", "no_ollama_models_found"

def call_ollama(model: str, prompt: str, timeout: int = 600) -> tuple[bool, str, str | None]:
    payload = json.dumps({
        "model": model,
        "prompt": prompt,
        "stream": False
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{OLLAMA_URL}/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = json.loads(r.read().decode("utf-8"))
        return True, data.get("response", ""), None
    except urllib.error.HTTPError as e:
        try:
            body = e.read().decode("utf-8", errors="replace")
        except Exception:
            body = ""
        return False, "", f"http_error:{e.code}:{body[:500]}"
    except Exception as e:
        return False, "", f"{type(e).__name__}:{e}"

def is_participant_pathway(req: dict[str, Any]) -> bool:
    blob = " ".join(str(req.get(k, "")) for k in [
        "source_case", "source_question", "question", "expected_output", "source_task_id"
    ]).lower()
    return "participant_pathway" in blob or "participant-pathway" in blob

def build_prompt(entity: dict[str, Any], req: dict[str, Any]) -> str:
    constraints = "\n".join(f"- {c}" for c in req.get("constraints", []))
    expected = req.get("expected_output", "draft response")
    source_case = req.get("source_case", "unknown")
    source_task_id = req.get("source_task_id", "")
    source_task_card = req.get("source_task_card", "")

    if is_participant_pathway(req):
        result_section = f"""3. Предлагаемый фрагмент для `{expected}`.
4. Какие решения должен принять ОПЕРАТОР / КООРДИНАТОР.
5. Что остаётся неясным.
6. Какие следующие карточки log16 нужны."""
    else:
        result_section = f"""3. Черновой результат для `{expected}`.
4. Какие решения должен принять ОПЕРАТОР / КООРДИНАТОР / адресная Сущность.
5. Что остаётся неясным.
6. Какие следующие карточки log16 нужны."""

    return f"""# Роль Сущности

{entity.get("role_prompt", "")}

# Задача

Адресная Сущность:
{entity.get("display_name")} / {entity.get("entity_id")}

Source case:
{source_case}

Source task:
{source_task_id}

Source task card:
{source_task_card}

Исходный вопрос / событие:
{req.get("source_question", "")}

Текущий вопрос к этой Сущности:
{req.get("question")}

Ожидаемый результат:
{expected}

Ограничения:
{constraints}

# Формат ответа

Дай ответ строго по-русски.

Структура:
1. Краткий вывод.
2. Что должна сделать эта Сущность.
{result_section}

Не утверждай канон окончательно.
Не имитируй внешние источники.
Если данных не хватает, укажи конкретные вопросы.
Не уходи в общую философию, держись expected_output.
"""

def move_request(src: Path, dst_dir: Path, status: str) -> Path:
    data = load_json(src)
    data["status"] = status
    data["updated_at"] = now()
    dst = dst_dir / src.name
    save_json(dst, data)
    try:
        src.unlink()
    except FileNotFoundError:
        pass
    return dst

def run(case_filter: str | None = None, limit: int | None = None, target_entity: str | None = None):
    for d in [PENDING, RUNNING, DONE, FAILED, RESPONSES, RESPONSES_FAILED, REPORTS]:
        d.mkdir(parents=True, exist_ok=True)

    registry = load_registry()
    available = ollama_tags()

    case_slug = slug(case_filter or "all")
    run_id = f"runner__{stamp()}__{case_slug}"
    run_dir = REPORTS / run_id
    raw_dir = run_dir / "raw"
    prompts_dir = run_dir / "prompts"
    raw_dir.mkdir(parents=True, exist_ok=True)
    prompts_dir.mkdir(parents=True, exist_ok=True)

    requests = sorted(PENDING.glob("*.json"))
    selected = []
    for p in requests:
        req = load_json(p)
        if case_filter and case_filter not in str(req.get("source_case", "")):
            continue
        if target_entity and target_entity != str(req.get("target_entity", "")):
            continue
        selected.append(p)
    if limit:
        selected = selected[:limit]

    summary = []
    summary.append(f"# log16 agent runner report\n")
    summary.append(f"Run id: {run_id}\n")
    summary.append(f"Started: {now()}\n")
    summary.append(f"Case filter: {case_filter}\n")
    summary.append(f"Target entity filter: {target_entity}\n")
    summary.append(f"Pending selected: {len(selected)}\n")
    summary.append(f"Ollama models available: {', '.join(available) if available else 'none'}\n")

    responses_created = []
    failed = []

    for path in selected:
        req = load_json(path)
        target = req.get("target_entity")
        entity = registry.get(target)
        if not entity:
            failed.append((path, "entity_not_in_registry"))
            move_request(path, FAILED, "failed")
            continue

        running_path = move_request(path, RUNNING, "running")
        req = load_json(running_path)

        preferred = entity.get("model", "qwen3:8b")
        model, model_note = choose_model(preferred, available)
        prompt = build_prompt(entity, req)

        prompt_path = prompts_dir / f"{req['request_id']}.prompt.md"
        prompt_path.write_text(prompt, encoding="utf-8")

        ok, response_text, error = call_ollama(model, prompt)

        source_case = slug(str(req.get("source_case", "unknown")))
        response_id = f"response__{stamp()}__{target}__{source_case}"
        raw_path = raw_dir / f"{response_id}.txt"
        raw_path.write_text(response_text if response_text else (error or ""), encoding="utf-8")

        response_card = {
            "response_id": response_id,
            "request_id": req.get("request_id"),
            "target_entity": target,
            "target_display_name": entity.get("display_name"),
            "provider": "ollama",
            "model": model,
            "model_note": model_note,
            "source_case": req.get("source_case"),
            "source_task_id": req.get("source_task_id"),
            "source_task_card": req.get("source_task_card"),
            "source_question": req.get("source_question"),
            "question": req.get("question"),
            "expected_output": req.get("expected_output"),
            "response_text": response_text,
            "raw_response_path": str(raw_path),
            "error": error,
            "status": "needs_review" if ok and response_text.strip() else "failed",
            "created_at": now(),
            "requires_human_review": True
        }

        if ok and response_text.strip():
            resp_path = RESPONSES / f"{response_id}.json"
            save_json(resp_path, response_card)
            move_request(running_path, DONE, "done")
            responses_created.append(resp_path)
            summary.append(f"\n## {entity.get('display_name')} / {target}\n")
            summary.append(f"Status: needs_review\n")
            summary.append(f"Source case: {req.get('source_case')}\n")
            summary.append(f"Expected output: {req.get('expected_output')}\n")
            summary.append(f"Model: {model}\n")
            if model_note:
                summary.append(f"Model note: {model_note}\n")
            summary.append(f"Response card: {resp_path}\n")
            summary.append("\n### Ответ\n")
            summary.append(response_text[:8000] + "\n")
        else:
            resp_path = RESPONSES_FAILED / f"{response_id}.json"
            save_json(resp_path, response_card)
            move_request(running_path, FAILED, "failed")
            failed.append((path, error or "empty_response"))
            summary.append(f"\n## FAILED {target}\n")
            summary.append(f"Error: {error or 'empty_response'}\n")
            summary.append(f"Response card: {resp_path}\n")

    summary.append("\n# Human next action\n")
    if responses_created:
        summary.append("1. Прочитать этот runner-summary.md.\n")
        summary.append("2. Проверить entity_response cards.\n")
        summary.append("3. Запустить synthesis/review слой для полученных expected_output.\n")
        summary.append("4. Не считать ответы approved без review.\n")
    else:
        summary.append("1. Проверить Ollama, модели, registry и pending requests.\n")

    summary.append("\n# Machine summary\n")
    summary.append(f"- responses_created: {len(responses_created)}\n")
    summary.append(f"- failed: {len(failed)}\n")

    report_path = run_dir / "runner-summary.md"
    report_path.write_text("\n".join(summary), encoding="utf-8")

    manifest = {
        "run_id": run_id,
        "root": str(ROOT),
        "case_filter": case_filter,
        "target_entity_filter": target_entity,
        "selected_requests": len(selected),
        "responses_created": len(responses_created),
        "failed": len(failed),
        "report": str(report_path),
        "status": "PASS" if responses_created else "NO_RESPONSES",
        "created_at": now()
    }
    save_json(run_dir / "manifest.json", manifest)

    archive = OUTBOX / f"CONS__log16-agent-runner-v01-{stamp()}__OPR.tgz"
    with tarfile.open(archive, "w:gz") as tar:
        for p in sorted(run_dir.rglob("*")):
            tar.add(p, arcname=f"CONS__log16-agent-runner-v01__OPR/{p.relative_to(run_dir)}")

    print("PASS log16 agent runner completed" if responses_created else "WARN log16 agent runner completed without responses")
    print(f"REQUESTS_SELECTED: {len(selected)}")
    print(f"RESPONSES_CREATED: {len(responses_created)}")
    print(f"FAILED: {len(failed)}")
    print(f"SUMMARY: {report_path}")
    print(f"ARCHIVE: {archive}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", default=None, help="source_case filter, e.g. topic_to_task_system")
    ap.add_argument("--target-entity", default=None, help="target_entity filter, e.g. archivarius")
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args()
    run(args.case, args.limit, args.target_entity)

if __name__ == "__main__":
    main()
