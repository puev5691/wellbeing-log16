#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import tarfile
import time
from pathlib import Path
from typing import Any

ROOT = Path("/data/wellbeing/obs/log16")
OUTBOX = Path("/data/wellbeing/obs/consultant/outbox")
RESP = ROOT / "entity-responses" / "needs_review"
SYN = ROOT / "synthesis" / "participant-pathway"

ENTITY_ORDER = [
    ("koordinator", "КООРДИНАТОР"),
    ("vhodnoy-nastavnik", "ВХОДНОЙ НАСТАВНИК"),
    ("shkola", "ШКОЛА"),
    ("consultant", "КОНСУЛЬТАНТ"),
]

def now():
    return time.strftime("%Y-%m-%dT%H:%M:%S")

def stamp():
    return time.strftime("%Y%m%d-%H%M%S")

def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))

def clean(s: str) -> str:
    return re.sub(r"\n{3,}", "\n\n", (s or "").strip())

def latest_responses() -> dict[str, dict[str, Any]]:
    cards = {}
    for path in sorted(RESP.glob("*.json"), key=lambda p: p.stat().st_mtime):
        try:
            data = load_json(path)
        except Exception:
            continue
        text = " ".join([
            str(path),
            data.get("source_case", ""),
            data.get("response_id", ""),
            data.get("question", ""),
        ]).lower()
        if "participant_pathway" not in text and "participant-pathway" not in text:
            continue
        ent = data.get("target_entity")
        if not ent:
            continue
        data["_path"] = str(path)
        data["_mtime"] = path.stat().st_mtime
        cards[ent] = data
    return cards

def response_section(entity_id: str, label: str, data: dict[str, Any] | None) -> str:
    if not data:
        return f"## {label}\n\nОтвет Сущности не найден.\n"
    txt = clean(data.get("response_text", ""))
    path = data.get("_path", "")
    model = data.get("model", "")
    return f"""## {label}

Источник:
{path}

Model:
{model}

Ответ Сущности:
{txt}
"""

