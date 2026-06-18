# log16 module map v01

## Current clean modules

### log16.config

Назначение:
загрузка root config.

### log16.storage.cards

Назначение:
чтение/запись/перемещение JSON cards.

### log16.storage.layout

Назначение:
единая карта runtime directories.

### log16.review.decisions

Назначение:
фиксация review decisions:
- approve_as_is;
- approve_with_edit;
- request_revision;
- reject.

### log16.cli

Назначение:
placeholder для будущего CLI.

## Legacy area

    src/log16_legacy/bin

Назначение:
текущие рабочие scripts до переписывания.

КТО: КОНСУЛЬТАНТ
ДЛЯ ЧЕГО: карта модулей log16
СТАТУС: working
