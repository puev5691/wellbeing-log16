# Contributing to wellbeing-log16

## Краткий смысл

`wellbeing-log16` находится на стадии local lab.

Публичные contribution routes пока готовятся. Этот файл задаёт первый безопасный порядок участия.

## Before contributing

Сначала прочитайте:

    README.md
    docs/public/navigation.md
    docs/public/publication-boundary.md
    docs/public/faq/index.md
    docs/public/tasks/open-task-classes.md

## What is useful now

Полезные типы вклада:

    исправление неясных формулировок
    найденные пробелы в документации
    проверка README и FAQ
    локальные diagnostic reports
    предложения public task classes
    проверка Windows/WSL route
    небольшие code patches with tests

## What not to include

Не добавляйте в public issues или PR:

    private credentials
    private runtime state
    personal correspondence
    raw internal queues
    unreviewed private project materials
    private infrastructure details

## Local checks

Перед предложением изменений полезно запускать:

    scripts/run-tests.sh
    /data/wellbeing/obs/log16/bin/log16 doctor --json
    scripts/github-prepublish-check.sh

## Status

draft contribution guide

КТО: КОНСУЛЬТАНТ
ДЛЯ ЧЕГО: public contributing guide
СТАТУС: draft
