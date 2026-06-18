# log16 public entry plan v01

## Краткий смысл

log16 нельзя публиковать как простой набор shell-скриптов для любого прохожего.

Полноценный запуск требует подготовленного окружения:

    Linux / bash / git
    Python
    Ollama
    qwen3:8b
    рабочий runtime layout
    понимание локального ИИ
    умение читать ошибки

Поэтому public repo должен быть не только кодом, но и системой входа в работу.

## Цель

Создать публичный входной контур:

    объяснение проекта
    демонстрация log16
    обучение локальному ИИ
    проверка окружения
    карта задач
    маршруты участия
    hosted/demo перспектива

## Этап 0. Локальная готовность

Состояние:

    repo локальный
    remote не обязателен
    public push не обязателен
    runtime локально
    prepublish-check проходит

Задача:

    не ломать рабочий контур
    продолжать вести git history
    не публиковать случайно

## Этап 1. Уровни входа

Нужно описать разные аудитории:

    читатель
    пользователь GitHub
    локальный AI-тестировщик
    разработчик
    инфраструктурщик
    потенциальный участник проекта

Каждый уровень должен иметь отдельный маршрут.

## Этап 2. Environment doctor

Нужен будущий модуль:

    log16 doctor

Он должен проверять:

    OS
    bash
    git
    python
    repo path
    runtime path
    Ollama availability
    qwen3:8b installed
    Ollama API responding
    disk space
    dashboard port availability

## Этап 3. Mock/demo mode

Нужен будущий режим:

    log16 demo --mock

Он должен показывать механику без реального LLM:

    sample question
    routing
    fake entity response
    review
    approved answer

Это позволит понять систему тем, у кого ещё нет Ollama/qwen3:8b.

## Этап 4. Local AI onboarding

Нужен отдельный учебный раздел:

    docs/local-ai/

Цель:

    объяснить локальный ИИ
    поставить Ollama
    скачать qwen3:8b
    проверить API
    подключить log16
    разобрать типовые ошибки

## Этап 5. Public knowledge base

Repo должен содержать не только код, но и базу ответов проекта:

    question class
    canonical answer
    short answer
    long answer
    links
    related tasks
    review status
    source status
    expiry condition

## Этап 6. Hosted/demo контур

Для большинства пользователей нужен hosted вариант.

Но нельзя открывать наружу сырой LLM без контроля.

Нужен контур:

    public web UI
    limited question form
    cached approved answers
    queue for new questions
    moderation/review
    controlled LLM calls
    no direct raw Ollama exposure

## Этап 7. GitHub publication

Публиковать только после:

    clean repo
    prepublish-check
    public docs skeleton
    no runtime leaks
    no private config
    no internal logs
    clear README
    clear contribution path

## Главная формула

    GitHub repo не равен установщик.
    GitHub repo = публичная школа входа + демонстрация системы + карта участия + код для подготовленных.

КТО: КОНСУЛЬТАНТ
ДЛЯ ЧЕГО: public entry plan for log16
СТАТУС: working
