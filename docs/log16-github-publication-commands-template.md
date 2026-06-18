# log16 GitHub publication commands template

## Вариант A: remote уже создан на GitHub

    cd /data/wellbeing/repos/wellbeing-log16
    scripts/github-prepublish-check.sh
    git status --short
    git remote add origin <GITHUB_REMOTE_URL>
    git remote -v
    git push -u origin master
    git push origin --tags

## Вариант B: gh CLI

    cd /data/wellbeing/repos/wellbeing-log16
    scripts/github-prepublish-check.sh
    git status --short
    gh repo create <OWNER>/wellbeing-log16 --private --source=. --remote=origin --push
    git push origin --tags

## Защита от случайности

Для реального shell-template:

    scripts/github-push-template.sh

нужны переменные:

    LOG16_CONFIRM_GITHUB_PUSH=YES_I_REALLY_MEAN_IT
    LOG16_GITHUB_REMOTE_URL=<url>

КТО: КОНСУЛЬТАНТ
ДЛЯ ЧЕГО: шаблон команд публикации log16 на GitHub
СТАТУС: template