def make_draft(cards: dict[str, dict[str, Any]]) -> str:
    return f"""# participant-pathway-canon.md — draft v01

## Статус

Черновик. Не утверждено.

Основание:
ответы локальных Сущностей через log16-agent-runner-v01.

Дата сборки:
{now()}

## Краткий смысл

Новый участник проекта должен находить своё поле деятельности не через свободное блуждание по проекту, а через управляемый маршрут:

1. первичный контакт;
2. первичная диагностика;
3. первая безопасная задача;
4. наблюдение за результатом;
5. предложение нескольких направлений;
6. закрепление в подходящем контуре;
7. дальнейшее обучение и проверка полезного вклада.

## Рабочий маршрут участника

### 1. Первичный контакт

Участник сообщает:
- чем интересуется;
- что умеет;
- сколько времени готов уделять;
- какие устройства и инструменты у него есть;
- какие ограничения есть по связи, грамотности, опыту, здоровью, быту.

Задача проекта на этом этапе — не обещать участнику результат, а понять, может ли он выполнить простое полезное действие.

### 2. Первичная диагностика

ВХОДНОЙ НАСТАВНИК должен выяснить:
- уровень самостоятельности;
- способность читать и выполнять простую инструкцию;
- способность прислать файл, скриншот, текст, голосовое сообщение;
- интерес к текстам, поиску информации, общению, техническим действиям, обучению, организации;
- готовность доводить маленькую задачу до результата.

### 3. Первая безопасная задача

Первая задача должна быть:
- короткой;
- понятной;
- без доступа к чувствительным данным;
- без финансовых обещаний;
- проверяемой;
- полезной для проекта даже в малом объёме.

Примеры:
- написать короткий текст о себе;
- прочитать материал и ответить на 3 вопроса;
- сделать скриншот и прислать его по инструкции;
- найти и переслать одну ссылку по заданной теме;
- оформить простой файл;
- дать короткую рецензию на публикацию.

### 4. Наблюдение за результатом

Оценивается не “талант вообще”, а конкретное поведение:
- понял ли задачу;
- задал ли уточняющий вопрос;
- смог ли выполнить;
- не начал ли фантазировать;
- уложился ли в понятный срок;
- можно ли дать следующую задачу.

### 5. Предложение направлений

После первой задачи участнику можно предложить 2–3 возможных поля деятельности:

- медийные задачи;
- обучение и рецензирование;
- сбор и проверка информации;
- технические простые действия;
- помощь другим участникам;
- организационные поручения;
- тестирование инструкций;
- участие в обсуждениях.

### 6. Закрепление в поле деятельности

Участник закрепляется не по заявлению “хочу быть полезным”, а по серии маленьких результатов.

Критерии закрепления:
- есть 2–3 выполненные задачи;
- виден устойчивый интерес;
- есть понятный тип полезного действия;
- есть Сущность, которая может вести участника дальше;
- результат можно учитывать в системе проекта.

### 7. Переход к обучению и участию

ШКОЛА подключается, когда видно:
- чему участника нужно доучить;
- какие задачи ему подходят;
- какие инструкции надо упростить;
- какие ошибки повторяются;
- может ли участник перейти от пробных задач к регулярному участию.

## Роли Сущностей

### КООРДИНАТОР

КООРДИНАТОР отвечает за:
- общую схему маршрута;
- связь между Сущностями;
- назначение ответственных;
- постановку задач по пробелам;
- фиксацию решений, которые должен принять ОПЕРАТОР.

### ВХОДНОЙ НАСТАВНИК

ВХОДНОЙ НАСТАВНИК отвечает за:
- первичную диагностику;
- первые безопасные задачи;
- наблюдение за результатом;
- первичную рекомендацию поля деятельности.

### ШКОЛА

ШКОЛА отвечает за:
- учебно-практический маршрут;
- задания для развития навыков;
- переход от обучения к полезному участию;
- критерии готовности.

### КОНСУЛЬТАНТ

КОНСУЛЬТАНТ отвечает за:
- сборку ответов в канон;
- выявление противоречий;
- формирование вопросов автору;
- подготовку review для log16.

## Решения, которые должен принять ОПЕРАТОР

1. Какие поля деятельности считать стартовыми для новых участников.
2. Какие первые задачи допустимы без риска для проекта.
3. Какой минимальный результат считать полезным.
4. Кто принимает решение о закреплении участника.
5. Как фиксировать результат участника в системе проекта.
6. Какие обещания участнику запрещены на входе.
7. Какой уровень автоматизации допустим при первичной диагностике.

## Открытые вопросы

1. Нужна ли единая анкета первичного контакта?
2. Какие стартовые задания должны быть утверждены первыми?
3. Как связывать путь участника с будущей учётной системой WBN/WBNP?
4. Кто владеет participant-pathway-canon.md: КООРДИНАТОР, ШКОЛА или КОНСУЛЬТАНТ?
5. Какой минимум результата нужен, чтобы участник перестал быть “новым”?
6. Как обрабатывать участников, которые хотят быстрых денег, но не готовы к задачам?
7. Как фиксировать отказ, паузу или неподходящее поле деятельности без конфликта?

## Следующие log16 карточки

- task: утвердить список стартовых полей деятельности;
- task: утвердить 5–7 первых безопасных задач;
- task: подготовить первичную анкету участника;
- task: описать критерии закрепления участника;
- review: проверить этот draft КООРДИНАТОРОМ и ОПЕРАТОРОМ;
- approved_answer candidate: краткий ответ “как участник находит поле деятельности”.

## Приложение: ответы Сущностей

{response_section("koordinator", "КООРДИНАТОР", cards.get("koordinator"))}

{response_section("vhodnoy-nastavnik", "ВХОДНОЙ НАСТАВНИК", cards.get("vhodnoy-nastavnik"))}

{response_section("shkola", "ШКОЛА", cards.get("shkola"))}

{response_section("consultant", "КОНСУЛЬТАНТ", cards.get("consultant"))}

## Служебный хвост

КТО: КОНСУЛЬТАНТ / log16-synthesize-participant-pathway.py
КОГДА: {now()}
ДЛЯ ЧЕГО: собрать первый draft participant-pathway-canon.md из entity_response cards
СТАТУС: needs_operator_review
"""

