# log16 root README activation v02

## Краткий смысл

 активирован как root .

## Activated source

    docs/public/github-root-readme-draft-v02.md

## Activated target

    README.md

## Backup

    docs/public/root-readme-backups/README-before-v02-activation-0619-2206.md

## Fix note

Первый activation installer создал корректный результат, но при записи этого productization note использовал unquoted heredoc with Markdown backticks.

Из-за этого shell попытался выполнить пути внутри обратных кавычек как команды и вывел ошибки:

    docs/public/github-root-readme-draft-v02.md: Permission denied
    README.md: command not found

Функционально activation прошла успешно, потому что root README был скопирован и проверки подтвердили соответствие.

Этот файл исправлен отдельным fix commit, чтобы в документации не оставался повреждённый note.

## Safety

Remote не добавлялся.

Push не выполнялся.

Root README activation выполнена локально и зафиксирована commit-ом.

## Status

fixed

КТО: КОНСУЛЬТАНТ
ДЛЯ ЧЕГО: root README activation v02 corrected note
СТАТУС: fixed
