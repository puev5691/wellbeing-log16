# log16 GitHub remote dry-run v01

## Краткий смысл

Подготовлен read-only dry-run для возможной GitHub-публикации wellbeing-log16.

## Repo

    /data/wellbeing/repos/wellbeing-log16

## Runtime

    /data/wellbeing/obs/log16

## Scripts

    scripts/github-publication-dry-run.sh
    scripts/github-push-template.sh

## Важно

Этот шаг не добавляет remote и не выполняет push.

`github-push-template.sh` намеренно отказывается работать без явных переменных:

    LOG16_CONFIRM_GITHUB_PUSH=YES_I_REALLY_MEAN_IT
    LOG16_GITHUB_REMOTE_URL=<url>

## Рекомендуемый порядок настоящей публикации

1. Ещё раз выполнить:

       scripts/github-prepublish-check.sh
       git status --short

2. Создать репозиторий на GitHub вручную или через gh CLI.

3. Добавить remote.

4. Выполнить push master.

5. Выполнить push tags.

## Не публиковать

- runtime state;
- outbox/inbox;
- archives;
- backups;
- responses/reviews runtime;
- private config;
- secrets/tokens/keys.

КТО: КОНСУЛЬТАНТ
ДЛЯ ЧЕГО: GitHub publication dry-run для log16
СТАТУС: dry-run
