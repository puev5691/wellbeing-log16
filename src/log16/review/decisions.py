from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from time import strftime

from log16.storage.cards import move_card, read_json, write_json
from log16.storage.layout import RuntimeLayout

VALID_DECISIONS = {
    "approve_as_is",
    "approve_with_edit",
    "request_revision",
    "reject",
}

@dataclass(frozen=True)
class ReviewResult:
    review_id: str
    decision: str
    response_id: str
    response_target_path: Path
    review_json_path: Path
    review_md_path: Path
    reviewed_doc_path: Path | None

def now() -> str:
    return strftime("%Y-%m-%dT%H:%M:%S")

def stamp() -> str:
    return strftime("%Y%m%d-%H%M%S")

def target_dir_for_decision(layout: RuntimeLayout, decision: str) -> Path:
    if decision in {"approve_as_is", "approve_with_edit"}:
        return layout.responses_approved
    if decision == "request_revision":
        return layout.responses_revision_requested
    if decision == "reject":
        return layout.responses_rejected
    raise ValueError(f"unknown review decision: {decision}")

def apply_review_decision(
    response_card_path: str | Path,
    layout: RuntimeLayout,
    decision: str,
    operator_text: str = "",
    operator_note: str = "",
    reviewer: str = "OPERATOR",
) -> ReviewResult:
    if decision not in VALID_DECISIONS:
        raise ValueError(f"invalid decision: {decision}")

    response_path = Path(response_card_path)
    data = read_json(response_path)

    response_id = str(data.get("response_id") or response_path.stem)
    review_id = f"review__{stamp()}__{response_id}"

    reviewed_doc_path: Path | None = None
    if decision == "approve_with_edit":
        reviewed_doc_path = layout.reviewed_docs / f"{response_id}.md"
        reviewed_doc_path.parent.mkdir(parents=True, exist_ok=True)
        reviewed_doc_path.write_text(operator_text, encoding="utf-8")

    review_card = {
        "review_id": review_id,
        "response_id": response_id,
        "source_response_card": str(response_path),
        "decision": decision,
        "operator_note": operator_note,
        "reviewed_doc_path": str(reviewed_doc_path) if reviewed_doc_path else None,
        "created_at": now(),
        "created_by": reviewer,
    }

    review_json = layout.reviews / f"{review_id}.json"
    review_md = layout.reviews / f"{review_id}.md"
    write_json(review_json, review_card)

    review_md.write_text(
        "\n".join([
            f"# {review_id}",
            "",
            f"Decision: {decision}",
            f"Response: {response_id}",
            "",
            "Operator note:",
            operator_note,
            "",
            f"Reviewed doc: {reviewed_doc_path if reviewed_doc_path else 'none'}",
            f"Source response card: {response_path}",
            "",
            "КТО: ОПЕРАТОР / log16",
            "ДЛЯ ЧЕГО: фиксация решения review по response card",
            f"СТАТУС: {decision}",
            "",
        ]),
        encoding="utf-8",
    )

    updates = {
        "review_status": decision,
        "review_id": review_id,
        "reviewed_at": now(),
        "operator_note": operator_note,
    }
    if reviewed_doc_path:
        updates["reviewed_doc_path"] = str(reviewed_doc_path)

    target_path = move_card(response_path, target_dir_for_decision(layout, decision), updates)

    return ReviewResult(
        review_id=review_id,
        decision=decision,
        response_id=response_id,
        response_target_path=target_path,
        review_json_path=review_json,
        review_md_path=review_md,
        reviewed_doc_path=reviewed_doc_path,
    )
