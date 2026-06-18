# log16 Windows open questions v01

## Краткий смысл

Before claiming Windows support, these questions must be tested.

## WSL / path questions

    Can we reliably use /data/wellbeing layout inside WSL?
    Should installer create /data/wellbeing?
    Do permissions behave cleanly?
    Does file watching matter later?

## Ollama questions

    Should Windows users run Ollama natively or inside WSL?
    Can WSL reliably reach Windows-native Ollama on localhost?
    Is host-IP fallback needed?
    Does qwen3:8b appear the same from WSL diagnostics?
    Does GPU acceleration work in each mode?

## Runtime questions

    Can dashboard bind/open predictably?
    Which ports collide on Windows systems?
    Does browser access from Windows host to WSL dashboard work cleanly?
    Should dashboard bind to 127.0.0.1 or 0.0.0.0?

## Documentation questions

    How much Linux/WSL training is required?
    What is the shortest safe path?
    What screenshots are needed?
    Which errors are common?

## Support boundary

For v01:

    Windows through WSL2: experimental target
    Windows PowerShell-only: not supported
    hosted demo: future route for nontechnical users

КТО: КОНСУЛЬТАНТ
ДЛЯ ЧЕГО: Windows open questions for log16
СТАТУС: working
