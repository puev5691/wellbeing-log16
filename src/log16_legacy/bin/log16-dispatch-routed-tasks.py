#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import tarfile
import time
import re
from pathlib import Path
from typing import Any

ROOT = Path("/data/wellbeing/obs/log16")
OUTBOX = Path("/data/wellbeing/obs/consultant/outbox")
ROUTED = ROOT / "derived-tasks" / "routed"
PENDING = ROOT / "entity-requests" / "pending"
RUNS = ROOT / "routed-task-dispatch-runs"

CODE_TO_ENTITY = {
    "KOORD": "koordinator",
    "CONS": "consultant",
    "VN": "vhodnoy-nastavnik",
    "SHKOLA": "shkola",
    "ARCH": "archivarius",
    "KODER": "koder",
    "SYS": "sysadmin",
    "RED": "redaktor",
    "KANC": "kancelyariya",
    "OPR": "operator"
}

ENTITY_LABELS = {
    "KOORD": "КООРДИНАТОР",
    "CONS": "КОНСУЛЬТАНТ",
    "VN": "ВХОДНОЙ НАСТАВНИК",
    "SHKOLA": "ШКОЛА",
    "ARCH": "АРХИВАРИУС",
    "KODER": "КОДЕР",
    "SYS": "СИСАДМИН",
    "RED": "РЕДАКТОР",
    "KANC": "КАНЦЕЛЯРИЯ",
    "OPR": "ОПЕРАТОР"
}

def now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S")

def stamp() -> str:
    return time.strftime("%Y%m%d-%H%M%S")

def slug(s: str) -> str:
    s = (s or "").lower().replace("ё", "е")
    s = re.sub(r"[^a-z0-9а-я_-]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s[:80] or "task"

def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))

def save_json(path: Path, data: dict[str, Any]):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def task_to_request(task: dict[str, Any], source_path: Path, run_stamp: str) -> dict[str, Any]:
    code = task.get("target_entity", "CONS")
    entity_id = CODE_TO_ENTITY.get(code, code.lower())
    task_id = task.get("task_id", source_path.stem)
    title = task.get("title", "Без названия")
    expected = task.get("expected_output", "draft response")
    done = task.get("done_criteria", [])
    reason = task.get("reason", "")

    request_id = f"request__{run_stamp}__{entity_id}__{slug(title)}"
    question = f"""Выполнить задачу topic-to-task.

Название задачи:
{title}

Причина:
{reason}

Ожидаемый результат:
{expected}

Критерии готовности:
{chr(10).join('- ' + str(x) for x in done)}
"""

    return {
        "request_id": request_id,
        "target_entity": entity_id,
        "target_entity_code": code,
        "target_entity_label": ENTITY_LABELS.get(code, code),
        "source_case": task.get("source_theme_key", task.get("source_theme", "topic_to_task")),
        "source_task_id": task_id,
        "source_task_card": str(source_path),
        "source_question": task.get("source_event", ""),
        "question": question,
        "expected_output": expected,
        "constraints": [
            "Ответ является draft для review, не approved canon.",
            "Не выдумывать источники.",
            "Если данных не хватает, указать конкретные вопросы.",
            "Результат оформить так, чтобы его можно было сохранить как Markdown-документ."
        ],
        "status": "pending",
        "created_at": now(),
        "created_by": "CONSULTANT/log16-dispatch-routed-tasks.py"
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--create", action="store_true", help="create entity_request cards")
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args()

    for d in [ROUTED, PENDING, RUNS]:
        d.mkdir(parents=True, exist_ok=True)

    run_stamp = stamp()
    run_id = f"routed-dispatch__{run_stamp}"
    run_dir = RUNS / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    paths = sorted(ROUTED.glob("*.json"))
    if args.limit:
        paths = paths[:args.limit]

    planned = []
    created = []

    for p in paths:
        task = load_json(p)
        req = task_to_request(task, p, run_stamp)
        planned.append((p, task, req))
        if args.create:
            req_path = PENDING / f"{req['request_id']}.json"
            save_json(req_path, req)
            created.append(req_path)

    summary = []
    summary.append("# routed task dispatch summary\n")
    summary.append(f"Created: {now()}\n")
    summary.append(f"Mode: {'CREATE' if args.create else 'REPORT_ONLY'}\n")
    summary.append(f"Routed tasks inspected: {len(paths)}\n")
    summary.append(f"Entity requests created: {len(created)}\n")
    summary.append("\n## Planned requests\n")
    for p, task, req in planned:
        summary.append(f"\n### {req['target_entity_label']} / {req['target_entity']}\n")
        summary.append(f"- title: {task.get('title')}")
        summary.append(f"- expected_output: {task.get('expected_output')}")
        summary.append(f"- source_task: {p}")
        summary.append(f"- request_id: {req['request_id']}")
        if args.create:
            summary.append(f"- request_card: {PENDING / (req['request_id'] + '.json')}")
    summary.append("\n## Human next action\n")
    if args.create:
        summary.append("1. Запустить runner по созданным pending requests.")
        summary.append("2. После runner проверить entity_responses.")
    else:
        summary.append("1. Проверить summary.")
        summary.append("2. Если нормально, запустить с --create.")
    summary.append("\nКТО: КОНСУЛЬТАНТ / log16-dispatch-routed-tasks.py")
    summary.append("ДЛЯ ЧЕГО: dispatch routed derived tasks в entity_requests")
    summary.append("СТАТУС: generated\n")

    summary_path = run_dir / "routed-dispatch-summary.md"
    summary_path.write_text("\n".join(summary), encoding="utf-8")

    manifest = {
        "run_id": run_id,
        "mode": "create" if args.create else "report_only",
        "routed_tasks_inspected": len(paths),
        "entity_requests_created": len(created),
        "summary": str(summary_path),
        "created_requests": [str(p) for p in created],
        "status": "PASS",
        "created_at": now()
    }
    save_json(run_dir / "manifest.json", manifest)

    archive = OUTBOX / f"CONS__routed-task-dispatch-{run_stamp}__OPR.tgz"
    with tarfile.open(archive, "w:gz") as tar:
        for p in sorted(run_dir.rglob("*")):
            tar.add(p, arcname=f"CONS__routed-task-dispatch__OPR/{p.relative_to(run_dir)}")
        for p in created:
            tar.add(p, arcname=f"CONS__routed-task-dispatch__OPR/entity-requests/{p.name}")

    print("PASS routed task dispatch completed")
    print(f"MODE: {'CREATE' if args.create else 'REPORT_ONLY'}")
    print(f"ROUTED_TASKS_INSPECTED: {len(paths)}")
    print(f"ENTITY_REQUESTS_CREATED: {len(created)}")
    print(f"SUMMARY: {summary_path}")
    print(f"ARCHIVE: {archive}")

if __name__ == "__main__":
    main()
