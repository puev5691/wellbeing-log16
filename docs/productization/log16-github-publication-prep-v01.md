# log16 GitHub publication prep v01

## Краткий смысл

Этот документ фиксирует последнюю локальную подготовку перед возможной публичной публикацией repo.

Это НЕ push.

Это НЕ добавление remote.

Это НЕ публикация.

## Current local milestone

    v0.3.3-lab

## What must be true before publication

    README.md активирован и проверен
    GitHub issue templates добавлены
    pull request template добавлен
    public docs checks pass
    public answer cards checks pass
    tests pass
    doctor OK
    prepublish READY_FOR_GITHUB_PREP
    git status clean

## Final local check

Use:

    scripts/check-github-publication-prep.sh

## Publication remains guarded

Перед реальным push ОПЕРАТОР должен отдельно решить:

    где будет remote
    public или private repo
    как будет называться repo
    какие branch/tag публиковать
    нужен ли mirror/backup перед push

## Explicit no-go without separate decision

    не добавлять remote автоматически
    не выполнять git push автоматически
    не публиковать private runtime state
    не публиковать raw internal queues
    не публиковать private credentials

## Status

draft publication prep

КТО: КОНСУЛЬТАНТ
ДЛЯ ЧЕГО: GitHub publication preparation checklist
СТАТУС: draft
