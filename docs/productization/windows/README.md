# log16 Windows onboarding

## Краткий смысл

Windows support для log16 нужно рассматривать как отдельный productization track.

Текущий log16 вырос в Linux/bash/runtime окружении. Для Windows-пользователей реалистичны не один, а несколько маршрутов:

    Windows + WSL2 Ubuntu + log16
    Windows-native Ollama + WSL2 log16
    WSL2-native Ollama + WSL2 log16
    hosted/demo access для нетехнических пользователей

## Базовые документы

    log16-windows-strategy-v01.md
    log16-windows-test-matrix-v01.md
    log16-windows-wsl2-ollama-qwen3-v01.md
    log16-windows-hardware-notes-v01.md
    log16-windows-open-questions-v01.md

## Sources

    https://ollama.com/download/windows
    https://ollama.com/library/qwen3:8b
    https://learn.microsoft.com/en-us/windows/wsl/install
    https://docs.nvidia.com/cuda/wsl-user-guide/index.html
    https://learn.microsoft.com/en-us/windows/ai/directml/gpu-cuda-in-wsl

КТО: КОНСУЛЬТАНТ
ДЛЯ ЧЕГО: Windows onboarding index for log16
СТАТУС: working
