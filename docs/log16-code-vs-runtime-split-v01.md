# log16 code vs runtime split v01

## Проблема

Сейчас код, runtime state и отчёты смешаны в старом каталоге:

    /data/wellbeing/obs/consultant/outbox/log16-kernel

Это удобно для эксперимента, но плохо для программы.

## Решение

Разделить:

### Code

    /data/wellbeing/repos/wellbeing-log16

Содержит исходный код, schemas, docs, examples, tests, install scripts.

### Runtime

    /data/wellbeing/obs/log16

Содержит entity registry, queues, cards, responses, reviews, reports, dashboard runs, archives, var/cache/locks.

### Consultant outbox

    /data/wellbeing/obs/consultant/outbox

Содержит пакеты выдачи КОНСУЛЬТАНТА, tgz для ОПЕРАТОРА, route-note, manifest.

## Правило

GitHub получает code.
Obsidian/runtime получает project state.
Outbox получает delivery artifacts.

КТО: КОНСУЛЬТАНТ
ДЛЯ ЧЕГО: разделение кода и runtime state log16
СТАТУС: working
