# log16 doctor CLI bridge v01

## Краткий смысл

Команда `log16 doctor` добавлена как bridge к уже проверенному script:

    scripts/log16-doctor-readonly.sh

## Почему bridge

Doctor уже проверен как standalone script.

На этом этапе безопаснее встроить его в CLI как bridge, а не сразу переписывать всю диагностику в Python.

## Команда

    log16 doctor

## Overrides

    log16 doctor --repo /path/to/repo
    log16 doctor --runtime /path/to/runtime
    log16 doctor --ollama-url http://127.0.0.1:11434
    log16 doctor --model qwen3:8b

## Что проверяет underlying doctor

    bash
    git
    python3
    curl
    repo path
    git status
    prepublish-check
    runtime root
    critical runtime files
    log16 check --json
    Ollama API
    qwen3:8b presence
    related ports
    disk usage

## Следующий шаг

После нескольких реальных прогонов можно перенести doctor logic из bash в Python module:

    src/log16/doctor/

КТО: КОНСУЛЬТАНТ
ДЛЯ ЧЕГО: log16 doctor CLI bridge
СТАТУС: working
