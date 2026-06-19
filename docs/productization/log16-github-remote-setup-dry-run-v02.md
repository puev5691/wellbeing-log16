# log16 GitHub remote setup dry-run v02

## Краткий смысл

Подготовлен guarded remote setup and dry-run push для первой публикации `wellbeing-log16`.

## Parameters

    remote_url: git@github.com:puev5691/wellbeing-log16.git
    visibility: public
    repo_name: wellbeing-log16
    publish_scope: master + tags

## What the script does

    checks git status clean
    checks current branch master
    checks tag v0.3.3-lab
    runs scripts/check-github-publication-prep.sh
    adds origin if missing
    aborts if origin exists and differs
    runs git ls-remote origin
    runs git push --dry-run origin master
    runs git push --dry-run origin --tags

## What it does not do

    no real push
    no GitHub repo creation
    no visibility change
    no branch protection setup

## Script

    scripts/github-remote-setup-dry-run-v02.sh

## Status

draft remote dry-run prep

КТО: КОНСУЛЬТАНТ
ДЛЯ ЧЕГО: GitHub remote setup dry-run before first public push
СТАТУС: draft
