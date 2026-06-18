# log16 GitHub publish guarded v01

## Краткий смысл

Добавлен защищённый script для реальной публикации wellbeing-log16 на GitHub.

## Script

    scripts/github-publish-guarded.sh

## Важно

Installer этого пакета не публикует код.

Реальная публикация возможна только при явном запуске guarded script с переменными:

    LOG16_CONFIRM_GITHUB_PUBLISH=YES_I_REALLY_MEAN_IT
    LOG16_GITHUB_OWNER=<owner>
    LOG16_GITHUB_REPO=wellbeing-log16
    LOG16_GITHUB_VISIBILITY=private

## Рекомендуемый безопасный запуск

    cd /data/wellbeing/repos/wellbeing-log16
    scripts/github-prepublish-check.sh
    git status --short

    LOG16_CONFIRM_GITHUB_PUBLISH=YES_I_REALLY_MEAN_IT \
    LOG16_GITHUB_OWNER=puev5691 \
    LOG16_GITHUB_REPO=wellbeing-log16 \
    LOG16_GITHUB_VISIBILITY=private \
    scripts/github-publish-guarded.sh

## Что делает guarded script

- проверяет явное подтверждение;
- требует owner;
- default repo name: wellbeing-log16;
- default visibility: private;
- запускает prepublish-check;
- требует clean git status;
- проверяет gh CLI;
- создаёт GitHub repo, если его нет;
- добавляет origin, если его нет;
- отказывается работать, если origin уже есть и отличается;
- выполняет push master;
- выполняет push tags.

## Почему private по умолчанию

Потому что сначала лучше опубликовать закрыто, проверить содержимое на GitHub глазами, а потом уже решать вопрос публичности.

КТО: КОНСУЛЬТАНТ
ДЛЯ ЧЕГО: guarded GitHub publish script for log16
СТАТУС: guarded
