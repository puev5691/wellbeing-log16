# log16 Windows hardware notes v01

## Краткий смысл

Windows test machine should be treated as a dedicated reproducibility bench, not just another laptop.

## Candidate hardware

Recommended:

    Windows 11 capable laptop
    NVIDIA GPU
    12 GB VRAM class or better
    32 GB RAM or better
    NVMe SSD
    enough cooling
    stable power

## Why 12 GB VRAM class

qwen3:8b through Ollama is a plausible local model target.

12 GB VRAM gives more breathing room than 8 GB for local LLM work, context, UI, and system overhead.

This does not guarantee all workloads fit; it just makes the test stand less miserable.

## What to test

    native Windows Ollama
    WSL2 Ubuntu
    WSL access to Windows Ollama
    WSL-native Ollama
    qwen3:8b latency
    dashboard access
    doctor script
    mock/demo mode when available

## Buying note

A separate Windows test laptop is useful because it gives a clean user-like environment.

Dual-boot or virtual tests can help, but they do not replace a normal Windows user machine.

КТО: КОНСУЛЬТАНТ
ДЛЯ ЧЕГО: Windows hardware notes for log16
СТАТУС: working
