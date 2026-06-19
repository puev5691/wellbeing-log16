---
name: Local diagnostics report
description: Отчёт о локальной проверке log16.
title: "Diagnostics: "
labels: [diagnostics, local-lab]
body:
  - type: markdown
    attributes:
      value: |
        Используйте этот шаблон для отчётов о локальном запуске.
        Перед публикацией удалите private credentials, private paths with personal data и внутренние материалы проекта.
  - type: textarea
    id: environment
    attributes:
      label: Environment
      description: ОС, shell, Python, Ollama, model, способ запуска.
      placeholder: Ubuntu, bash, Python 3.x, Ollama, qwen3:8b
    validations:
      required: true
  - type: textarea
    id: commands
    attributes:
      label: Commands run
      description: Какие команды запускались.
      placeholder: scripts/run-tests.sh
    validations:
      required: true
  - type: textarea
    id: result
    attributes:
      label: Result
      description: Краткий результат без private data.
    validations:
      required: true
---
