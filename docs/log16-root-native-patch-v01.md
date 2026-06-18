# log16 root native patch v01

## Краткий смысл

Live bin scripts переведены с legacy symlink path на native runtime root.

## Old path

    /data/wellbeing/obs/consultant/outbox/log16-kernel

## New path

    /data/wellbeing/obs/log16

## Backup

    /data/wellbeing/obs/log16/backups/bin-before-root-native-patch-0618-1929

## Rollback

    /data/wellbeing/repos/wellbeing-log16/scripts/log16-root-native-patch-rollback-0618-1929.sh

## Post-check

    /data/wellbeing/repos/wellbeing-log16/docs/log16-root-native-patch-v01-post-check.md

## Что важно

Compatibility symlink сохранён, но основной запуск теперь должен идти из:

    /data/wellbeing/obs/log16/bin

КТО: КОНСУЛЬТАНТ
ДЛЯ ЧЕГО: фиксация root-native patch log16
СТАТУС: patched
