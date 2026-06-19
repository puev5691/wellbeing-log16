# log16 publication decision checklist v01

## Краткий смысл

Перед первой публикацией нужно принять человеческое решение, а не дать скрипту изображать начальника.

## Decision points

1. Repo visibility

    public
    private
    delayed publication

2. Repo name

    wellbeing-log16
    другой вариант

3. Remote provider

    GitHub
    GitLab
    локальный mirror
    иной вариант

4. First published tag

    v0.3.3-lab
    более поздний tag
    branch only

5. What must not be published

    private credentials
    private runtime state
    raw internal queues
    unreviewed private materials
    infrastructure-private details

6. Last command before any push

    scripts/check-github-publication-prep.sh

## Recommended conservative path

    keep remote unset
    archive local repo state
    run final prep check
    review README.md manually
    decide publication target
    only then add remote and push

КТО: КОНСУЛЬТАНТ
ДЛЯ ЧЕГО: publication decision checklist
СТАТУС: draft
