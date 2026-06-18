# log16 productization plan v01

## Цель

Превратить набор рабочих скриптов log16 в единую программу.

## Этап 1. Repo skeleton

Статус:
started

Действия:
- создать `/data/wellbeing/repos/wellbeing-log16`;
- скопировать legacy scripts;
- скопировать schemas;
- создать README;
- создать .gitignore;
- создать docs.

## Этап 2. Root configuration

Нужно:
- убрать hardcoded `/data/wellbeing/obs/consultant/outbox/log16-kernel`;
- ввести `LOG16_ROOT`;
- добавить config/paths.json.

## Этап 3. Runtime migration

Нужно:
- создать backup старого runtime;
- скопировать state в `/data/wellbeing/obs/log16`;
- поставить compatibility symlink или root config;
- проверить dashboard/pult/runner.

## Этап 4. Module split

Разнести legacy scripts по модулям:
- storage;
- cards;
- runner;
- dashboard;
- review;
- dispatch;
- triage;
- adapters.

## Этап 5. Tests

Добавить проверки:
- import;
- path config;
- card read/write;
- triage;
- dispatch;
- review decision.

## Этап 6. GitHub

После sanitation:
- git init;
- first commit;
- remote add;
- push.

КТО: КОНСУЛЬТАНТ
ДЛЯ ЧЕГО: план превращения log16 в единую программу
СТАТУС: working
