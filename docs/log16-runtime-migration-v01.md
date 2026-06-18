# log16 runtime migration v01

## Краткий смысл

Runtime log16 перенесён из legacy path в target path с сохранением compatibility symlink.

## Legacy path

    /data/wellbeing/obs/consultant/outbox/log16-kernel

Теперь это symlink на:

    /data/wellbeing/obs/log16

## Backup

    /data/wellbeing/obs/consultant/outbox/log16-kernel.backup-0618-1926

## Rollback

    /data/wellbeing/repos/wellbeing-log16/scripts/log16-runtime-migration-rollback-0618-1926.sh

## Post-check

    /data/wellbeing/repos/wellbeing-log16/docs/log16-runtime-migration-v01-post-check.md

## Что важно

Старые скрипты с hardcoded path продолжают работать через symlink.

Следующий этап:
- проверить dashboard;
- проверить pult;
- затем постепенно переводить код на LOG16_ROOT/config без зависимости от symlink.

КТО: КОНСУЛЬТАНТ
ДЛЯ ЧЕГО: фиксация миграции runtime log16
СТАТУС: migrated
