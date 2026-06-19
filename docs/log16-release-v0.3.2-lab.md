# log16 release v0.3.2-lab

## Краткий смысл

v0.3.2-lab фиксирует состояние после активации README draft v02 как root README.md.

Это локальный lab milestone, а не публичная публикация и не production release.

## Что изменилось после v0.3.1-lab

### README v02

Добавлен README draft v02 с универсальной подачей:

    log16 как система работы с большими текстовыми информационными полями
    БЛАГОПОЛУЧИЕ как первый живой полигон
    применимость к другим большим массивам текстовой информации
    статус local lab, а не production

### Root README activation

README draft v02 активирован как root README.md.

Проверка:

    scripts/check-root-readme-active-v02.sh

### Activation note fix

Исправлен служебный productization note после shell heredoc issue.

Проверка:

    scripts/check-root-readme-activation-note-v02.sh

## Verification

Перед фиксацией release выполнены:

    scripts/check-root-readme-active-v02.sh
    scripts/check-root-readme-activation-note-v02.sh
    scripts/check-public-root-readme-v02.sh
    scripts/check-public-root-readme-draft.sh
    scripts/check-public-docs-skeleton.sh
    scripts/check-public-answer-cards.sh
    scripts/check-public-answer-links.sh
    scripts/run-tests.sh
    log16 doctor --json
    scripts/github-prepublish-check.sh

Ожидаемое состояние:

    ROOT_README_ACTIVE_V02 OK
    ROOT_README_ACTIVATION_NOTE_V02 OK
    PUBLIC_ROOT_README_V02 OK
    PUBLIC_ROOT_README_DRAFT OK
    PUBLIC_DOCS_SKELETON OK
    PUBLIC_ANSWER_CARDS OK
    PUBLIC_ANSWER_LINKS OK
    tests OK
    doctor OK
    prepublish READY_FOR_GITHUB_PREP
    git status clean

См. рядом:

    docs/log16-release-v0.3.2-lab-public-checks.txt
    docs/log16-release-v0.3.2-lab-test-output.txt
    docs/log16-release-v0.3.2-lab-doctor-output.json
    docs/log16-release-v0.3.2-lab-prepublish-output.txt
    docs/log16-release-v0.3.2-lab-git-log.txt

## Publication status

Remote не добавлялся.

Push не выполнялся.

GitHub publication остаётся отдельным guarded step.

## Recommended next step

После v0.3.2-lab разумно переходить к одному из двух направлений:

    public GitHub preparation package
    public issue/task templates

Перед push нужен отдельный operator decision.

КТО: КОНСУЛЬТАНТ
ДЛЯ ЧЕГО: release note for log16 v0.3.2-lab
СТАТУС: lab milestone
