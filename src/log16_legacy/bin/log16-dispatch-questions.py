#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import tarfile
import time
from pathlib import Path
from typing import Any

ROOT = Path("/data/wellbeing/obs/log16")
OUTBOX = Path("/data/wellbeing/obs/consultant/outbox")

ENTITY_LABELS = {
    "OPR": "ОПЕРАТОР",
    "KOORD": "КООРДИНАТОР",
    "VN": "ВХОДНОЙ НАСТАВНИК",
    "SHKOLA": "ШКОЛА",
    "CONS": "КОНСУЛЬТАНТ",
    "ARCH": "АРХИВАРИУС",
    "KANC": "КАНЦЕЛЯРИЯ",
    "RED": "РЕДАКТОР",
    "SHTAB": "ШТАБИСТ",
    "SYS": "СИСАДМИН",
    "KODER": "КОДЕР",
    "SHARD": "ШАРДОВИК",
}

def read_json(p: Path) -> dict[str, Any]:
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        return {"_error": str(e), "_path": str(p)}

def get(obj: Any, *keys: str) -> str:
    if isinstance(obj, dict):
        for k in keys:
            v = obj.get(k)
            if v not in (None, ""):
                return str(v)
        for v in obj.values():
            if isinstance(v, dict):
                found = get(v, *keys)
                if found:
                    return found
    return ""

def text_of(obj: Any) -> str:
    try:
        return json.dumps(obj, ensure_ascii=False, sort_keys=True)
    except Exception:
        return str(obj)

def detect_pattern(path: Path, obj: dict[str, Any]) -> str:
    text = (str(path) + " " + text_of(obj)).lower()
    for p in [
        "participant_pathway",
        "participant-pathway",
        "problem_field_map",
        "status_report",
        "research_digest",
        "routing_decision",
        "next_action_plan",
        "source_review",
    ]:
        if p in text:
            return p.replace("-", "_")
    return get(obj, "answer_pattern", "pattern", "intent") or "unknown"

def task_status(path: Path, obj: dict[str, Any]) -> str:
    return path.parent.name if path.parent.name else (get(obj, "status", "state") or "unknown")

def normalize_spaces(s: str) -> str:
    return re.sub(r"\s+", " ", s or "").strip()

def collect_cards(pattern_filter: str | None = None) -> list[dict[str, Any]]:
    task_paths = sorted((ROOT / "tasks" / "proposed").glob("*.json"))
    gap_paths = sorted((ROOT / "gaps" / "detected").glob("*.json"))

    cards: list[dict[str, Any]] = []

    for p in task_paths:
        obj = read_json(p)
        pattern = detect_pattern(p, obj)
        if pattern_filter and pattern_filter not in pattern:
            continue
        question = get(obj, "question", "source_question", "user_question", "question_original")
        reason = get(obj, "reason", "gap_reason", "why")
        expected = get(obj, "expected_output", "expected_result", "output")
        title = get(obj, "title", "task_title", "summary") or p.stem
        cards.append({
            "kind": "task",
            "path": str(p),
            "pattern": pattern,
            "status": task_status(p, obj),
            "title": normalize_spaces(title),
            "question": normalize_spaces(question),
            "reason": normalize_spaces(reason),
            "expected_output": normalize_spaces(expected),
        })

    for p in gap_paths:
        obj = read_json(p)
        pattern = detect_pattern(p, obj)
        if pattern_filter and pattern_filter not in pattern:
            continue
        question = get(obj, "question", "source_question", "user_question", "question_original")
        reason = get(obj, "reason", "gap_reason", "why")
        expected = get(obj, "expected_output", "expected_result", "output")
        title = get(obj, "title", "gap_title", "summary") or p.stem
        cards.append({
            "kind": "gap",
            "path": str(p),
            "pattern": pattern,
            "status": task_status(p, obj),
            "title": normalize_spaces(title),
            "question": normalize_spaces(question),
            "reason": normalize_spaces(reason),
            "expected_output": normalize_spaces(expected),
        })

    # Deduplicate by pattern+expected+question+kind/title enough for now.
    seen = set()
    uniq = []
    for c in cards:
        key = (
            c.get("kind"),
            c.get("pattern"),
            c.get("question"),
            c.get("expected_output"),
            c.get("title"),
        )
        if key in seen:
            continue
        seen.add(key)
        uniq.append(c)
    return uniq

