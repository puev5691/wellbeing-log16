from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from log16.config import load_config
from log16.review.decisions import VALID_DECISIONS, apply_review_decision
from log16.storage.layout import RuntimeLayout
from log16.storage.status import status_counts

def make_layout(root: str | None = None) -> RuntimeLayout:
    if root:
        return RuntimeLayout(Path(root))
    return RuntimeLayout(load_config().runtime_root)

def cmd_paths(args: argparse.Namespace) -> int:
    cfg = load_config()
    data = {
        "repo_root": str(cfg.repo_root),
        "runtime_root": str(cfg.runtime_root),
        "legacy_runtime_root": str(cfg.legacy_runtime_root),
        "outbox_root": str(cfg.outbox_root),
        "mode": cfg.mode,
    }
    print(json.dumps(data, ensure_ascii=False, indent=2))
    return 0

def cmd_status(args: argparse.Namespace) -> int:
    layout = make_layout(args.root)
    counts = status_counts(layout)
    if args.json:
        print(json.dumps(counts, ensure_ascii=False, indent=2))
    else:
        for key in sorted(counts):
            print(f"{key}: {counts[key]}")
    return 0

def cmd_review_apply(args: argparse.Namespace) -> int:
    layout = make_layout(args.root)
    operator_text = args.operator_text or ""
    if args.operator_text_file:
        operator_text = Path(args.operator_text_file).read_text(encoding="utf-8")

    result = apply_review_decision(
        args.card,
        layout,
        decision=args.decision,
        operator_text=operator_text,
        operator_note=args.operator_note or "",
        reviewer=args.reviewer,
    )

    print(json.dumps({
        "review_id": result.review_id,
        "decision": result.decision,
        "response_id": result.response_id,
        "response_target_path": str(result.response_target_path),
        "review_json_path": str(result.review_json_path),
        "review_md_path": str(result.review_md_path),
        "reviewed_doc_path": str(result.reviewed_doc_path) if result.reviewed_doc_path else None,
    }, ensure_ascii=False, indent=2))
    return 0

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="log16", description="Unified CLI for wellbeing-log16")
    sub = parser.add_subparsers(dest="command", required=True)

    p_paths = sub.add_parser("paths", help="show resolved log16 paths")
    p_paths.set_defaults(func=cmd_paths)

    p_status = sub.add_parser("status", help="show runtime status counts")
    p_status.add_argument("--root", help="runtime root override")
    p_status.add_argument("--json", action="store_true", help="print JSON")
    p_status.set_defaults(func=cmd_status)

    p_review = sub.add_parser("review-apply", help="apply review decision to a response card")
    p_review.add_argument("--root", help="runtime root override")
    p_review.add_argument("--card", required=True, help="path to response card JSON")
    p_review.add_argument("--decision", required=True, choices=sorted(VALID_DECISIONS))
    p_review.add_argument("--operator-text", default="", help="edited response text")
    p_review.add_argument("--operator-text-file", help="file with edited response text")
    p_review.add_argument("--operator-note", default="", help="operator note")
    p_review.add_argument("--reviewer", default="OPERATOR/log16-cli")
    p_review.set_defaults(func=cmd_review_apply)

    return parser

def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))

if __name__ == "__main__":
    raise SystemExit(main())
