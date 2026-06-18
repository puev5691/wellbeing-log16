# log16 module split v07 — health check

## Краткий смысл

Добавлен health-check слой:

    log16.health.checks

и команда CLI:

    log16 check

## Команды

    log16 check
    log16 check --json
    log16 check --dashboard-url http://127.0.0.1:8898/

## Что проверяется

- runtime root;
- live layout directories;
- critical bin files:
  - log16;
  - log16-pult;
  - log16-dashboard.sh;
  - log16-dashboard.py;
- dashboard URL, если задан явно.

## Следующий шаг

После проверки v07 можно ставить tag:

    v0.2.0-lab

и затем начинать следующий слой:
- runner integration;
- cleaner dashboard module extraction;
- GitHub publication sanitation.

КТО: КОНСУЛЬТАНТ
ДЛЯ ЧЕГО: фиксация health-check log16
СТАТУС: working
