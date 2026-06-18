# log16 module split v04 — dashboard cards

## Краткий смысл

Dashboard JSON helpers переведены на чистый модуль:

    log16.storage.cards

## Что добавлено

    safe_read_json()
    tests/test_log16_cards_safe.py

## Что изменено

`log16-dashboard.py` оставляет локальные функции:

    load_json()
    save_json()

но теперь они делегируют работу в:

    log16.storage.cards.safe_read_json
    log16.storage.cards.write_json

## Что не изменено

Визуальная часть dashboard не переписана.
Runner/pult не переписаны.

## Следующий шаг

module split v05:
- вынести file/path rendering helpers;
- подготовить нормальный `log16` CLI entrypoint;
- начать сокращать legacy dashboard code.

КТО: КОНСУЛЬТАНТ
ДЛЯ ЧЕГО: фиксация module split v04 dashboard cards
СТАТУС: working
