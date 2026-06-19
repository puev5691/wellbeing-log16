---
name: Documentation feedback
description: Уточнение, ошибка или неясность в публичной документации.
title: "Docs: "
labels: [documentation, review-needed]
body:
  - type: markdown
    attributes:
      value: |
        Используйте этот шаблон для замечаний к README, FAQ, public docs или answer cards.
        Не вставляйте private credentials, private runtime state или внутренние материалы проекта.
  - type: input
    id: document
    attributes:
      label: Документ
      description: Укажите путь к документу.
      placeholder: docs/public/faq/index.md
    validations:
      required: true
  - type: textarea
    id: problem
    attributes:
      label: Что неясно или неверно
      description: Опишите проблему.
    validations:
      required: true
  - type: textarea
    id: proposed
    attributes:
      label: Предложение
      description: Как это лучше сформулировать или исправить.
    validations:
      required: false
---
