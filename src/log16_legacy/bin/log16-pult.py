#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import tarfile
import time
from pathlib import Path
from typing import Any

ROOT = Path("/data/wellbeing/obs/log16")
OUTBOX = Path("/data/wellbeing/obs/consultant/outbox")
BIN = ROOT / "bin"
PULT_RUNS = ROOT / "pult-runs"

DIRS = {
    "themes_captured": ROOT / "themes" / "captured",
    "tasks_proposed": ROOT / "derived-tasks" / "proposed",
    "tasks_routed": ROOT / "derived-tasks" / "routed",
    "tasks_dispatched": ROOT / "derived-tasks" / "dispatched",
    "tasks_done": ROOT / "derived-tasks" / "done",
    "requests_pending": ROOT / "entity-requests" / "pending",
    "requests_done": ROOT / "entity-requests" / "done",
    "requests_failed": ROOT / "entity-requests" / "failed",
    "responses_needs_review": ROOT / "entity-responses" / "needs_review",
    "responses_failed": ROOT / "entity-responses" / "failed",
    "runner_reports": ROOT / "runner-reports",
}

REGISTRY = ROOT / "entity-registry" / "entity-registry.json"

def now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S")

def stamp() -> str:
    return time.strftime("%Y%m%d-%H%M%S")

def ensure_dirs():
    for d in DIRS.values():
        d.mkdir(parents=True, exist_ok=True)
    PULT_RUNS.mkdir(parents=True, exist_ok=True)

def count_json(path: Path) -> int:
    return len(list(path.glob("*.json"))) if path.exists() else 0

def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))

def save_json(path: Path, data: dict[str, Any]):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def run_cmd(cmd: list[str], log_path: Path) -> tuple[int, str]:
    p = subprocess.run(cmd, text=True, capture_output=True)
    out = "$ " + " ".join(cmd) + "\n\n"
    out += "STDOUT:\n" + p.stdout + "\n\n"
    out += "STDERR:\n" + p.stderr + "\n"
    write(log_path, out)
    return p.returncode, out

def make_run_dir(prefix: str) -> Path:
    run_dir = PULT_RUNS / f"{prefix}-{stamp()}"
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir

def archive_run(run_dir: Path, archive_prefix: str) -> Path:
    archive = OUTBOX / f"CONS__{archive_prefix}-{stamp()}__OPR.tgz"
    with tarfile.open(archive, "w:gz") as tar:
        for p in sorted(run_dir.rglob("*")):
            tar.add(p, arcname=f"CONS__{archive_prefix}__OPR/{p.relative_to(run_dir)}")
    return archive

def all_cards_with_source_task_id() -> dict[str, list[str]]:
    refs: dict[str, list[str]] = {}
    search_dirs = [
        DIRS["requests_pending"],
        DIRS["requests_done"],
        DIRS["requests_failed"],
        DIRS["responses_needs_review"],
        DIRS["responses_failed"],
    ]
    for d in search_dirs:
        for p in sorted(d.glob("*.json")):
            try:
                data = load_json(p)
            except Exception:
                continue
            sid = data.get("source_task_id")
            if sid:
                refs.setdefault(str(sid), []).append(str(p))
    return refs

def cleanup_stale_routed(apply: bool = True) -> tuple[int, list[str]]:
    ensure_dirs()
    refs = all_cards_with_source_task_id()
    moved = 0
    notes = []
    for p in sorted(DIRS["tasks_routed"].glob("*.json")):
        try:
            data = load_json(p)
        except Exception as e:
            notes.append(f"skip unreadable {p}: {e}")
            continue
        task_id = data.get("task_id")
        if task_id and str(task_id) in refs:
            notes.append(f"dispatched: {p.name} -> evidence {len(refs[str(task_id)])}")
            if apply:
                data["status"] = "dispatched"
                data["dispatch_evidence_refs"] = refs[str(task_id)]
                data["dispatch_cleanup_at"] = now()
                dst = DIRS["tasks_dispatched"] / p.name
                save_json(dst, data)
                p.unlink()
            moved += 1
    return moved, notes

