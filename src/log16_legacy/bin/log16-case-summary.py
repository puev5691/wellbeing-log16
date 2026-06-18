#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path
from datetime import datetime

ROOT = Path("/data/wellbeing/obs/log16")

def load_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        return {"_load_error": str(e), "_raw_text": path.read_text(encoding="utf-8", errors="replace")[:4000]}

def all_cards():
    groups = {
        "answers": list((ROOT / "answers").glob("*/*.json")),
        "gaps": list((ROOT / "gaps").glob("*/*.json")),
        "tasks": list((ROOT / "tasks").glob("*/*.json")),
        "reviews": list((ROOT / "reviews").glob("*.json")),
        "reports": list((ROOT / "reports").glob("*.md")),
    }
    return groups

def stringify(obj):
    try:
        return json.dumps(obj, ensure_ascii=False, sort_keys=True)
    except Exception:
        return str(obj)

def norm(s):
    return re.sub(r"\s+", " ", str(s or "").lower()).strip()

def extract(obj, *keys):
    if not isinstance(obj, dict):
        return ""
    for k in keys:
        if k in obj and obj[k] not in (None, ""):
            return obj[k]
    # shallow nested fallback
    for v in obj.values():
        if isinstance(v, dict):
            for k in keys:
                if k in v and v[k] not in (None, ""):
                    return v[k]
    return ""

def card_pattern(path, obj):
    candidates = [
        extract(obj, "answer_pattern", "pattern", "answer_intent", "intent"),
        path.stem,
        path.name,
    ]
    text = " ".join(map(str, candidates))
    for p in [
        "participant_pathway",
        "problem_field_map",
        "status_report",
        "research_digest",
        "routing_decision",
        "next_action_plan",
        "source_review",
        "entity_setup_report",
        "concept_reconstruction_note",
    ]:
        if p in text:
            return p
    return str(candidates[0] or "unknown")

def card_question(obj):
    return extract(obj, "question_original", "question", "question_normalized", "source_question", "user_question")

def card_status(path, obj):
    if len(path.parts) >= 2:
        parent = path.parent.name
        if parent in ["draft", "needs_review", "approved", "deprecated", "detected", "routed", "resolved", "proposed", "done"]:
            return parent
    return str(extract(obj, "status", "review_status", "state") or "unknown")

def card_title(path, obj):
    return str(extract(obj, "title", "task_title", "gap_title", "summary") or path.name)

def card_reason(obj):
    return str(extract(obj, "reason", "why", "gap_reason", "review_reason", "operator_feedback") or "")

def card_expected(obj):
    return str(extract(obj, "expected_output", "expected_result", "next_action", "output") or "")

def matches(path, obj, pattern=None, query=None):
    text = norm(str(path) + " " + stringify(obj))
    if pattern and pattern.lower() not in text:
        return False
    if query:
        q = norm(query)
        tokens = [t for t in re.split(r"\W+", q) if len(t) >= 4]
        if not tokens:
            return q in text
        score = sum(1 for t in tokens if t in text)
        return score >= max(1, min(3, len(tokens)//3))
    return True

def latest(paths):
    paths = [p for p in paths if p.exists()]
    if not paths:
        return None
    return max(paths, key=lambda p: p.stat().st_mtime)

def summarize(pattern=None, query=None):
    groups = all_cards()
    loaded = {}
    for group, paths in groups.items():
        if group == "reports":
            continue
        rows = []
        for p in paths:
            obj = load_json(p)
            if matches(p, obj, pattern, query):
                rows.append((p, obj))
        loaded[group] = rows

    report_rows = []
    for p in groups["reports"]:
        text = p.read_text(encoding="utf-8", errors="replace")
        fake = {"text": text, "path": str(p)}
        if matches(p, fake, pattern, query):
            report_rows.append(p)

    print("LOG16 CASE SUMMARY")
    print(f"root: {ROOT}")
    if pattern:
        print(f"pattern filter: {pattern}")
    if query:
        print(f"query filter: {query}")
    print()

    print("counts:")
    for group in ["answers", "gaps", "tasks", "reviews"]:
        print(f"  {group}: {len(loaded.get(group, []))}")
    print(f"  reports: {len(report_rows)}")
    print()

    # High-level diagnosis
    answer_statuses = {}
    for p, obj in loaded.get("answers", []):
        answer_statuses[card_status(p, obj)] = answer_statuses.get(card_status(p, obj), 0) + 1
    gap_count = len(loaded.get("gaps", []))
    task_count = len(loaded.get("tasks", []))
    approved = answer_statuses.get("approved", 0)
    needs = answer_statuses.get("needs_review", 0)

    print("diagnosis:")
    if approved:
        print("  Есть approved answer: можно использовать быстрый ответ, если он не устарел.")
    elif needs:
        print("  Есть answer_card в needs_review: ответ есть, но он ещё не утверждён.")
    else:
        print("  Нет answer_card по фильтру: сначала нужен run/import или ручной seed.")

    if gap_count and task_count:
        print("  Есть gap_card и task_card: система выявила пробел и уже поставила задачу.")
    elif gap_count and not task_count:
        print("  Есть gap_card, но нет task_card: пробел найден, задача не оформлена.")
    elif not gap_count and needs:
        print("  Gap не создан: importer считает, что явного пробела нет, но answer всё ещё needs_review.")
    else:
        print("  Gap не найден по фильтру.")
    print()

    def print_rows(title, rows, limit=6):
        print(title)
        if not rows:
            print("  none")
            print()
            return
        for p, obj in sorted(rows, key=lambda x: x[0].stat().st_mtime, reverse=True)[:limit]:
            pat = card_pattern(p, obj)
            st = card_status(p, obj)
            q = card_question(obj)
            ttl = card_title(p, obj)
            reason = card_reason(obj)
            expected = card_expected(obj)
            print(f"  - file: {p}")
            print(f"    pattern: {pat}")
            print(f"    status: {st}")
            if q:
                print(f"    question: {q}")
            if ttl and ttl != p.name:
                print(f"    title: {ttl}")
            if reason:
                print(f"    reason: {reason[:500]}")
            if expected:
                print(f"    expected_output: {expected[:500]}")
        print()

    print_rows("answers:", loaded.get("answers", []))
    print_rows("gaps:", loaded.get("gaps", []))
    print_rows("tasks:", loaded.get("tasks", []))
    print_rows("reviews:", loaded.get("reviews", []))

    print("reports:")
    if not report_rows:
        print("  none")
    else:
        for p in sorted(report_rows, key=lambda x: x.stat().st_mtime, reverse=True)[:6]:
            print(f"  - {p}")
    print()

    print("human next action:")
    if approved:
        print("  1. Проверить срок применимости approved answer.")
        print("  2. Добавить его в fast_response_cache, если ещё не добавлен.")
    elif gap_count and task_count:
        print("  1. Открыть latest task_card.")
        print("  2. Выполнить expected_output.")
        print("  3. После нового документа сделать review и обновить answer_card.")
    elif needs:
        print("  1. Открыть latest answer_card и review_card.")
        print("  2. Решить: принять, отправить на доработку или создать gap/task.")
    else:
        print("  1. Запустить v05.2 run и импортировать его в log16.")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pattern", default=None, help="answer pattern, e.g. participant_pathway")
    ap.add_argument("--query", default=None, help="question or keywords")
    args = ap.parse_args()
    summarize(args.pattern, args.query)

if __name__ == "__main__":
    main()
