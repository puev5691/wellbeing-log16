#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
import tarfile
import time
from pathlib import Path
from typing import Any

ROOT = Path("/data/wellbeing/obs/log16")
OUTBOX = Path("/data/wellbeing/obs/consultant/outbox")
PROPOSED = ROOT / "derived-tasks" / "proposed"
ROUTED = ROOT / "derived-tasks" / "routed"
DONE = ROOT / "derived-tasks" / "done"
REJECTED = ROOT / "derived-tasks" / "rejected"
ARCHIVED = ROOT / "derived-tasks" / "archived"
RUNS = ROOT / "topic-task-triage-runs"

ENTITY_LABELS = {
    "CONS": "КОНСУЛЬТАНТ",
    "KOORD": "КООРДИНАТОР",
    "ARCH": "АРХИВАРИУС",
    "KODER": "КОДЕР",
    "VN": "ВХОДНОЙ НАСТАВНИК",
    "SHKOLA": "ШКОЛА",
    "SYS": "СИСАДМИН",
    "RED": "РЕДАКТОР",
    "KANC": "КАНЦЕЛЯРИЯ",
    "OPR": "ОПЕРАТОР",
}

def now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S")

def stamp() -> str:
    return time.strftime("%Y%m%d-%H%M%S")

def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))

def save_json(path: Path, data: dict[str, Any]):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s or "").strip().lower()

def detect_existing_completion(task: dict[str, Any]) -> str | None:
    title = norm(task.get("title", ""))
    expected = norm(task.get("expected_output", ""))
    # The demo creates a task to install the core after it was just installed.
    if "установить минимальный topic-to-task core" in title or "log16-topic-to-task-core-v01 working prototype" in expected:
        if (ROOT / "bin" / "log16-topic-to-task-core.py").exists():
            return "already_done_core_installed"
    return None

def triage_task(path: Path) -> dict[str, Any]:
    task = load_json(path)
    title = task.get("title", "")
    target = task.get("target_entity", "UNKNOWN")
    risk = task.get("risk_level", "low")
    expected = task.get("expected_output", "")
    done_criteria = task.get("done_criteria", [])
    source_theme_key = task.get("source_theme_key", "")

    completion = detect_existing_completion(task)
    if completion:
        decision = "mark_done_or_superseded"
        reason = "Задача уже выполнена текущим install/run: core установлен, повторять не надо."
        route_action = "do_not_route"
    elif not expected or not done_criteria or target == "UNKNOWN":
        decision = "reject_or_rewrite"
        reason = "Задача неполная: нет expected_output, done_criteria или target_entity."
        route_action = "do_not_route"
    elif risk in ["high", "critical"]:
        decision = "needs_operator_decision"
        reason = "Высокий риск: задача не должна уходить автоматически."
        route_action = "operator_review"
    else:
        decision = "route_candidate"
        reason = "Задача имеет адресата, результат и критерии готовности."
        route_action = "route_to_entity"

    return {
        "path": str(path),
        "task": task,
        "decision": decision,
        "reason": reason,
        "route_action": route_action,
        "target_entity": target,
        "target_label": ENTITY_LABELS.get(target, target),
        "title": title,
        "expected_output": expected,
        "source_theme_key": source_theme_key,
        "risk_level": risk,
        "priority": task.get("priority", "normal"),
        "completion_reason": completion,
    }