def pending_cases() -> list[str]:
    cases = set()
    for p in sorted(DIRS["requests_pending"].glob("*.json")):
        try:
            case = str(load_json(p).get("source_case", "")).strip()
        except Exception:
            case = ""
        if case:
            cases.add(case)
    return sorted(cases)

def status_text(cleanup: bool = False) -> str:
    if cleanup:
        cleanup_stale_routed(apply=True)
    ensure_dirs()
    lines = []
    lines.append("# log16 pult status\n")
    lines.append(f"Created: {now()}\n")
    lines.append("## Counts\n")
    for key, path in DIRS.items():
        if key == "runner_reports":
            count = len([p for p in path.iterdir() if p.is_dir()]) if path.exists() else 0
        else:
            count = count_json(path)
        lines.append(f"- {key}: {count}")
    lines.append("\n## Pending source cases\n")
    cases = pending_cases()
    if cases:
        for c in cases:
            n = 0
            for p in DIRS["requests_pending"].glob("*.json"):
                try:
                    if load_json(p).get("source_case") == c:
                        n += 1
                except Exception:
                    pass
            lines.append(f"- {c}: {n}")
    else:
        lines.append("- none")
    lines.append("\n## Meaning\n")
    lines.append("- tasks_proposed: задачи ещё не разобраны triage.")
    lines.append("- tasks_routed: задачи ждут dispatch; если они уже отработаны, запусти cleanup.")
    lines.append("- tasks_dispatched: задачи уже превратились в requests/responses.")
    lines.append("- requests_pending: есть что запускать runner.")
    lines.append("- responses_needs_review: есть ответы Сущностей, требующие review.")
    lines.append("\n## Latest runner reports\n")
    reps = sorted(DIRS["runner_reports"].glob("*/runner-summary.md"), key=lambda p: p.stat().st_mtime, reverse=True)[:5]
    if reps:
        for r in reps:
            lines.append(f"- {r}")
    else:
        lines.append("- none")
    return "\n".join(lines) + "\n"

def dirty_counts() -> dict[str, int]:
    cleanup_stale_routed(apply=True)
    return {
        "proposed": count_json(DIRS["tasks_proposed"]),
        "routed": count_json(DIRS["tasks_routed"]),
        "pending": count_json(DIRS["requests_pending"]),
    }

def cmd_status(args):
    print(status_text(cleanup=args.cleanup))

def cmd_cleanup(args):
    run_dir = make_run_dir("cleanup")
    moved, notes = cleanup_stale_routed(apply=True)
    lines = []
    lines.append("# log16 pult cleanup\n")
    lines.append(f"Created: {now()}\n")
    lines.append(f"Moved routed -> dispatched: {moved}\n")
    lines.append("## Notes\n")
    for n in notes:
        lines.append(f"- {n}")
    lines.append("\n## Status after cleanup\n")
    lines.append(status_text(cleanup=False))
    summary = run_dir / "cleanup-summary.md"
    write(summary, "\n".join(lines))
    archive = archive_run(run_dir, "log16-pult-cleanup")
    print("PASS log16 pult cleanup completed")
    print(f"MOVED: {moved}")
    print(f"SUMMARY: {summary}")
    print(f"ARCHIVE: {archive}")

