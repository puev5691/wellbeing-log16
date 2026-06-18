# log16 root config design v01

## Цель

Подготовить log16 к переносу из экспериментального legacy runtime:

    /data/wellbeing/obs/consultant/outbox/log16-kernel

в будущий canonical runtime:

    /data/wellbeing/obs/log16

без немедленного разрушения работающей системы.

## Проблема

Legacy scripts содержат hardcoded paths.

Если просто перенести каталог, часть скриптов продолжит смотреть в старый путь.

## Решение

Ввести единый config layer:

- environment variable `LOG16_ROOT`;
- optional `LOG16_CONFIG`;
- repo config `config/paths.json`;
- Python module `log16.config`.

## Порядок

1. Зафиксировать hardcoded path audit.
2. Добавить config module.
3. Подготовить migration script.
4. Сделать copy migration, не move.
5. Прогнать checks.
6. Только потом менять wrappers/dashboard/pult на новый root.
7. Legacy path оставить как compatibility bridge до стабилизации.

## Не делать

Не делать сырой `mv`.
Не удалять legacy runtime.
Не публиковать runtime в GitHub.

КТО: КОНСУЛЬТАНТ
ДЛЯ ЧЕГО: design root config для log16
СТАТУС: working
