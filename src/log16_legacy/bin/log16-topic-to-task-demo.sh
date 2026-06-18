#!/usr/bin/env bash
set -Eeuo pipefail
exec /data/wellbeing/obs/log16/bin/log16-topic-to-task-core.py \
  --source-label "demo-current-system-task" \
  --text "Создать систему, использующую накопленную информацию проекта для формирования новых задач по темам, возникающим в процессе разработки подготовительной стадии запуска проекта. Participant_pathway был тестовым примером контура простой коммуникации участника с проектом."