def cmd_tasks(args):
    text = args.text
    if not text:
        raise SystemExit("ERROR: provide topic/event text: log16-pult tasks 'текст темы или события'")

    dirty = dirty_counts()
    if not args.force and any(dirty.values()):
        print("STOP: pipeline has unfinished queues.")
        print(f"proposed={dirty['proposed']} routed={dirty['routed']} pending={dirty['pending']}")
        print("Use:")
        print("  log16-pult status --cleanup")
        print("  log16-pult cleanup")
        print("  log16-pult run-pending")
        print("Or rerun tasks with --force if you intentionally want to process existing queues too.")
        return

    run_dir = make_run_dir("tasks")
    write(run_dir / "input-event.txt", text)

    steps = [
        ("01-topic-to-task.log", [str(BIN / "log16-topic-to-task.sh"), "--text", text]),
        ("02-triage-apply.log", [str(BIN / "log16-topic-task-triage.sh"), "--apply"]),
        ("03-dispatch-create.log", [str(BIN / "log16-dispatch-routed-tasks.sh"), "--create"]),
    ]

    ok = True
    for log_name, cmd in steps:
        rc, _ = run_cmd(cmd, run_dir / log_name)
        if rc != 0:
            ok = False
            break

    # After dispatch, clean routed cards that now have request/response evidence.
    moved, notes = cleanup_stale_routed(apply=True)
    write(run_dir / "04-cleanup-after-dispatch.txt", "\n".join(notes) + f"\nMOVED={moved}\n")

    if ok and not args.no_run:
        rc, _ = run_cmd([str(BIN / "log16-pult.py"), "run-pending"], run_dir / "05-run-pending.log")
        if rc != 0:
            ok = False

    summary = []
    summary.append("# log16 pult tasks summary\n")
    summary.append(f"Created: {now()}\n")
    summary.append(f"Status: {'PASS' if ok else 'FAILED'}\n")
    summary.append("## Input event\n")
    summary.append(text + "\n")
    summary.append("## Resulting status\n")
    summary.append(status_text(cleanup=True))
    summary.append("\nКТО: КОНСУЛЬТАНТ / log16-pult.py")
    summary.append("ДЛЯ ЧЕГО: one-command topic-to-task cycle")
    summary.append("СТАТУС: generated\n")
    summary_path = run_dir / "pult-tasks-summary.md"
    write(summary_path, "\n".join(summary))

    archive = archive_run(run_dir, "log16-pult-tasks")
    print("PASS log16 pult tasks completed" if ok else "WARN log16 pult tasks ended with errors")
    print(f"SUMMARY: {summary_path}")
    print(f"ARCHIVE: {archive}")

def registry_entities() -> list[dict[str, Any]]:
    if not REGISTRY.exists():
        return []
    try:
        data = load_json(REGISTRY)
    except Exception:
        return []
    return data.get("entities", [])

def direct_answer(question: str) -> str:
    q = question.lower()
    entities = registry_entities()
    if "сущност" in q and ("сколько" in q or "количество" in q):
        lines = []
        lines.append("# direct answer — entity count\n")
        lines.append("## Краткий ответ\n")
        lines.append(f"В техническом `entity-registry` сейчас зарегистрировано {len(entities)} Сущностей для runner/log16.\n")
        if entities:
            lines.append("## Entity registry\n")
            for e in entities:
                lines.append(f"- {e.get('display_name', e.get('entity_id'))} / {e.get('entity_id')} / {e.get('code', '')}")
        lines.append("\n## Важное уточнение\n")
        lines.append("Это не обязательно полное количество проектных ролей в БЛАГОПОЛУЧИИ. Это количество Сущностей, которые прямо сейчас зарегистрированы в техническом runner registry и могут получать entity_request.")
        lines.append("\nДля полного проектного списка нужен отдельный entity-inventory по источникам проекта: роли, активные чаты, отложенные Сущности, технические контуры.")
        lines.append("\n## Следующая задача\n")
        lines.append("Создать `project-entity-inventory-v01.md`, где различить:")
        lines.append("- проектные Сущности;")
        lines.append("- технически зарегистрированные runner entities;")
        lines.append("- человеческие роли;")
        lines.append("- отложенные будущие контуры.")
        return "\n".join(lines) + "\n"

    return f"""# direct answer — unsupported question type

## Краткий ответ

`log16-pult answer` v02 пока умеет уверенно отвечать только на несколько простых локальных вопросов, например по entity registry.

Вопрос:
{question}

Для этого вопроса нужен полноценный answer pipeline:
- поиск источников;
- evidence lookup;
- synthesis;
- review.

## Что сделать

Используй `log16-pult tasks "{question}"`, если цель — породить задачи по теме.

КТО: КОНСУЛЬТАНТ / log16-pult.py
ДЛЯ ЧЕГО: честный отказ direct answer v02 при нехватке answer pipeline
СТАТУС: unsupported_direct_answer_v02
"""

