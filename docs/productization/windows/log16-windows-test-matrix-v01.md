# log16 Windows test matrix v01

## Краткий смысл

Без тестовой Windows-машины нельзя честно заявлять Windows support.

Нужна матрица проверки.

## Minimum matrix

### W-01. Windows + WSL2 + native Windows Ollama

    Windows 11
    WSL2 Ubuntu
    Ollama installed in Windows
    qwen3:8b pulled in Windows Ollama
    log16 repo inside WSL
    log16 doctor checks Ollama API

Проверить:

    WSL can reach Ollama API
    qwen3:8b visible
    log16 check OK
    dashboard opens
    pult works
    runner can call model

### W-02. Windows + WSL2 + WSL-native Ollama

    Windows 11
    WSL2 Ubuntu
    NVIDIA driver for WSL CUDA
    Ollama installed inside WSL
    qwen3:8b pulled inside WSL
    log16 repo inside WSL

Проверить:

    GPU visible inside WSL
    Ollama uses GPU if available
    model responds
    log16 doctor OK

### W-03. CPU-only fallback

    Windows 11
    WSL2 Ubuntu
    no usable GPU
    small model or mock mode

Проверить:

    mock demo works
    docs explain limitation
    qwen3:8b may be too slow/heavy

### W-04. Hosted-only user

    no local AI
    no WSL
    browser only

Проверить:

    public docs usable
    knowledge base usable
    hosted demo route described

## Result states

    supported
    experimental
    docs-only
    not supported

## Current status

    Windows support is not yet verified.
    Windows support is plausible through WSL2.
    Native PowerShell-only support is not a target for v01.

КТО: КОНСУЛЬТАНТ
ДЛЯ ЧЕГО: Windows test matrix for log16
СТАТУС: working
