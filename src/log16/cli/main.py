from __future__ import annotations

import argparse
import json
import os
import subprocess
from pathlib import Path
from typing import Sequence

from log16.config import load_config
from log16.health.checks import checks_to_dict, run_checks
from log16.review.decisions import VALID_DECISIONS, apply_review_decision
from log16.storage.layout import RuntimeLayout
from log16.storage.status import status_counts

def make_layout(root: str | None = None) -> RuntimeLayout:
    if root:
        return RuntimeLayout(Path(root))
    return RuntimeLayout(load_config().runtime_root)

def run_external(command: list[str]) -> int:
    proc = subprocess.run(command)
    return int(proc.returncode)

def pult_path(layout: RuntimeLayout) -> Path:
    return layout.root / "bin" / "log16-pult"

def dashboard_path(layout: RuntimeLayout) -> Path:
    return layout.root / "bin" / "log16-dashboard.sh"

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

def cmd_check(args: argparse.Namespace) -> int:
    checks = run_checks(
        root=args.root,
        include_bins=not args.skip_bins,
        dashboard_url=args.dashboard_url,
    )
    data = checks_to_dict(checks)
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(f"ok: {data['ok']}")
        for item in data["checks"]:
            status = "OK" if item["ok"] else "FAIL"
            print(f"{status}: {item['name']} -> {item['detail']}")
    return 0 if data["ok"] else 1

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

def cmd_pult(args: argparse.Namespace) -> int:
    layout = make_layout(args.root)
    extra = list(args.args or [])
    if extra and extra[0] == "--":
        extra = extra[1:]
    return run_external([str(pult_path(layout)), *extra])

def cmd_answer(args: argparse.Namespace) -> int:
    layout = make_layout(args.root)
    return run_external([str(pult_path(layout)), "answer", args.text])

def cmd_tasks(args: argparse.Namespace) -> int:
    layout = make_layout(args.root)
    return run_external([str(pult_path(layout)), "tasks", args.text])

def cmd_run_pending(args: argparse.Namespace) -> int:
    layout = make_layout(args.root)
    return run_external([str(pult_path(layout)), "run-pending"])

def cmd_latest(args: argparse.Namespace) -> int:
    layout = make_layout(args.root)
    return run_external([str(pult_path(layout)), "latest"])

def cmd_cleanup(args: argparse.Namespace) -> int:
    layout = make_layout(args.root)
    return run_external([str(pult_path(layout)), "cleanup"])

def cmd_dashboard(args: argparse.Namespace) -> int:
    layout = make_layout(args.root)
    return run_external([str(dashboard_path(layout))])


def cmd_doctor(args: argparse.Namespace) -> int:
    cfg = load_config()
    script = cfg.repo_root / "scripts" / "log16-doctor-readonly.sh"

    if not script.exists():
        print(f"doctor script missing: {script}")
        return 2

    env = os.environ.copy()
    if args.repo:
        env["LOG16_REPO"] = args.repo
    if args.runtime:
        env["LOG16_RUNTIME"] = args.runtime
    if args.ollama_url:
        env["LOG16_OLLAMA_URL"] = args.ollama_url
    if args.model:
        env["LOG16_MODEL"] = args.model

    proc = subprocess.run([str(script)], env=env)
    return int(proc.returncode)

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="log16", description="Unified CLI for wellbeing-log16")
    sub = parser.add_subparsers(dest="command", required=True)

    p_paths = sub.add_parser("paths", help="show resolved log16 paths")
    p_paths.set_defaults(func=cmd_paths)

    p_status = sub.add_parser("status", help="show runtime status counts")
    p_status.add_argument("--root", help="runtime root override")
    p_status.add_argument("--json", action="store_true", help="print JSON")
    p_status.set_defaults(func=cmd_status)

    p_check = sub.add_parser("check", help="run health checks")
    p_check.add_argument("--root", help="runtime root override")
    p_check.add_argument("--json", action="store_true", help="print JSON")
    p_check.add_argument("--skip-bins", action="store_true", help="skip critical bin checks")
    p_check.add_argument("--dashboard-url", help="optional dashboard URL check")
    p_check.set_defaults(func=cmd_check)

    p_doctor = sub.add_parser("doctor", help="run read-only environment doctor")
    p_doctor.add_argument("--repo", help="repo root override")
    p_doctor.add_argument("--runtime", help="runtime root override")
    p_doctor.add_argument("--ollama-url", help="Ollama API URL override")
    p_doctor.add_argument("--model", help="required model override")
    p_doctor.set_defaults(func=cmd_doctor)

    p_review = sub.add_parser("review-apply", help="apply review decision to a response card")
    p_review.add_argument("--root", help="runtime root override")
    p_review.add_argument("--card", required=True, help="path to response card JSON")
    p_review.add_argument("--decision", required=True, choices=sorted(VALID_DECISIONS))
    p_review.add_argument("--operator-text", default="", help="edited response text")
    p_review.add_argument("--operator-text-file", help="file with edited response text")
    p_review.add_argument("--operator-note", default="", help="operator note")
    p_review.add_argument("--reviewer", default="OPERATOR/log16-cli")
    p_review.set_defaults(func=cmd_review_apply)

    p_pult = sub.add_parser("pult", help="bridge to legacy log16-pult")
    p_pult.add_argument("--root", help="runtime root override")
    p_pult.add_argument("args", nargs=argparse.REMAINDER, help="arguments passed to log16-pult")
    p_pult.set_defaults(func=cmd_pult)

    p_answer = sub.add_parser("answer", help="bridge: log16-pult answer TEXT")
    p_answer.add_argument("--root", help="runtime root override")
    p_answer.add_argument("text")
    p_answer.set_defaults(func=cmd_answer)

    p_tasks = sub.add_parser("tasks", help="bridge: log16-pult tasks TEXT")
    p_tasks.add_argument("--root", help="runtime root override")
    p_tasks.add_argument("text")
    p_tasks.set_defaults(func=cmd_tasks)

    p_run = sub.add_parser("run-pending", help="bridge: log16-pult run-pending")
    p_run.add_argument("--root", help="runtime root override")
    p_run.set_defaults(func=cmd_run_pending)

    p_latest = sub.add_parser("latest", help="bridge: log16-pult latest")
    p_latest.add_argument("--root", help="runtime root override")
    p_latest.set_defaults(func=cmd_latest)

    p_cleanup = sub.add_parser("cleanup", help="bridge: log16-pult cleanup")
    p_cleanup.add_argument("--root", help="runtime root override")
    p_cleanup.set_defaults(func=cmd_cleanup)

    p_dashboard = sub.add_parser("dashboard", help="start dashboard through unified CLI")
    p_dashboard.add_argument("--root", help="runtime root override")
    p_dashboard.set_defaults(func=cmd_dashboard)

    return parser

def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))

if __name__ == "__main__":
    raise SystemExit(main())
