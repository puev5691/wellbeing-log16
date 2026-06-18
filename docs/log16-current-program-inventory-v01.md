# log16 current program inventory v01

## Краткий смысл

Этот документ фиксирует текущее состояние log16 как набора рабочих скриптов и runtime-каталогов.

## Старый runtime root

    /data/wellbeing/obs/consultant/outbox/log16-kernel

## Новый repo root

    /data/wellbeing/repos/wellbeing-log16

## Future runtime root

    /data/wellbeing/obs/log16

## Скопированные скрипты

        log16-agent-runner-check.sh
    log16-agent-runner-generic-check.sh
    log16-agent-runner.py
    log16-ask-import-v05-2.sh
    log16-case-summary.py
    log16-case-summary.sh
    log16-create-participant-pathway-requests.py
    log16-dashboard-check.sh
    log16-dashboard-open.sh
    log16-dashboard.py
    log16-dashboard.sh
    log16-dispatch-participant-pathway.sh
    log16-dispatch-questions.py
    log16-dispatch-questions.sh
    log16-dispatch-routed-tasks.py
    log16-dispatch-routed-tasks.sh
    log16-extend-entity-registry-v01.py
    log16-gui-check.sh
    log16-gui.py
    log16-gui.sh
    log16-import-latest-v05-2.sh
    log16-import-v05-run.py
    log16-import-v05-run.sh
    log16-last-report.sh
    log16-new-id.sh
    log16-participant-pathway-case.sh
    log16-pult
    log16-pult-check.sh
    log16-pult.py
    log16-routed-task-dispatch-check.sh
    log16-runner-participant-communication.sh
    log16-runner-participant-pathway.sh
    log16-runner-topic-to-task-system.sh
    log16-smoke-test.sh
    log16-status.sh
    log16-synthesize-participant-pathway.py
    log16-synthesize-participant-pathway.sh
    log16-topic-task-triage-check.sh
    log16-topic-task-triage.py
    log16-topic-task-triage.sh
    log16-topic-to-task-check.sh
    log16-topic-to-task-core.py
    log16-topic-to-task-demo.sh
    log16-topic-to-task.sh
    log16-webui-check.sh
    log16-webui-open.sh
    log16-webui.py
    log16-webui.sh

## Скопированные schemas

        answer-card.schema.json
    approved-answer-card.schema.json
    derived-task-card.schema.json
    entity-request-card.schema.json
    entity-response-card.schema.json
    gap-card.schema.json
    review-card.schema.json
    task-batch.schema.json
    task-card.schema.json
    theme-card.schema.json

## Что это значит

Сейчас программа ещё не очищена.
Рабочие скрипты помещены в legacy-зону, чтобы их можно было анализировать, переписывать и постепенно превращать в нормальные модули.

КТО: КОНСУЛЬТАНТ
ДЛЯ ЧЕГО: инвентаризация текущей программы log16
СТАТУС: working
