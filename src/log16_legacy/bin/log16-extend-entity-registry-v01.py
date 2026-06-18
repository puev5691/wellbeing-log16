#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path("/data/wellbeing/obs/log16")
REG = ROOT / "entity-registry" / "entity-registry.json"

ADD = [
    {
      "entity_id": "archivarius",
      "display_name": "АРХИВАРИУС",
      "code": "ARCH",
      "provider": "ollama",
      "model": "qwen3:8b",
      "autonomy_level": "draft_only",
      "requires_human_review": True,
      "role_prompt": "Ты Сущность АРХИВАРИУС проекта БЛАГОПОЛУЧИЕ. Твоя зона — источники, evidence, provenance, поиск связанных файлов, картирование документов, фиксация происхождения и подготовка evidence lookup. Не утверждай канон, не выдумывай источники, помечай нехватку данных.",
      "context_files": []
    },
    {
      "entity_id": "koder",
      "display_name": "КОДЕР",
      "code": "KODER",
      "provider": "ollama",
      "model": "qwen3:8b",
      "autonomy_level": "draft_only",
      "requires_human_review": True,
      "role_prompt": "Ты Сущность КОДЕР проекта БЛАГОПОЛУЧИЕ. Твоя зона — код, схемы, прототипы, runner, проверяемые скрипты, анализ технических ограничений. Не выполняй опасные действия, не утверждай production-решения, пиши результат как draft для review.",
      "context_files": []
    },
    {
      "entity_id": "sysadmin",
      "display_name": "СИСАДМИН",
      "code": "SYS",
      "provider": "ollama",
      "model": "qwen3:8b",
      "autonomy_level": "draft_only",
      "requires_human_review": True,
      "role_prompt": "Ты Сущность СИСАДМИН проекта БЛАГОПОЛУЧИЕ. Твоя зона — инфраструктура, серверы, локальная среда, безопасность, сервисы, диагностика. Не меняй production и не предлагай опасные команды без явного review.",
      "context_files": []
    }
]

def main():
    if not REG.exists():
        REG.parent.mkdir(parents=True, exist_ok=True)
        data = {"entities": []}
    else:
        data = json.loads(REG.read_text(encoding="utf-8"))

    entities = data.setdefault("entities", [])
    by_id = {e.get("entity_id"): e for e in entities}
    added = []
    updated = []
    for item in ADD:
        if item["entity_id"] in by_id:
            by_id[item["entity_id"]].update(item)
            updated.append(item["entity_id"])
        else:
            entities.append(item)
            added.append(item["entity_id"])

    REG.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    print("PASS entity registry extended")
    print(f"REGISTRY: {REG}")
    print(f"ADDED: {len(added)} {' '.join(added)}")
    print(f"UPDATED: {len(updated)} {' '.join(updated)}")

if __name__ == "__main__":
    main()
