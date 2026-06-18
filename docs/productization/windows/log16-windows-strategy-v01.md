# log16 Windows strategy v01

## Краткий смысл

Windows support возможен, но его нельзя обещать как простой нативный запуск.

Текущий реалистичный путь:

    Windows 11
    WSL2
    Ubuntu
    bash/git/python внутри WSL
    Ollama + qwen3:8b
    log16 repo/runtime внутри WSL/Linux layout

## Почему не PowerShell-only

log16 уже использует:

    bash scripts
    Linux-like paths
    git workflow
    runtime directories
    local service ports
    Linux-style diagnostics

Переписывать это под PowerShell на текущем этапе нецелесообразно.

## Поддерживаемый путь v01

    Windows host
    WSL2 Ubuntu
    repo in WSL filesystem
    runtime in WSL filesystem
    Ollama either Windows-native or WSL-native

## Маршрут A. Windows-native Ollama + WSL log16

Плюсы:

    проще поставить Ollama через Windows installer
    модель живёт в Windows Ollama
    пользователю проще стартовать

Минусы:

    нужно проверить доступ WSL к Ollama API
    возможны сетевые нюансы localhost/host IP
    нужно документировать diagnostics

## Маршрут B. WSL-native Ollama + WSL log16

Плюсы:

    ближе к Linux setup
    проще для bash/runtime логики
    лучше воспроизводимость для разработчиков

Минусы:

    сложнее GPU/CUDA setup
    нужен корректный NVIDIA driver/CUDA on WSL
    сложнее для обычного пользователя

## Маршрут C. Hosted/demo

Для большинства пользователей это будет главный вход:

    web UI
    approved answers
    limited questions
    controlled LLM usage
    no local install

## Вывод

Windows support — это не один installer, а отдельная дорожка:

    read-only docs
    test matrix
    doctor checks
    WSL guide
    Ollama guide
    common errors
    hosted fallback

КТО: КОНСУЛЬТАНТ
ДЛЯ ЧЕГО: Windows support strategy for log16
СТАТУС: working