def apply_decisions(items: list[dict[str, Any]]):
    for item in items:
        src = Path(item["path"])
        if not src.exists():
            continue
        data = load_json(src)
        if item["decision"] == "mark_done_or_superseded":
            data["status"] = "done"
            data["triage_status"] = "already_done"
            data["triage_reason"] = item["reason"]
            data["triaged_at"] = now()
            dst = DONE / src.name
        elif item["decision"] == "route_candidate":
            data["status"] = "routed"
            data["triage_status"] = "accepted_for_routing"
            data["triage_reason"] = item["reason"]
            data["triaged_at"] = now()
            dst = ROUTED / src.name
        elif item["decision"] == "reject_or_rewrite":
            data["status"] = "rejected"
            data["triage_status"] = "needs_rewrite"
            data["triage_reason"] = item["reason"]
            data["triaged_at"] = now()
            dst = REJECTED / src.name
        else:
            # Keep proposed for operator decision.
            continue
        save_json(dst, data)
        src.unlink()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="apply safe triage: move done/routed/rejected cards")
    args = ap.parse_args()

    for d in [PROPOSED, ROUTED, DONE, REJECTED, ARCHIVED, RUNS]:
        d.mkdir(parents=True, exist_ok=True)

    run_id = f"triage__{stamp()}"
    run_dir = RUNS / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    paths = sorted(PROPOSED.glob("*.json"))
    items = [triage_task(p) for p in paths]

    if args.apply:
        apply_decisions(items)

    counts: dict[str, int] = {}
    for i in items:
        counts[i["decision"]] = counts.get(i["decision"], 0) + 1

    summary_lines = []
    summary_lines.append("# topic-task triage summary\n")
    summary_lines.append(f"Created: {now()}\n")
    summary_lines.append(f"Mode: {'APPLY' if args.apply else 'REPORT_ONLY'}\n")
    summary_lines.append(f"Proposed tasks inspected: {len(items)}\n")
    summary_lines.append("## Counts\n")
    for k in sorted(counts):
        summary_lines.append(f"- {k}: {counts[k]}")
    summary_lines.append("\n## Decisions\n")
    for item in items:
        summary_lines.append(f"\n### {item['title']}\n")
        summary_lines.append(f"- target: {item['target_label']} / {item['target_entity']}")
        summary_lines.append(f"- source_theme: {item['source_theme_key']}")
        summary_lines.append(f"- expected: {item['expected_output']}")
        summary_lines.append(f"- risk: {item['risk_level']}")
        summary_lines.append(f"- priority: {item['priority']}")
        summary_lines.append(f"- decision: {item['decision']}")
        summary_lines.append(f"- reason: {item['reason']}")
        summary_lines.append(f"- card: {item['path']}")
    summary_lines.append("\n## Human next action\n")
    if not args.apply:
        summary_lines.append("1. Проверить этот triage-summary.md.")
        summary_lines.append("2. Если решения нормальные, запустить triage с --apply.")
        summary_lines.append("3. После apply передать routed cards в dispatch/runner.")
    else:
        summary_lines.append("1. Проверить routed/done/rejected каталоги.")
        summary_lines.append("2. Передать routed tasks в следующий routing слой.")
        summary_lines.append("3. Не трогать задачи, оставшиеся proposed, без решения ОПЕРАТОРА.")
    summary_lines.append("\nКТО: КОНСУЛЬТАНТ / log16-topic-task-triage.py")
    summary_lines.append("ДЛЯ ЧЕГО: triage proposed tasks из topic-to-task")
    summary_lines.append("СТАТУС: generated\n")

    summary_path = run_dir / "triage-summary.md"
    summary_path.write_text("\n".join(summary_lines), encoding="utf-8")

    routing_lines = []
    routing_lines.append("# task-routing-queue\n")
    routing_lines.append("Кандидаты на передачу Сущностям после triage.\n")
    for item in items:
        if item["decision"] == "route_candidate":
            routing_lines.append(f"\n## {item['target_label']}\n")
            routing_lines.append(f"- title: {item['title']}")
            routing_lines.append(f"- expected_output: {item['expected_output']}")
            routing_lines.append(f"- card: {item['path']}")
            routing_lines.append(f"- action: передать адресной Сущности / runner")
    routing_lines.append("\nКТО: КОНСУЛЬТАНТ / log16-topic-task-triage.py")
    routing_lines.append("ДЛЯ ЧЕГО: очередь маршрутизации задач после triage")
    routing_lines.append("СТАТУС: generated\n")
    routing_path = run_dir / "task-routing-queue.md"
    routing_path.write_text("\n".join(routing_lines), encoding="utf-8")

    operator_lines = []
    operator_lines.append("# operator-decision-list\n")
    operator_lines.append("Задачи, где нужно решение ОПЕРАТОРА или ручная проверка.\n")
    for item in items:
        if item["decision"] in ["needs_operator_decision", "reject_or_rewrite", "mark_done_or_superseded"]:
            operator_lines.append(f"\n## {item['title']}\n")
            operator_lines.append(f"- decision: {item['decision']}")
            operator_lines.append(f"- reason: {item['reason']}")
            operator_lines.append(f"- card: {item['path']}")
    operator_lines.append("\nКТО: КОНСУЛЬТАНТ / log16-topic-task-triage.py")
    operator_lines.append("ДЛЯ ЧЕГО: список решений ОПЕРАТОРА по proposed tasks")
    operator_lines.append("СТАТУС: generated\n")
    operator_path = run_dir / "operator-decision-list.md"
    operator_path.write_text("\n".join(operator_lines), encoding="utf-8")

    manifest = {
        "run_id": run_id,
        "mode": "apply" if args.apply else "report_only",
        "tasks_inspected": len(items),
        "counts": counts,
        "summary": str(summary_path),
        "routing_queue": str(routing_path),
        "operator_decision_list": str(operator_path),
        "status": "PASS",
        "created_at": now()
    }
    save_json(run_dir / "manifest.json", manifest)

    archive = OUTBOX / f"CONS__topic-task-triage-{stamp()}__OPR.tgz"
    with tarfile.open(archive, "w:gz") as tar:
        for p in sorted(run_dir.rglob("*")):
            tar.add(p, arcname=f"CONS__topic-task-triage__OPR/{p.relative_to(run_dir)}")

    print("PASS topic-task triage completed")
    print(f"MODE: {'APPLY' if args.apply else 'REPORT_ONLY'}")
    print(f"TASKS_INSPECTED: {len(items)}")
    for k in sorted(counts):
        print(f"{k.upper()}: {counts[k]}")
    print(f"SUMMARY: {summary_path}")
    print(f"ROUTING_QUEUE: {routing_path}")
    print(f"OPERATOR_DECISIONS: {operator_path}")
    print(f"ARCHIVE: {archive}")

if __name__ == "__main__":
    main()