def make_operator_questions(cards: dict[str, dict[str, Any]]) -> str:
    return f"""# Operator decision questions — participant_pathway

## Кратко

Для превращения draft в канон ОПЕРАТОРу нужно принять несколько решений.

## Вопросы к ОПЕРАТОРУ

1. Какие стартовые поля деятельности участника считаем базовыми?
   - медийное;
   - учебное;
   - информационный поиск;
   - технические простые задачи;
   - организационная помощь;
   - тестирование инструкций;
   - другое.

2. Какие первые задачи можно давать участнику без риска?

3. Должна ли быть единая анкета первичного контакта?

4. Кто принимает решение о закреплении участника:
   - ВХОДНОЙ НАСТАВНИК;
   - КООРДИНАТОР;
   - ШКОЛА;
   - ОПЕРАТОР;
   - связка Сущностей?

5. Что считать минимальным полезным результатом?

6. Как фиксировать результат:
   - файл;
   - карточка log16;
   - запись в учётной системе;
   - будущая WBN/WBNP связка?

7. Какие обещания участнику запрещены на входе?

8. Когда участник переходит из статуса “новый” в статус “закреплён в контуре”?

## Рекомендация

Не утверждать весь канон сразу. Сначала утвердить:
- список первых безопасных задач;
- первичную анкету;
- критерии первой оценки результата.

КТО: КОНСУЛЬТАНТ / log16-synthesize-participant-pathway.py
КОГДА: {now()}
ДЛЯ ЧЕГО: вопросы ОПЕРАТОРУ для утверждения participant_pathway
СТАТУС: needs_operator_decision
"""

def main():
    cards = latest_responses()
    stamp_value = stamp()
    out = SYN / f"synthesis-{stamp_value}"
    out.mkdir(parents=True, exist_ok=True)

    draft_path = out / "participant-pathway-canon-draft.md"
    operator_path = out / "operator-decision-questions.md"
    report_path = out / "synthesis-report.md"
    manifest_path = out / "manifest.json"

    draft_path.write_text(make_draft(cards), encoding="utf-8")
    operator_path.write_text(make_operator_questions(cards), encoding="utf-8")

    manifest = {
        "package_id": f"CONS__participant-pathway-synthesis-{stamp_value}__OPR",
        "root": str(ROOT),
        "responses_found": sorted(cards.keys()),
        "draft": str(draft_path),
        "operator_questions": str(operator_path),
        "status": "PASS" if cards else "NO_RESPONSES",
        "created_at": now()
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    report_path.write_text(f"""# participant_pathway synthesis report

Status:
{manifest["status"]}

Responses found:
{", ".join(sorted(cards.keys())) if cards else "none"}

Created:
- {draft_path}
- {operator_path}
- {manifest_path}

Human next action:
1. Открыть operator-decision-questions.md.
2. Ответить на решения ОПЕРАТОРА.
3. После этого доработать participant-pathway-canon-draft.md.
4. Не считать draft утверждённым каноном.

КТО: КОНСУЛЬТАНТ
ДЛЯ ЧЕГО: отчёт сборки participant_pathway из entity_response cards
СТАТУС: generated
""", encoding="utf-8")

    archive = OUTBOX / f"CONS__participant-pathway-synthesis-{stamp_value}__OPR.tgz"
    with tarfile.open(archive, "w:gz") as tar:
        for p in sorted(out.rglob("*")):
            tar.add(p, arcname=f"CONS__participant-pathway-synthesis-{stamp_value}__OPR/{p.relative_to(out)}")

    print("PASS participant_pathway synthesis generated" if cards else "WARN participant_pathway synthesis generated without responses")
    print(f"RESPONSES_FOUND: {len(cards)}")
    for ent in sorted(cards):
        print(f"- {ent}: {cards[ent].get('_path')}")
    print(f"DRAFT: {draft_path}")
    print(f"OPERATOR_QUESTIONS: {operator_path}")
    print(f"REPORT: {report_path}")
    print(f"ARCHIVE: {archive}")

if __name__ == "__main__":
    main()