def route_entities(card: dict[str, Any]) -> list[str]:
    pattern = card.get("pattern", "")
    text = " ".join([
        pattern,
        card.get("question", ""),
        card.get("reason", ""),
        card.get("expected_output", ""),
        card.get("title", ""),
    ]).lower()

    if "participant_pathway" in text or "participant-pathway" in text or "участник" in text or "поле деятельности" in text:
        return ["KOORD", "VN", "SHKOLA", "CONS"]

    if "источник" in text or "source" in text or "evidence" in text:
        return ["ARCH", "CONS"]

    if "публикац" in text or "редактор" in text or "текст" in text:
        return ["RED", "KOORD", "CONS"]

    if "сервер" in text or "vds" in text or "инфраструкт" in text:
        return ["SYS", "KOORD", "CONS"]

    if "канон" in text or "регламент" in text or "прав" in text:
        return ["KOORD", "KANC", "CONS"]

    return ["KOORD", "CONS"]

def entity_question(entity: str, card: dict[str, Any]) -> str:
    label = ENTITY_LABELS.get(entity, entity)
    pattern = card.get("pattern", "unknown")
    expected = card.get("expected_output") or "краткий ответ / решение / следующий проверяемый артефакт"
    source_question = card.get("question") or "не указан"
    reason = card.get("reason") or "не указан"
    title = card.get("title") or "задача log16"

    if pattern == "participant_pathway":
        base = f"""# Вопрос для {label}: participant_pathway

Кратко:
нужно помочь закрыть пробел по маршруту нового участника проекта.

Исходный вопрос:
{source_question}

Почему вопрос возник:
{reason}

Ожидаемый результат:
{expected}

Просьба к {label}:
1. Сформулировать свою часть ответа: как участник должен находить своё поле деятельности.
2. Указать, какие решения должен принять ОПЕРАТОР/КООРДИНАТОР.
3. Указать, какие материалы или источники нужны для проверки.
4. Дать результат так, чтобы из него можно было собрать participant-pathway-canon.md.

Минимальный формат ответа:
- краткий вывод;
- маршрут участника;
- первичная диагностика;
- первая задача;
- критерии закрепления в контуре;
- что ещё не решено.

Связанный log16 pattern:
{pattern}

Связанная карточка:
{card.get("path")}

КТО: КОНСУЛЬТАНТ
ДЛЯ ЧЕГО: вопрос Сущности для закрытия пробела log16
СТАТУС: draft_for_entity
"""
        return base

    return f"""# Вопрос для {label}: {title}

Исходный вопрос:
{source_question}

Почему вопрос возник:
{reason}

Ожидаемый результат:
{expected}

Просьба к {label}:
1. Дать ответ по своей зоне ответственности.
2. Указать недостающие вводные.
3. Указать, кому дальше передать вопрос.
4. Предложить следующий проверяемый артефакт.

Связанный log16 pattern:
{pattern}

Связанная карточка:
{card.get("path")}

КТО: КОНСУЛЬТАНТ
ДЛЯ ЧЕГО: вопрос Сущности для закрытия пробела log16
СТАТУС: draft_for_entity
"""

