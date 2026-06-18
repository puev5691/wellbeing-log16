# log16 Windows WSL2 Ollama qwen3 v01

## Краткий смысл

Основной кандидатный путь для Windows:

    Windows 11
    WSL2 Ubuntu
    Ollama
    qwen3:8b
    log16 repo/runtime in Linux filesystem

## Official starting points

    Windows Ollama:
    https://ollama.com/download/windows

    qwen3:8b in Ollama:
    https://ollama.com/library/qwen3:8b

    WSL install:
    https://learn.microsoft.com/en-us/windows/wsl/install

    NVIDIA CUDA on WSL:
    https://docs.nvidia.com/cuda/wsl-user-guide/index.html
    https://learn.microsoft.com/en-us/windows/ai/directml/gpu-cuda-in-wsl

## Candidate install flow

### Step 1. Install WSL2

    wsl --install

Preferred distro:

    Ubuntu

### Step 2. Prepare Linux tools in WSL

    sudo apt update
    sudo apt install -y git curl python3 python3-venv

### Step 3A. Use Windows-native Ollama

Install Ollama in Windows.

Then check from WSL:

    curl http://127.0.0.1:11434/api/tags

If localhost does not work from WSL, document host-IP fallback later.

### Step 3B. Use WSL-native Ollama

Install Ollama inside WSL.

Then check:

    ollama --version
    ollama pull qwen3:8b
    curl http://127.0.0.1:11434/api/tags

### Step 4. Clone or copy repo

Future public case:

    git clone <repo-url>

Current local/test case:

    transfer bundle or copy repo

### Step 5. Run checks

    scripts/github-prepublish-check.sh
    scripts/log16-doctor-readonly.sh
    /data/wellbeing/obs/log16/bin/log16 check --json

## Open issue

Current runtime paths are Linux-specific:

    /data/wellbeing/obs/log16
    /data/wellbeing/repos/wellbeing-log16

For Windows/WSL guide, we need decide whether to preserve /data/wellbeing inside WSL or provide alternative root.

## Recommended v01 rule

For WSL testers, use the same Linux layout inside WSL:

    /data/wellbeing/obs/log16
    /data/wellbeing/repos/wellbeing-log16

This reduces path drift.

КТО: КОНСУЛЬТАНТ
ДЛЯ ЧЕГО: Windows WSL2 Ollama qwen3 guide draft for log16
СТАТУС: working
