# log16 module split v06 — CLI bridge

## Краткий смысл

Единый CLI `log16` получил bridge-команды к старым рабочим pult/dashboard.

## Команды

    log16 pult status --cleanup
    log16 answer "вопрос"
    log16 tasks "тема"
    log16 run-pending
    log16 latest
    log16 cleanup
    log16 dashboard

## Что важно

Это bridge layer.
Он не удаляет старые:

    log16-pult
    log16-dashboard.sh
    runner

## Зачем

ОПЕРАТОР получает единый вход:

    /data/wellbeing/obs/log16/bin/log16

а старые механизмы продолжают работать до постепенного переписывания.

## Следующий шаг

module split v07:
- сделать `log16 check`;
- добавить health-check dashboard/pult/runtime;
- подготовить release tag v0.2.0-lab после стабилизации.

КТО: КОНСУЛЬТАНТ
ДЛЯ ЧЕГО: фиксация CLI bridge log16
СТАТУС: working
