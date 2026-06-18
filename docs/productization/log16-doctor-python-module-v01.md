# log16 doctor Python module v01

## Краткий смысл

`log16 doctor` переведён с shell bridge на Python module:

    src/log16/doctor/checks.py

Standalone script остаётся как fallback:

    scripts/log16-doctor-readonly.sh

## Команда

    log16 doctor

## JSON

    log16 doctor --json

## Useful options

    log16 doctor --skip-ollama
    log16 doctor --skip-prepublish
    log16 doctor --skip-bins
    log16 doctor --repo /path/to/repo
    log16 doctor --runtime /path/to/runtime
    log16 doctor --ollama-url http://127.0.0.1:11434
    log16 doctor --model qwen3:8b

## Warning policy

Doctor должен быть полезен внешним тестировщикам.

Поэтому отсутствие Ollama или qwen3:8b является warning, а не fatal failure.

Для частичных тестовых окружений есть:

    --skip-bins

Это нужно потому, что RuntimeLayout.ensure() создаёт структуру каталогов, но не создаёт реальные runtime/bin scripts.

## Test policy

Во время installer-а repo может быть dirty до commit.

Поэтому CLI JSON test проверяет:

    ok == true
    failures == 0
    status in OK/WARN

После commit и clean repo полноценный live doctor должен стремиться к status OK.

## Почему это важно

Для Windows/WSL, hosted demo, внешних тестировщиков и локальных AI новичков нужен единый структурированный diagnostic report.

КТО: КОНСУЛЬТАНТ
ДЛЯ ЧЕГО: Python doctor module for log16
СТАТУС: fixed2
