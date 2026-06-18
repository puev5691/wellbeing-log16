#!/usr/bin/env python3
from __future__ import annotations

import json
import time
from pathlib import Path

ROOT = Path("/data/wellbeing/obs/log16")
PENDING = ROOT / "entity-requests" / "pending"

QUESTION = "Как привлекаемый участник будет находить своё поле деятельности в проекте?"
EXPECTED = "participant-pathway-canon.md"
CASE = "participant_pathway::participant-pathway-canon"

TARGETS = [
    {
        "target_entity": "koordinator",
        "question": "Утвердить общий маршрут нового участника проекта от первичного интереса до закрепления в поле деятельности.",
        "constraints": [
            "Ответ должен быть draft, не final canon.",
            "Выделить решения, которые должен принять ОПЕРАТОР.",
            "Указать, какие Сущности должны дать фрагменты канона."
        ]
    },
    {
        "target_entity": "vhodnoy-nastavnik",
        "question": "Описать первичную диагностику участника, первые безопасные задачи и признаки подходящего поля деятельности.",
        "constraints": [
            "Ориентироваться на участника с низкой подготовкой.",
            "Писать практично, без сложной теории.",
            "Выделить вопросы, которые надо задать участнику."
        ]
    },
    {
        "target_entity": "shkola",
        "question": "Описать учебно-практический маршрут участника и переход от обучения к реальному участию.",
        "constraints": [
            "Связать обучение с полезными действиями проекта.",
            "Предложить первые типы заданий.",
            "Выделить критерии готовности."
        ]
    },
    {
        "target_entity": "consultant",
        "question": "Собрать будущий participant-pathway-canon.md: структура документа, пробелы, вопросы автору, порядок review.",
        "constraints": [
            "Не утверждать канон.",
            "Сформировать структуру будущего документа.",
            "Выделить, какие ответы нужны от других Сущностей."
        ]
    }
]

def now():
    return time.strftime("%Y-%m-%dT%H:%M:%S")

def safe_stamp():
    return time.strftime("%Y%m%d-%H%M%S")

def main():
    PENDING.mkdir(parents=True, exist_ok=True)
    stamp = safe_stamp()
    created = []
    for item in TARGETS:
        ent = item["target_entity"]
        request_id = f"request__{stamp}__{ent}__participant_pathway"
        card = {
            "request_id": request_id,
            "target_entity": ent,
            "source_case": CASE,
            "source_question": QUESTION,
            "question": item["question"],
            "expected_output": EXPECTED,
            "constraints": item["constraints"],
            "status": "pending",
            "created_at": now(),
            "created_by": "CONSULTANT/log16-create-participant-pathway-requests.py",
            "source_log16_cards": []
        }
        path = PENDING / f"{request_id}.json"
        path.write_text(json.dumps(card, ensure_ascii=False, indent=2), encoding="utf-8")
        created.append(path)

    print("PASS entity requests created")
    print(f"CREATED: {len(created)}")
    for p in created:
        print(f"- {p}")

if __name__ == "__main__":
    main()
