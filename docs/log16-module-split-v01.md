# log16 module split v01

## Краткий смысл

Начат первый module split: из legacy scripts выделены базовые модули для storage, layout и review decisions.

## Что добавлено

    src/log16/storage/cards.py
    src/log16/storage/layout.py
    src/log16/review/decisions.py
    src/log16/cli/__init__.py
    tests/test_log16_imports.py
    tests/test_log16_cards.py
    scripts/run-tests.sh

## Что не сделано

Живой dashboard/pult/runner пока не переписаны на эти модули.

Это осознанно: сначала добавляем проверяемые модули, потом постепенно переводим legacy scripts.

## Следующий шаг

module split v02:
- вынести dashboard review decision logic на `log16.review.decisions`;
- вынести status counts на `log16.storage.layout`;
- добавить CLI entrypoint.

КТО: КОНСУЛЬТАНТ
ДЛЯ ЧЕГО: первый module split log16
СТАТУС: working
