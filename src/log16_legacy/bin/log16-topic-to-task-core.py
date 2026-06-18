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
THEMES = ROOT / "themes" / "captured"
TASKS = ROOT / "derived-tasks" / "proposed"
BATCHES = ROOT / "task-batches"
RUNS = ROOT / "topic-to-task-runs"

THEME_RULES = [
    {
        "theme_key": "topic_to_task_system",
        "title": "Система формирования задач из информационного поля проекта",
        "keywords": ["система", "накоплен", "информацион", "формирован", "новых задач", "темам", "topic-to-task", "задач"],
        "entities": ["CONS", "KOORD", "ARCH", "KODER"],
        "summary": "Развитие log16 от ответа на вопрос к системе, которая выявляет темы, пробелы и порождает новые проверяемые задачи."
    },
    {
        "theme_key": "participant_communication",
        "title": "Простая коммуникация участника с проектом",
        "keywords": ["участник", "коммуникац", "регистрац", "статус", "активац", "путь участника", "participant"],
        "entities": ["VN", "SHKOLA", "KOORD", "CONS"],
        "summary": "Контур, где участник получает понятный вход, первую безопасную задачу и маршрут включения."
    },
    {
        "theme_key": "agent_syndicate",
        "title": "Синдикат ИИ-Сущностей и автоматическая маршрутизация",
        "keywords": ["синдикат", "ииш", "runner", "сущност", "автомат", "ollama", "agent", "агент"],
        "entities": ["CONS", "KODER", "SYS", "ARCH"],
        "summary": "Автоматическая передача вопросов Сущностям, получение ответов и возврат результатов в log16."
    },
    {
        "theme_key": "review_approval_layer",
        "title": "Review и approval слой для рабочих документов",
        "keywords": ["review", "approval", "утверд", "working", "канон", "доработ", "провер"],
        "entities": ["KOORD", "CONS", "ARCH"],
        "summary": "Слой проверки, принятия и перевода документов из draft/working в approved."
    }
]

DEFAULT_TASKS = {
    "topic_to_task_system": [
        {
            "title": "Установить минимальный topic-to-task core",
            "target_entity": "KODER",
            "expected_output": "log16-topic-to-task-core-v01 working prototype",
            "reason": "Нужен первый технический цикл input_event → theme_card → derived_task_cards → task_batch.",
            "done_criteria": ["создаются theme_card", "создаются derived_task_cards", "создаётся topic-summary.md"],
            "priority": "high",
            "risk_level": "low"
        },
        {
            "title": "Описать evidence lookup для theme_case",
            "target_entity": "ARCH",
            "expected_output": "theme-evidence-lookup-v01.md",
            "reason": "Для задач по теме нужно находить уже накопленные документы, карточки и решения.",
            "done_criteria": ["описаны источники", "описан порядок поиска", "описан provenance"],
            "priority": "normal",
            "risk_level": "low"
        },
        {
            "title": "Проверить качество создаваемых задач",
            "target_entity": "CONS",
            "expected_output": "task-quality-review-v01.md",
            "reason": "Система не должна плодить мусорные задачи без результата.",
            "done_criteria": ["каждая задача имеет expected_output", "есть done_criteria", "есть target_entity"],
            "priority": "high",
            "risk_level": "low"
        },
        {
            "title": "Согласовать routing policy для новых задач",
            "target_entity": "KOORD",
            "expected_output": "topic-task-routing-policy-v01.md",
            "reason": "Нужно определить, какие типы задач уходят каким Сущностям.",
            "done_criteria": ["есть карта задач по Сущностям", "есть правила high-risk", "есть human gate"],
            "priority": "high",
            "risk_level": "medium"
        }
    ],
    "participant_communication": [
        {
            "title": "Подготовить starter tasks catalog",
            "target_entity": "VN",
            "expected_output": "starter-tasks-catalog.md",
            "reason": "Для простого входа участника нужен каталог первых безопасных задач.",
            "done_criteria": ["есть 5-10 задач", "есть формат результата", "есть критерии проверки"],
            "priority": "normal",
            "risk_level": "low"
        },
        {
            "title": "Проверить participant-pathway-canon-working-v01",
            "target_entity": "SHKOLA",
            "expected_output": "shkola-review-participant-pathway.md",
            "reason": "Нужно проверить учебно-практический маршрут и статусы trainee/trial_participant.",
            "done_criteria": ["есть замечания", "есть предложения", "есть решение accept/revise"],
            "priority": "normal",
            "risk_level": "low"
        }
    ],
    "agent_syndicate": [
        {
            "title": "Описать adapter roadmap для разных ИИ",
            "target_entity": "KODER",
            "expected_output": "agent-adapter-roadmap-v01.md",
            "reason": "Нужно понять, как подключать Ollama, OpenAI API и будущие внешние агентные системы.",
            "done_criteria": ["описаны adapters", "описаны ограничения", "есть порядок внедрения"],
            "priority": "normal",
            "risk_level": "medium"
        }
    ],
    "review_approval_layer": [
        {
            "title": "Спроектировать review/approval layer для log16",
            "target_entity": "CONS",
            "expected_output": "log16-review-approval-layer-v01.md",
            "reason": "Нужно переводить документы из draft/working в reviewed/approved без ручного хаоса.",
            "done_criteria": ["описаны статусы", "описаны действия", "описаны роли"],
            "priority": "high",
            "risk_level": "medium"
        }
    ]
}

