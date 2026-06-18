# log16 provider adapter roadmap v01

## Краткий смысл

Будущая работа с ChatGPT, Claude, Ollama и другими LLM должна идти через provider adapters, а не ручную копипасту между чатами.

## Минимальная схема

    entity_request
    -> provider_adapter
    -> model/API/local runner
    -> entity_response
    -> review
    -> synthesis

## Provider adapters

### ollama

Статус:
имеется лабораторный runner.

### chatgpt/openai

Статус:
будущий adapter.

Нужно:
- API key через .env;
- запрет на публикацию ключей;
- model config;
- request/response logging;
- human review.

### claude

Статус:
будущий adapter.

Нужно:
- отдельный provider module;
- совместимый response card;
- фиксация model/provider.

## Правило

ОПЕРАТОР не должен вручную бегать между LLM.
Если внешняя LLM нужна, она должна быть provider внутри log16.

КТО: КОНСУЛЬТАНТ
ДЛЯ ЧЕГО: roadmap provider adapters для log16
СТАТУС: working
