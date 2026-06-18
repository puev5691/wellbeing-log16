# log16 doctor readonly v01

## Краткий смысл

Добавлен первый read-only doctor script для диагностики окружения log16.

## Script

    scripts/log16-doctor-readonly.sh

## Что проверяет

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
    related listening ports
    disk usage

## Что не делает

    не меняет repo
    не меняет runtime
    не запускает сервисы
    не скачивает модели
    не добавляет remote
    не делает push

## Переменные

    LOG16_REPO=/data/wellbeing/repos/wellbeing-log16
    LOG16_RUNTIME=/data/wellbeing/obs/log16
    LOG16_OLLAMA_URL=http://127.0.0.1:11434
    LOG16_MODEL=qwen3:8b

## Зачем нужен

Перед тем как давать log16 внешним тестировщикам, нужно иметь единый диагностический отчёт.

Иначе внешний тестировщик будет писать "не работает", а внутри этого "не работает" может быть:

    нет Ollama
    нет qwen3:8b
    не тот path
    не запущен runtime
    сломан git status
    нет curl
    закрыт порт
    пользователь запустил не там

## Следующий шаг

После проверки standalone doctor нужно встроить его в CLI:

    log16 doctor

КТО: КОНСУЛЬТАНТ
ДЛЯ ЧЕГО: read-only doctor plan/script for log16
СТАТУС: working
