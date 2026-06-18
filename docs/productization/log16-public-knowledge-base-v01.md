# log16 public knowledge base v01

## Краткий смысл

Публичная база знаний должна отвечать на вопросы пользователей о проекте и вести их к участию.

Это не просто FAQ.

Это слой reusable answers.

## Единица базы

    question_class
    canonical_question
    short_answer
    long_answer
    links
    related_docs
    related_tasks
    review_status
    source_status
    expiry_condition

## Базовые классы вопросов

    Что такое проект БЛАГОПОЛУЧИЕ?
    Что такое log16?
    Зачем нужен локальный AI?
    Как поставить Ollama?
    Почему нужен qwen3:8b?
    Что можно сделать без установки?
    Как помочь проекту?
    Какие задачи открыты?
    Как работает review?
    Что уже готово?
    Что пока не готово?
    Где границы ответственности?
    Как не навредить проекту?

## Публичные статусы ответов

    draft
    reviewed
    approved
    outdated
    needs_revision

## Форматы

    Markdown docs
    JSON answer cards
    searchable index
    GitHub Pages later
    hosted answer cache later

## Запреты

Не включать:

    private logs
    runtime queues
    personal data
    internal conflict notes
    credentials
    raw unreviewed entity outputs
    неутверждённые внешние обещания

## Связь с log16

log16 должен уметь производить approved/reusable answer cards, из которых затем собирается public knowledge base.

## Вывод

Публичная база знаний — это не приложение к repo.

Это один из главных интерфейсов проекта.

КТО: КОНСУЛЬТАНТ
ДЛЯ ЧЕГО: public knowledge base plan for log16
СТАТУС: working
