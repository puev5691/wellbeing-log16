# log16 module split v05 — CLI entrypoint

## Краткий смысл

Добавлен единый CLI entrypoint:

    log16

## Runtime wrapper

    /data/wellbeing/obs/log16/bin/log16

## Команды

    log16 paths
    log16 status
    log16 status --json
    log16 review-apply --card PATH --decision approve_as_is

## Что не изменено

Старые `log16-pult`, dashboard и runner пока не заменены.
Новый CLI — это первый единый вход в программу, а не демонтаж работающих частей.

## Следующий шаг

module split v06:
- перевести часть pult/status на новый CLI;
- добавить subcommand для dashboard start/check;
- подготовить постепенную замену wrappers.

КТО: КОНСУЛЬТАНТ
ДЛЯ ЧЕГО: фиксация единого CLI entrypoint log16
СТАТУС: working
