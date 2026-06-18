# log16 module split v02 — dashboard review

## Краткий смысл

Dashboard review actions переведены на чистый модуль:

    log16.review.decisions

## Что изменено

- `src/log16/storage/layout.py` теперь соответствует текущему live runtime:
  - `derived-tasks/`
  - `entity-requests/`
  - `entity-responses/`

- `log16-dashboard.py` теперь оставляет локальную функцию `review_decision`, но она делегирует работу в:
  - `apply_review_decision`
  - `RuntimeLayout(ROOT)`

- `log16-dashboard.sh` выставляет `PYTHONPATH` на repo `src`.

## Что не изменено

Визуальная часть dashboard не переписана.
Runner/pult не переписаны.
Legacy code ещё остаётся.

## Следующий шаг

module split v03:
- вынести status counts dashboard в `log16.storage.layout`;
- убрать дублирующие функции read/write JSON из dashboard;
- добавить CLI для review decision.

КТО: КОНСУЛЬТАНТ
ДЛЯ ЧЕГО: фиксация module split v02 dashboard review
СТАТУС: working
