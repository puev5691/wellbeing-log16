# log16 release v0.2.0-lab

## Краткий смысл

Зафиксирована лабораторная milestone-точка log16 после сборки единой программы из рабочего набора скриптов.

## Статус

    v0.2.0-lab

## Что уже есть

- runtime перенесён в:

      /data/wellbeing/obs/log16

- старый путь сохранён как compatibility symlink:

      /data/wellbeing/obs/consultant/outbox/log16-kernel

- repo создан:

      /data/wellbeing/repos/wellbeing-log16

- локальный git repo чистый;
- единый CLI entrypoint есть:

      /data/wellbeing/obs/log16/bin/log16

- dashboard работает;
- review-submit работает;
- health-check работает;
- tests проходят.

## CLI

    log16 paths
    log16 status --json
    log16 check --json
    log16 pult status --cleanup
    log16 latest
    log16 dashboard

## Tests

См.:

    docs/log16-release-v0.2.0-lab-test-output.md

## Health

См.:

    docs/log16-release-v0.2.0-lab-health-output.json

## Последний HEAD перед release doc

    3ee2900

## Недавняя история

    3ee2900 Add log16 health check command
aaeaeee Add CLI bridge for pult and dashboard
a24cad6 Add unified log16 CLI entrypoint
6216ef3 Use storage card helpers from dashboard
7be4027 Use status module from dashboard
03ed52f Use review module from dashboard
fc05a62 Add first log16 module split
de1d980 Finalize log16 git cleanup log
470ac39 Add log16 git cleanup report
c302b7a Clean up log16 git snapshot metadata
667bfb5 Initial lab assembly of wellbeing-log16

## Ограничения

Это не production release.

Остаются хвосты:
- dashboard всё ещё крупный legacy file;
- pult/runner ещё не переписаны как чистые modules;
- GitHub publication не выполнена;
- vector DB не подключалась;
- provider adapters не внедрены;
- responses_needs_review ещё требуют операторского review.

## Следующий этап

После этой milestone-точки можно:
1. готовить GitHub sanitation;
2. продолжать module split dashboard/pult/runner;
3. добавлять provider adapters;
4. отдельно вернуться к вопросу retrieval/vector DB, когда текущий контур перестанет шататься.

КТО: КОНСУЛЬТАНТ
ДЛЯ ЧЕГО: фиксация лабораторной milestone log16 v0.2.0-lab
СТАТУС: milestone
