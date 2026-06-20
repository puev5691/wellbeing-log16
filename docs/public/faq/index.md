# FAQ index

## Краткий смысл

Этот раздел собирает публичные ответы на первые вопросы о проекте БЛАГОПОЛУЧИЕ и log16.

## Первые FAQ

    what-is-wellbeing.md
    what-is-log16.md
    current-stage.md
    local-ai-requirements.md
    windows-support.md
    how-to-help.md
    not-ready-yet.md

## Связанные answer cards

    docs/public/knowledge-base/answers/

## Формат ответа

Каждый публичный ответ должен иметь:

    short answer
    long answer
    current status
    related docs
    related tasks
    review status

## Текущий статус

draft public FAQ skeleton

КТО: КОНСУЛЬТАНТ
ДЛЯ ЧЕГО: public FAQ index
СТАТУС: draft

<!-- LOG16-FAQ-DIALOGUE-LIMITS-RU-START -->
## Почему система пока не отвечает как обычный чат?

Потому что текущая версия `wellbeing-log16` ещё не является полноценным диалоговым помощником.

Режим `answer` сейчас поддерживает только ограниченный набор простых локальных вопросов. Если вопрос требует поиска источников, анализа большого контекста, маршрутизации к Сущностям или проверки результата, его нужно направлять не в прямой ответ, а в рабочий конвейер: `tasks`, source/evidence lookup, synthesis и review.

Практическое правило:

- простой локальный факт — `answer`;
- большая тема или проектная проблема — `tasks`;
- проверка состояния — dashboard/status;
- утверждение результата — review.

Следующая цель разработки — диалоговый слой, который будет сам определять тип запроса и выбирать правильный режим работы без необходимости заставлять ОПЕРАТОРА помнить внутреннюю механику программы.
<!-- LOG16-FAQ-DIALOGUE-LIMITS-RU-END -->