def now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S")

def safe_stamp() -> str:
    return time.strftime("%Y%m%d-%H%M%S")

def slug(s: str) -> str:
    s = s.lower().replace("ё", "е")
    s = re.sub(r"[^a-z0-9а-я_-]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s[:90] or "item"

def save_json(path: Path, data: dict[str, Any]):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def detect_themes(text: str) -> list[dict[str, Any]]:
    low = text.lower()
    found = []
    for rule in THEME_RULES:
        score = 0
        for kw in rule["keywords"]:
            if kw.lower() in low:
                score += 1
        if score:
            item = dict(rule)
            item["score"] = score
            found.append(item)
    if not found:
        found.append({
            "theme_key": "general_project_development",
            "title": "Общее развитие проекта",
            "keywords": [],
            "entities": ["CONS", "KOORD"],
            "summary": "Общая тема, требующая первичного анализа КОНСУЛЬТАНТОМ и КООРДИНАТОРОМ.",
            "score": 0
        })
    return sorted(found, key=lambda x: x["score"], reverse=True)

def tasks_for_theme(theme_key: str, source_event: str) -> list[dict[str, Any]]:
    base = DEFAULT_TASKS.get(theme_key)
    if base:
        return [dict(t) for t in base]
    return [
        {
            "title": "Провести первичный анализ темы",
            "target_entity": "CONS",
            "expected_output": f"{theme_key}-analysis-v01.md",
            "reason": "Для новой темы нужно понять смысл, пробелы и следующие задачи.",
            "done_criteria": ["есть краткий вывод", "есть пробелы", "есть предложения задач"],
            "priority": "normal",
            "risk_level": "low"
        },
        {
            "title": "Определить маршрут темы",
            "target_entity": "KOORD",
            "expected_output": f"{theme_key}-routing-v01.md",
            "reason": "Нужно определить ответственных Сущностей и порядок работы.",
            "done_criteria": ["есть адресаты", "есть порядок передачи", "есть критерии завершения"],
            "priority": "normal",
            "risk_level": "low"
        }
    ]

def generate(text: str, source_label: str = "manual"):
    for d in [THEMES, TASKS, BATCHES, RUNS]:
        d.mkdir(parents=True, exist_ok=True)

    stamp = safe_stamp()
    run_dir = RUNS / f"topic-to-task-{stamp}"
    run_dir.mkdir(parents=True, exist_ok=True)

    themes = detect_themes(text)
    created_themes = []
    created_tasks = []
    batches = []

    for theme in themes:
        theme_id = f"theme__{stamp}__{theme['theme_key']}"
        theme_card = {
            "theme_id": theme_id,
            "theme_key": theme["theme_key"],
            "title": theme["title"],
            "source_event": text,
            "source_label": source_label,
            "summary": theme["summary"],
            "related_entities": theme["entities"],
            "related_sources": [],
            "score": theme.get("score", 0),
            "status": "captured",
            "created_at": now(),
            "created_by": "CONSULTANT/log16-topic-to-task-core.py"
        }
        theme_path = THEMES / f"{theme_id}.json"
        save_json(theme_path, theme_card)
        created_themes.append(theme_path)

        task_paths = []
        for task in tasks_for_theme(theme["theme_key"], text):
            task_id = f"task__{stamp}__{theme['theme_key']}__{slug(task['title'])}"
            card = {
                "task_id": task_id,
                "title": task["title"],
                "source_theme": theme_id,
                "source_theme_key": theme["theme_key"],
                "source_event": text,
                "target_entity": task["target_entity"],
                "expected_output": task["expected_output"],
                "reason": task["reason"],
                "done_criteria": task["done_criteria"],
                "priority": task["priority"],
                "risk_level": task["risk_level"],
                "status": "proposed",
                "created_at": now(),
                "created_by": "CONSULTANT/log16-topic-to-task-core.py"
            }
            task_path = TASKS / f"{task_id}.json"
            save_json(task_path, card)
            created_tasks.append(task_path)
            task_paths.append(str(task_path))

        batch_id = f"batch__{stamp}__{theme['theme_key']}"
        batch = {
            "batch_id": batch_id,
            "source_theme": theme_id,
            "source_theme_key": theme["theme_key"],
            "tasks": task_paths,
            "operator_summary": f"Создан пакет задач по теме: {theme['title']}",
            "status": "proposed",
            "created_at": now(),
            "created_by": "CONSULTANT/log16-topic-to-task-core.py"
        }
        batch_path = BATCHES / f"{batch_id}.json"
        save_json(batch_path, batch)
        batches.append(batch_path)

    summary = []
    summary.append("# topic-to-task summary\n")
    summary.append(f"Created: {now()}\n")
    summary.append(f"Source label: {source_label}\n")
    summary.append("## Input event\n")
    summary.append(text + "\n")
    summary.append("## Themes\n")
    for p in created_themes:
        data = json.loads(p.read_text(encoding="utf-8"))
        summary.append(f"- {data['theme_key']}: {data['title']} (score={data.get('score')})")
        summary.append(f"  - card: {p}")
    summary.append("\n## Derived tasks\n")
    for p in created_tasks:
        data = json.loads(p.read_text(encoding="utf-8"))
        summary.append(f"- [{data['target_entity']}] {data['title']}")
        summary.append(f"  - expected: {data['expected_output']}")
        summary.append(f"  - risk: {data['risk_level']}, priority: {data['priority']}")
        summary.append(f"  - card: {p}")
    summary.append("\n## Task batches\n")
    for p in batches:
        summary.append(f"- {p}")
    summary.append("\n## Human next action\n")
    summary.append("1. Открыть этот topic-summary.md.")
    summary.append("2. Проверить, не создан ли мусор.")
    summary.append("3. Принять/отклонить proposed tasks.")
    summary.append("4. Передать нормальные задачи в routing/runner.")
    summary.append("\nКТО: КОНСУЛЬТАНТ / log16-topic-to-task-core.py")
    summary.append("ДЛЯ ЧЕГО: summary формирования задач из input_event")
    summary.append("СТАТУС: generated\n")

    summary_path = run_dir / "topic-summary.md"
    summary_path.write_text("\n".join(summary), encoding="utf-8")

    manifest = {
        "run_id": f"topic-to-task-{stamp}",
        "input_event": text,
        "themes_created": [str(p) for p in created_themes],
        "tasks_created": [str(p) for p in created_tasks],
        "batches_created": [str(p) for p in batches],
        "summary": str(summary_path),
        "status": "PASS",
        "created_at": now()
    }
    save_json(run_dir / "manifest.json", manifest)

    archive = OUTBOX / f"CONS__topic-to-task-run-{stamp}__OPR.tgz"
    with tarfile.open(archive, "w:gz") as tar:
        for p in sorted(run_dir.rglob("*")):
            tar.add(p, arcname=f"CONS__topic-to-task-run-{stamp}__OPR/{p.relative_to(run_dir)}")
        for p in created_themes + created_tasks + batches:
            tar.add(p, arcname=f"CONS__topic-to-task-run-{stamp}__OPR/cards/{p.name}")

    print("PASS topic-to-task generated")
    print(f"THEMES_CREATED: {len(created_themes)}")
    print(f"TASKS_CREATED: {len(created_tasks)}")
    print(f"BATCHES_CREATED: {len(batches)}")
    print(f"SUMMARY: {summary_path}")
    print(f"ARCHIVE: {archive}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", default=None, help="input event text")
    ap.add_argument("--file", default=None, help="path to text file")
    ap.add_argument("--source-label", default="manual")
    args = ap.parse_args()

    text = args.text
    if args.file:
        text = Path(args.file).read_text(encoding="utf-8")
    if not text:
        raise SystemExit("ERROR: provide --text or --file")

    generate(text, args.source_label)

if __name__ == "__main__":
    main()
