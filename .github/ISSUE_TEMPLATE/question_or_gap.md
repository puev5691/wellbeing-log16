---
name: Question or knowledge gap
description: Вопрос или обнаруженный пробел в public knowledge base.
title: "Gap: "
labels: [question, knowledge-gap]
body:
  - type: markdown
    attributes:
      value: |
        Используйте этот шаблон, если нашли вопрос, на который public docs пока не отвечают.
        Не вставляйте private credentials, private runtime state или внутренние материалы проекта.
  - type: textarea
    id: question
    attributes:
      label: Вопрос
      description: Сформулируйте вопрос коротко и проверяемо.
    validations:
      required: true
  - type: textarea
    id: context
    attributes:
      label: Контекст
      description: Где возник вопрос и с каким документом он связан.
    validations:
      required: false
  - type: textarea
    id: expected_answer
    attributes:
      label: Какой ответ был бы полезен
      description: Опишите, какой тип ответа нужен.
    validations:
      required: false
---
