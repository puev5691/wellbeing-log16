# log16 local AI onboarding v01

## Краткий смысл

Локальный запуск log16 без Ollama и qwen3:8b не является полноценным вариантом.

Нужна отдельная дорожка подготовки пользователя к локальному ИИ.

## Минимальная цель

Пользователь должен пройти путь:

    понять, зачем нужен локальный AI
    установить Ollama
    скачать qwen3:8b
    проверить API
    запустить log16 check
    запустить demo
    понять типовые ошибки

## Будущая структура docs/local-ai

    00_what_is_local_ai.md
    01_install_ollama.md
    02_pull_qwen3_8b.md
    03_test_ollama_api.md
    04_connect_log16.md
    05_common_errors.md
    06_hardware_notes.md
    07_send_diagnostic_report.md

## Минимальные команды будущего гайда

    ollama --version
    ollama pull qwen3:8b
    ollama list
    curl http://127.0.0.1:11434/api/tags
    log16 check
    log16 doctor
    log16 demo --mock

## Что нельзя обещать

Нельзя обещать, что это будет удобно всем.

Для большинства людей локальный AI всё ещё остаётся техническим входным барьером.

## Что можно обещать

Можно честно дать:

    пошаговую установку
    diagnostics
    common errors
    mock demo
    clear escalation route

## Типовые проблемы

    Ollama не установлен
    Ollama не запущен
    qwen3:8b не скачан
    модель слишком тяжёлая
    не хватает RAM/VRAM
    занят порт
    неправильный path
    пользователь запустил не из repo
    пользователь не понял разницу repo/runtime

## Следующий инженерный модуль

    log16 doctor

КТО: КОНСУЛЬТАНТ
ДЛЯ ЧЕГО: local AI onboarding plan for log16
СТАТУС: working
