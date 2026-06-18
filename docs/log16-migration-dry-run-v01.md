# log16 migration dry-run v01

## Краткий смысл

Проверка перед переносом runtime из legacy path в target path.

## Legacy runtime

    /data/wellbeing/obs/consultant/outbox/log16-kernel

## Target runtime

    /data/wellbeing/obs/log16

## Что сделано

Запущен dry-run script:

    /data/wellbeing/repos/wellbeing-log16/scripts/log16-migration-dry-run-v01.sh

## Важно

Этот dry-run ничего не переносит, не удаляет и не создаёт symlink.

## Следующий шаг

После review dry-run отчёта можно готовить actual migration package:

    CONS__log16-runtime-migration-v01__OPR

Но только если:
- legacy runtime существует;
- target runtime не содержит конфликтующих данных;
- есть backup plan;
- compatibility symlink strategy утверждена.

КТО: КОНСУЛЬТАНТ
ДЛЯ ЧЕГО: dry-run план миграции log16 runtime
СТАТУС: working
