"""Epistemic gate for log16.

This module does not try to answer broad project questions directly.
It classifies whether a question can be answered, whether evidence is
insufficient, and what information must be added to the file field.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field, asdict
from typing import Any

KNOWN_ANSWER = "KNOWN_ANSWER"
PARTIAL_ANSWER = "PARTIAL_ANSWER"
INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"
NEEDS_FILE_FIELD = "NEEDS_FILE_FIELD"
NEEDS_ENTITY_RESPONSE = "NEEDS_ENTITY_RESPONSE"
NEEDS_OPERATOR_DECISION = "NEEDS_OPERATOR_DECISION"
UNSUPPORTED_MODE = "UNSUPPORTED_MODE"


@dataclass
class EpistemicDecision:
    """Structured result of a knowledge-state check."""

    status: str
    answer_available: bool
    confidence: str
    short_answer: str
    reason: str
    missing_information: list[str] = field(default_factory=list)
    needed_file_field: list[str] = field(default_factory=list)
    suggested_actions: list[str] = field(default_factory=list)
    route: list[str] = field(default_factory=list)
    machine_note: str = "epistemic_gate_v01"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _contains_any(text: str, needles: list[str]) -> bool:
    return any(n in text for n in needles)


def evaluate_question(question: str) -> EpistemicDecision:
    """Evaluate whether log16 can answer a question with current evidence.

    v01 is deliberately conservative. It does not fabricate answers and does
    not perform full evidence lookup yet. It gives an explicit knowledge-state
    decision and routes broad questions toward file-field enrichment.
    """

    raw = (question or "").strip()
    text = raw.casefold()
    if not raw:
        return EpistemicDecision(
            status=UNSUPPORTED_MODE,
            answer_available=False,
            confidence="none",
            short_answer="Вопрос пустой.",
            reason="Нечего классифицировать.",
            suggested_actions=["Передать непустой вопрос."],
            route=["operator_input"],
        )

    file_field_terms = [
        "файлов", "файловое поле", "инвентаризац", "каталог", "каталоги",
        "архив", "архивариус", "obs", "repos", "документ", "источник",
    ]
    broad_question_terms = [
        "как ", "каким образом", "что делать", "план", "организ", "построить",
        "создать", "сформировать", "произвести", "разработать",
    ]
    entity_terms = ["сущност", "координатор", "архивариус", "консультант", "кодер", "шардовик"]
    decision_terms = ["утверд", "решить", "выбрать", "приоритет", "можно ли", "надо ли"]

    if _contains_any(text, file_field_terms) and _contains_any(text, broad_question_terms):
        return EpistemicDecision(
            status=NEEDS_FILE_FIELD,
            answer_available=False,
            confidence="low",
            short_answer="Я не могу дать проверяемый ответ: в файловом поле недостаточно подтверждённой информации.",
            reason="Вопрос требует карты файлового поля, критериев классификации и подтверждённых источников, а не прямого ответа.",
            missing_information=[
                "актуальная карта корневых каталогов проекта",
                "правила различения рабочих файлов, архивов, runtime-состояния, исходников, результатов и мусора",
                "список Сущностей-владельцев каталогов и зон ответственности",
                "критерии завершённости инвентаризации",
                "правила фиксации результата и передачи его Архивариусу/Координатору",
            ],
            needed_file_field=[
                "file-field-map-v01.md",
                "file-classification-policy-v01.md",
                "inventory-completion-criteria-v01.md",
                "entity-directory-ownership-map-v01.md",
            ],
            suggested_actions=[
                "создать file-field-request на пополнение файлового поля",
                "передать запрос Архивариусу на карту каталогов и правила классификации",
                "передать Координатору задачу согласовать критерии завершённости",
                "после появления источников повторить вопрос через evidence/synthesis pipeline",
            ],
            route=["epistemic_gate", "file_field_request", "archivarius", "koordinator", "review"],
        )

    if _contains_any(text, entity_terms) and _contains_any(text, broad_question_terms):
        return EpistemicDecision(
            status=NEEDS_ENTITY_RESPONSE,
            answer_available=False,
            confidence="low",
            short_answer="Нужен ответ профильной Сущности или подтверждённый файл от неё.",
            reason="Вопрос затрагивает распределение ответственности или содержание работы Сущностей.",
            missing_information=["актуальный ответ профильной Сущности", "подтверждённый route/task/status файл"],
            suggested_actions=["создать entity_request", "после ответа отправить результат на review"],
            route=["epistemic_gate", "entity_request", "review"],
        )

    if _contains_any(text, decision_terms):
        return EpistemicDecision(
            status=NEEDS_OPERATOR_DECISION,
            answer_available=False,
            confidence="medium",
            short_answer="Нужен выбор ОПЕРАТОРА или утверждённое проектное решение.",
            reason="Вопрос похож на решение, а не на извлечение знания из файлового поля.",
            missing_information=["критерий выбора", "границы решения", "ответственный за утверждение"],
            suggested_actions=["сформировать decision-request", "зафиксировать принятое решение в файловом поле"],
            route=["epistemic_gate", "operator_decision", "decision_record"],
        )

    if _contains_any(text, broad_question_terms):
        return EpistemicDecision(
            status=INSUFFICIENT_EVIDENCE,
            answer_available=False,
            confidence="low",
            short_answer="Я не знаю проверяемого ответа без поиска источников и уточнения файлового поля.",
            reason="Вопрос широкий и требует evidence lookup перед ответом.",
            missing_information=["релевантные источники", "границы применимости ответа", "критерии проверки"],
            suggested_actions=["создать evidence lookup task", "после сбора источников выполнить synthesis/review"],
            route=["epistemic_gate", "evidence_lookup", "synthesis", "review"],
        )

    return EpistemicDecision(
        status=PARTIAL_ANSWER,
        answer_available=False,
        confidence="low",
        short_answer="Недостаточно данных для уверенного прямого ответа.",
        reason="v01 не нашёл оснований считать вопрос поддержанным прямым ответом.",
        missing_information=["подтверждённый источник или уже утверждённая answer-card"],
        suggested_actions=["проверить наличие answer-card", "при отсутствии источника создать needs_file_field или evidence task"],
        route=["epistemic_gate", "answer_card_lookup", "needs_file_field"],
    )


def render_markdown(decision: EpistemicDecision, question: str) -> str:
    """Render a human-readable Russian decision."""

    lines: list[str] = []
    lines.append("# Проверка состояния знания")
    lines.append("")
    lines.append("## Вопрос")
    lines.append("")
    lines.append(question.strip() or "<пустой вопрос>")
    lines.append("")
    lines.append("## Краткий ответ")
    lines.append("")
    lines.append(decision.short_answer)
    lines.append("")
    lines.append("## Статус")
    lines.append("")
    lines.append(decision.status)
    lines.append("")
    lines.append("## Причина")
    lines.append("")
    lines.append(decision.reason)
    if decision.missing_information:
        lines.append("")
        lines.append("## Чего не хватает")
        lines.append("")
        for item in decision.missing_information:
            lines.append(f"- {item}")
    if decision.needed_file_field:
        lines.append("")
        lines.append("## Что нужно внести в файловое поле")
        lines.append("")
        for item in decision.needed_file_field:
            lines.append(f"- {item}")
    if decision.suggested_actions:
        lines.append("")
        lines.append("## Следующие действия")
        lines.append("")
        for item in decision.suggested_actions:
            lines.append(f"- {item}")
    if decision.route:
        lines.append("")
        lines.append("## Маршрут")
        lines.append("")
        lines.append(" → ".join(decision.route))
    lines.append("")
    lines.append("КТО: log16 epistemic_gate_v01")
    lines.append("ДЛЯ ЧЕГО: честная фиксация недостаточности знания перед ответом")
    lines.append(f"СТАТУС: {decision.status}")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="log16 epistemic gate v01")
    parser.add_argument("question", nargs="*", help="Question to evaluate")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of markdown")
    args = parser.parse_args(argv)

    question = " ".join(args.question).strip()
    decision = evaluate_question(question)
    if args.json:
        print(json.dumps(decision.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(render_markdown(decision, question), end="")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
