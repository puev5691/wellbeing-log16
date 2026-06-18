# log16 runtime layout v01

## Future runtime root

    /data/wellbeing/obs/log16

## Layout

    bin/
    config/
    registry/
    cases/
    themes/
    tasks/
      proposed/
      routed/
      dispatched/
      done/
      rejected/
      archived/
    requests/
      pending/
      running/
      done/
      failed/
    responses/
      needs_review/
      approved/
      revision_requested/
      rejected/
      failed/
    reviews/
    reviewed-docs/
    reports/
    dashboard-runs/
    runner-reports/
    archives/
    var/
    backups/

## Принцип

Runtime — это живое состояние системы.
Его нельзя смешивать с GitHub-кодом и outbox-пакетами.

КТО: КОНСУЛЬТАНТ
ДЛЯ ЧЕГО: план runtime layout log16
СТАТУС: working
