# log16 release v0.3.0-lab

## Краткий смысл

`v0.3.0-lab` фиксирует переход log16 от локального рабочего прототипа к подготовке публичного входного контура и диагностике внешних окружений.

Это не production release.

Это local lab milestone.

## Основные изменения после v0.2.0-lab

### Productization / onboarding

Добавлен раздел:

    docs/productization/

В него вошли документы:

    log16-public-entry-plan-v01.md
    log16-user-levels-v01.md
    log16-local-ai-onboarding-v01.md
    log16-hosted-demo-architecture-v01.md
    log16-public-knowledge-base-v01.md
    log16-publication-readiness-checklist-v01.md

### Windows / WSL onboarding

Добавлен раздел:

    docs/productization/windows/

В него вошли документы:

    log16-windows-strategy-v01.md
    log16-windows-test-matrix-v01.md
    log16-windows-wsl2-ollama-qwen3-v01.md
    log16-windows-hardware-notes-v01.md
    log16-windows-open-questions-v01.md

### Doctor diagnostics

Добавлены:

    scripts/log16-doctor-readonly.sh
    src/log16/doctor/checks.py
    log16 doctor
    log16 doctor --json

Doctor проверяет:

    core commands
    git repo/status
    prepublish-check
    runtime health
    Ollama API
    qwen3:8b
    disk
    related ports

### CLI

`log16 doctor` теперь работает через Python module.

Standalone shell doctor оставлен как fallback.

## Verification

Перед фиксацией release выполнены:

    scripts/run-tests.sh
    log16 doctor
    log16 doctor --json
    scripts/github-prepublish-check.sh

Ожидаемое состояние:

    tests OK
    doctor OK
    doctor JSON ok true
    prepublish READY_FOR_GITHUB_PREP
    git status clean

См. рядом:

    docs/log16-release-v0.3.0-lab-test-output.txt
    docs/log16-release-v0.3.0-lab-doctor-output.json
    docs/log16-release-v0.3.0-lab-prepublish-output.txt
    docs/log16-release-v0.3.0-lab-git-log.txt

## Publication status

Remote не добавлялся.

Push не выполнялся.

Публичная публикация отложена до отдельного решения.

## Next recommended direction

После `v0.3.0-lab` разумная линия работ:

    public knowledge base skeleton
    local AI onboarding docs
    Windows/WSL test bench
    doctor report export for support
    hosted demo requirements

КТО: КОНСУЛЬТАНТ
ДЛЯ ЧЕГО: release note for log16 v0.3.0-lab
СТАТУС: lab milestone
