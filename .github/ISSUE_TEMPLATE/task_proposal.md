---
name: Task proposal
description: Предложение public task для развития log16.
title: "Task: "
labels: [task-proposal, review-needed]
body:
  - type: markdown
    attributes:
      value: |
        Используйте этот шаблон для предложений задач.
        Задача должна быть небольшой, проверяемой и связанной с public docs, tests или local lab route.
  - type: textarea
    id: task
    attributes:
      label: Задача
      description: Что именно предлагается сделать.
    validations:
      required: true
  - type: textarea
    id: reason
    attributes:
      label: Зачем это нужно
      description: Какую проблему решает задача.
    validations:
      required: true
  - type: textarea
    id: check
    attributes:
      label: Как проверить результат
      description: Какая команда, файл или критерий подтвердит выполнение.
    validations:
      required: true
---
