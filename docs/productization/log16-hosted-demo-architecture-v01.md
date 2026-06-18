# log16 hosted demo architecture v01

## Краткий смысл

Для большинства пользователей нужен hosted/demo вариант.

Но нельзя просто открыть наружу LLM endpoint.

## Почему нельзя открыть сырой LLM

Риски:

    стоимость
    спам
    prompt abuse
    утечка внутреннего контекста
    хаотические ответы
    отсутствие review
    нагрузка на машину
    компрометация доверия к проекту

## Правильный контур

    public web UI
    question form
    approved answer cache
    new question queue
    review queue
    controlled LLM call
    human/entity approval
    published answer

## Минимальный hosted MVP

На первом этапе hosted demo может не генерировать всё заново.

Он может:

    принимать вопрос
    искать approved/reusable answer
    показывать готовый ответ
    если ответа нет — создавать pending question
    обещать review later
    не тратить LLM на каждый запрос

## Компоненты

    web frontend
    API gateway
    answer cache
    question queue
    moderation/review layer
    limited model runner
    logging without personal leaks
    admin dashboard

## Ограничения

    no raw shell access
    no direct runtime exposure
    no private project data
    no unlimited free generation
    no automatic publication without review

## Экономика

Hosted вариант будет стоить денег:

    VPS / GPU / local tunnel
    storage
    monitoring
    backups
    admin time
    abuse protection

Поэтому public hosted demo должен быть ограниченным.

## Вывод

Hosted demo нужен, но только как controlled answer system, а не как бесплатная дырка в локальный ИИ.

КТО: КОНСУЛЬТАНТ
ДЛЯ ЧЕГО: hosted demo architecture plan for log16
СТАТУС: working