def cmd_answer(args):
    question = args.text
    if not question:
        raise SystemExit("ERROR: provide question: log16-pult answer 'вопрос'")
    run_dir = make_run_dir("answer")
    answer = direct_answer(question)
    answer_path = run_dir / "direct-answer.md"
    write(answer_path, answer)
    archive = archive_run(run_dir, "log16-pult-answer")
    print(answer)
    print(f"ANSWER: {answer_path}")
    print(f"ARCHIVE: {archive}")

def cmd_run_pending(args):
    run_dir = make_run_dir("run-pending")
    cases = pending_cases()

    lines = []
    lines.append("# log16 pult run-pending\n")
    lines.append(f"Created: {now()}\n")
    lines.append(f"Cases: {', '.join(cases) if cases else 'none'}\n")

    if not cases:
        summary = run_dir / "pult-run-pending-summary.md"
        write(summary, "\n".join(lines))
        archive = archive_run(run_dir, "log16-pult-run-pending")
        print("NO_PENDING_CASES")
        print(f"SUMMARY: {summary}")
        print(f"ARCHIVE: {archive}")
        return

    ok = True
    for case in cases:
        safe = case.replace("/", "_").replace(" ", "_")
        cmd = [str(BIN / "log16-agent-runner.py"), "--case", case]
        rc, out = run_cmd(cmd, run_dir / f"runner-{safe}.log")
        lines.append(f"## {case}\n")
        lines.append(f"- return_code: {rc}")
        if rc != 0:
            ok = False
        for ln in out.splitlines():
            if ln.startswith(("PASS", "WARN", "REQUESTS_SELECTED", "RESPONSES_CREATED", "FAILED", "ARCHIVE", "SUMMARY")):
                lines.append(f"- {ln}")

    cleanup_stale_routed(apply=True)
    lines.append("\n## Resulting status\n")
    lines.append(status_text(cleanup=True))
    lines.append("\nКТО: КОНСУЛЬТАНТ / log16-pult.py")
    lines.append("ДЛЯ ЧЕГО: запуск всех pending source_case через runner")
    lines.append("СТАТУС: generated\n")
    summary = run_dir / "pult-run-pending-summary.md"
    write(summary, "\n".join(lines))
    archive = archive_run(run_dir, "log16-pult-run-pending")
    print("PASS log16 pult run-pending completed" if ok else "WARN log16 pult run-pending ended with errors")
    print(f"SUMMARY: {summary}")
    print(f"ARCHIVE: {archive}")

def cmd_latest(args):
    reps = sorted(DIRS["runner_reports"].glob("*/runner-summary.md"), key=lambda p: p.stat().st_mtime, reverse=True)[: args.limit]
    if not reps:
        print("NO_RUNNER_REPORTS")
        return
    for r in reps:
        print(str(r))

def main():
    ensure_dirs()
    ap = argparse.ArgumentParser(prog="log16-pult")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_status = sub.add_parser("status")
    p_status.add_argument("--cleanup", action="store_true")
    p_status.set_defaults(func=cmd_status)

    p_cleanup = sub.add_parser("cleanup")
    p_cleanup.set_defaults(func=cmd_cleanup)

    p_tasks = sub.add_parser("tasks")
    p_tasks.add_argument("text", nargs="?", default=None)
    p_tasks.add_argument("--force", action="store_true")
    p_tasks.add_argument("--no-run", action="store_true")
    p_tasks.set_defaults(func=cmd_tasks)

    p_answer = sub.add_parser("answer")
    p_answer.add_argument("text", nargs="?", default=None)
    p_answer.set_defaults(func=cmd_answer)

    # Human expects ask to mean answer. Keep ask as alias for answer.
    p_ask = sub.add_parser("ask")
    p_ask.add_argument("text", nargs="?", default=None)
    p_ask.set_defaults(func=cmd_answer)

    p_run = sub.add_parser("run-pending")
    p_run.set_defaults(func=cmd_run_pending)

    p_latest = sub.add_parser("latest")
    p_latest.add_argument("--limit", type=int, default=5)
    p_latest.set_defaults(func=cmd_latest)

    args = ap.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
