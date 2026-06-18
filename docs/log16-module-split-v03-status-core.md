# log16 module split v03 — status core

## Краткий смысл

Dashboard status counters переведены на чистый модуль:

    log16.storage.status

## Что добавлено

    src/log16/storage/status.py
    tests/test_log16_status.py

## Что изменено

`log16-dashboard.py` оставляет локальную функцию `status_counts`, но она теперь делегирует работу в:

    log16.storage.status.status_counts(RuntimeLayout(ROOT))

## Что не изменено

Визуальная часть dashboard не переписана.
Runner/pult не переписаны.

## Следующий шаг

module split v04:
- вынести JSON helper functions из dashboard;
- подключить dashboard к `log16.storage.cards`;
- подготовить единый CLI entrypoint.

КТО: КОНСУЛЬТАНТ
ДЛЯ ЧЕГО: фиксация module split v03 status core
СТАТУС: working
