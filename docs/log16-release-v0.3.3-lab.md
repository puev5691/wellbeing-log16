# log16 release v0.3.3-lab

## Краткий смысл

v0.3.3-lab фиксирует состояние после добавления GitHub public templates.

Это локальный lab milestone, а не публичная публикация и не production release.

## Что изменилось после v0.3.2-lab

Добавлены public GitHub entry templates:

    CONTRIBUTING.md
    .github/ISSUE_TEMPLATE/config.yml
    .github/ISSUE_TEMPLATE/documentation_feedback.md
    .github/ISSUE_TEMPLATE/question_or_gap.md
    .github/ISSUE_TEMPLATE/local_diagnostics_report.md
    .github/ISSUE_TEMPLATE/task_proposal.md
    .github/PULL_REQUEST_TEMPLATE.md

Добавлены проверки:

    scripts/check-github-public-templates.sh
    tests/test_github_public_templates.py

## Verification

Перед фиксацией release выполнены:

    scripts/check-github-public-templates.sh
    scripts/check-root-readme-active-v02.sh
    scripts/check-root-readme-activation-note-v02.sh
    scripts/run-tests.sh
    log16 doctor --json
    scripts/github-prepublish-check.sh

Ожидаемое состояние:

    GITHUB_PUBLIC_TEMPLATES OK
    ROOT_README_ACTIVE_V02 OK
    ROOT_README_ACTIVATION_NOTE_V02 OK
    tests OK
    doctor OK
    prepublish READY_FOR_GITHUB_PREP
    git status clean

См. рядом:

    docs/log16-release-v0.3.3-lab-public-checks.txt
    docs/log16-release-v0.3.3-lab-test-output.txt
    docs/log16-release-v0.3.3-lab-doctor-output.json
    docs/log16-release-v0.3.3-lab-prepublish-output.txt
    docs/log16-release-v0.3.3-lab-git-log.txt

## Publication status

Remote не добавлялся.

Push не выполнялся.

GitHub publication остаётся отдельным guarded step.

## Next recommended direction

После v0.3.3-lab логичный следующий шаг:

    guarded GitHub remote/publication preparation
    или final local archive bundle before first public push

Перед push нужен отдельный operator decision.

КТО: КОНСУЛЬТАНТ
ДЛЯ ЧЕГО: release note for log16 v0.3.3-lab
СТАТУС: lab milestone