def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pattern", default=None, help="filter pattern, e.g. participant_pathway")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    stamp = time.strftime("%Y%m%d-%H%M%S")
    run_dir = OUTBOX / f"log16-question-dispatch-{stamp}"
    docs = run_dir / "entity-questions"
    run_dir.mkdir(parents=True, exist_ok=True)
    docs.mkdir(parents=True, exist_ok=True)

    cards = collect_cards(args.pattern)
    dispatch_rows = []

    for card in cards:
        entities = route_entities(card)
        for ent in entities:
            dispatch_rows.append((ent, card))

    # Operator brief.
    lines = []
    lines.append("# log16 dispatch brief\n")
    lines.append("Короткий смысл:\n")
    lines.append("ОПЕРАТОРу не нужно читать все карточки log16. Ниже — кому какие вопросы отдать.\n")
    lines.append("\n## Сводка\n")
    lines.append(f"- Найдено карточек задач/пробелов: {len(cards)}")
    lines.append(f"- Создано адресных вопросов: {len(dispatch_rows)}")
    if args.pattern:
        lines.append(f"- Pattern filter: {args.pattern}")
    lines.append("\n## Что делать ОПЕРАТОРУ\n")
    lines.append("1. Взять файлы из `entity-questions/`.\n")
    lines.append("2. Загрузить каждый файл в чат указанной Сущности.\n")
    lines.append("3. Ответы Сущностей вернуть в log16 через следующий цикл review/import.\n")
    lines.append("\n## Очередь загрузки\n")
    for ent, card in dispatch_rows:
        label = ENTITY_LABELS.get(ent, ent)
        fname = f"CONS__log16-question-{card.get('pattern','unknown')}-{ent}__{ent}.md"
        lines.append(f"- {label}: `{fname}`")
    lines.append("\nКТО: КОНСУЛЬТАНТ\nДЛЯ ЧЕГО: краткая очередь вопросов из log16 для раздачи Сущностям\nСТАТУС: generated\n")
    write(run_dir / "operator-brief.md", "\n".join(lines))

    upload_lines = []
    upload_lines.append("# Chat upload queue\n")
    upload_lines.append("Эти файлы нужно загрузить в чаты адресных Сущностей. Inbox каталога не считать конечной доставкой.\n")
    for ent, card in dispatch_rows:
        label = ENTITY_LABELS.get(ent, ent)
        fname = f"CONS__log16-question-{card.get('pattern','unknown')}-{ent}__{ent}.md"
        upload_lines.append(f"\n## {label}\n")
        upload_lines.append(f"- file: `entity-questions/{fname}`")
        upload_lines.append(f"- reason: {card.get('reason') or 'не указан'}")
        upload_lines.append(f"- expected: {card.get('expected_output') or 'ответ/решение'}")
    upload_lines.append("\nКТО: КОНСУЛЬТАНТ\nДЛЯ ЧЕГО: очередь фактической загрузки вопросов в чаты Сущностей\nСТАТУС: generated\n")
    write(run_dir / "chat-upload-queue.md", "\n".join(upload_lines))

    # Write entity files.
    used = {}
    for ent, card in dispatch_rows:
        base_name = f"CONS__log16-question-{card.get('pattern','unknown')}-{ent}__{ent}.md"
        n = used.get(base_name, 0)
        used[base_name] = n + 1
        if n:
            base_name = base_name.replace(".md", f"-{n+1}.md")
        write(docs / base_name, entity_question(ent, card))

    manifest = {
        "package_id": f"CONS__log16-question-dispatch-{stamp}__OPR",
        "root": str(ROOT),
        "run_dir": str(run_dir),
        "pattern_filter": args.pattern,
        "cards_count": len(cards),
        "dispatch_questions_count": len(dispatch_rows),
        "status": "PASS",
    }
    write(run_dir / "manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2))
    write(run_dir / "report.md", f"""# log16 question dispatch report

Status:
PASS

Cards found:
{len(cards)}

Entity questions:
{len(dispatch_rows)}

Run dir:
{run_dir}

Main files:
- operator-brief.md
- chat-upload-queue.md
- entity-questions/

КТО: КОНСУЛЬТАНТ
ДЛЯ ЧЕГО: отчёт о генерации вопросов из log16 для Сущностей
СТАТУС: generated
""")

    archive = OUTBOX / f"CONS__log16-question-dispatch-{stamp}__OPR.tgz"
    with tarfile.open(archive, "w:gz") as tar:
        for p in sorted(run_dir.rglob("*")):
            tar.add(p, arcname=f"CONS__log16-question-dispatch-{stamp}__OPR/{p.relative_to(run_dir)}")

    print("PASS log16 question dispatch generated")
    print(f"RUN_DIR: {run_dir}")
    print(f"ARCHIVE: {archive}")
    print(f"OPERATOR_BRIEF: {run_dir / 'operator-brief.md'}")
    print(f"UPLOAD_QUEUE: {run_dir / 'chat-upload-queue.md'}")
    print("ENTITY_QUESTIONS:")
    for p in sorted(docs.glob("*.md")):
        print(f"- {p}")

if __name__ == "__main__":
    main()
