# GitHub root README activation note v01

## Краткий смысл

`docs/public/github-root-readme-draft-v01.md` подготовлен как будущий root `README.md`.

## Почему не перезаписан README.md автоматически

Root README — это входная дверь будущего public repo.

Перезаписывать её вслепую нельзя.

## Рекомендуемый порядок активации

1. Просмотреть draft:

    docs/public/github-root-readme-draft-v01.md

2. Проверить, есть ли текущий root README:

    test -f README.md && sed -n '1,160p' README.md || echo "README.md missing"

3. Принять одно из решений:

    A. root README отсутствует -> можно копировать draft в README.md
    B. root README существует -> сравнить и вручную объединить
    C. root README пока не нужен -> оставить draft в docs/public/

## Safe command if approved and README.md is absent

    cp docs/public/github-root-readme-draft-v01.md README.md

## Не делать

    не перезаписывать README.md без просмотра
    не делать git push
    не добавлять remote
    не обещать production readiness

КТО: КОНСУЛЬТАНТ
ДЛЯ ЧЕГО: safe activation note for root README
СТАТУС: draft
