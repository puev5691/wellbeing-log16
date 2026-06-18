# log16 GitHub publication policy v01

## Что можно выкладывать

- src/
- schemas/
- docs/
- examples/
- tests/
- README.md
- pyproject.toml
- scripts без secrets

## Что нельзя выкладывать

- runtime state;
- entity responses;
- private project documents;
- raw chat exports;
- API keys;
- tokens;
- personal data;
- generated archives;
- local logs.

## Перед первой публикацией

1. Проверить `.gitignore`.
2. Выполнить grep по secrets.
3. Убедиться, что runtime не попал в repo.
4. Создать первый local commit.
5. Только после review публиковать на GitHub.

КТО: КОНСУЛЬТАНТ
ДЛЯ ЧЕГО: политика публикации log16 на GitHub
СТАТУС: working
