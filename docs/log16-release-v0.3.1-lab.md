# log16 release v0.3.1-lab

## Краткий смысл

`v0.3.1-lab` фиксирует первый связанный public entry layer после `v0.3.0-lab`.

Это не production release.

Это local lab milestone for public entry preparation.

## Основные изменения после v0.3.0-lab

### Public knowledge base skeleton

Добавлен:

    docs/public/

Содержит:

    project docs
    FAQ index
    participation entry
    task classes
    glossary
    current status
    publication boundary
    answer card template

### Public FAQ answer cards

Добавлена первая партия FAQ pages и reusable answer cards:

    what-is-wellbeing
    what-is-log16
    current-stage
    local-ai-requirements
    windows-support
    how-to-help
    not-ready-yet

### Answer card links

Answer cards связаны с FAQ/docs через:

    related_docs
    related_tasks
    routing.next_docs
    routing.next_actions

Добавлен navigation map:

    docs/public/navigation.md

### Public root README draft

Подготовлен guarded draft будущего root README:

    docs/public/github-root-readme-draft-v01.md
    docs/public/github-root-readme-activation-note-v01.md

Root README.md не перезаписывался.

## Verification

Перед фиксацией release выполнены:

    scripts/check-public-root-readme-draft.sh
    scripts/check-public-docs-skeleton.sh
    scripts/check-public-answer-cards.sh
    scripts/check-public-answer-links.sh
    scripts/run-tests.sh
    log16 doctor --json
    scripts/github-prepublish-check.sh

Ожидаемое состояние:

    PUBLIC_ROOT_README_DRAFT OK
    PUBLIC_DOCS_SKELETON OK
    PUBLIC_ANSWER_CARDS OK
    PUBLIC_ANSWER_LINKS OK
    tests OK
    doctor OK
    prepublish READY_FOR_GITHUB_PREP
    git status clean

См. рядом:

    docs/log16-release-v0.3.1-lab-public-checks.txt
    docs/log16-release-v0.3.1-lab-test-output.txt
    docs/log16-release-v0.3.1-lab-doctor-output.json
    docs/log16-release-v0.3.1-lab-prepublish-output.txt
    docs/log16-release-v0.3.1-lab-git-log.txt

## Publication status

Remote не добавлялся.

Push не выполнялся.

Public GitHub publication остаётся отдельным guarded step.

## Next recommended direction

После `v0.3.1-lab` разумная линия:

    review public root README draft
    decide whether to activate README.md
    prepare public issue/task templates
    prepare Windows/WSL test bench
    prepare v0.4.0-lab only after public entry activation or Windows route verification

КТО: КОНСУЛЬТАНТ
ДЛЯ ЧЕГО: release note for log16 v0.3.1-lab
СТАТУС: lab milestone
