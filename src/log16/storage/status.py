from __future__ import annotations

from pathlib import Path

from log16.storage.layout import RuntimeLayout

def count_json(path: str | Path) -> int:
    p = Path(path)
    return len(list(p.glob("*.json"))) if p.exists() else 0

def count_dirs(path: str | Path) -> int:
    p = Path(path)
    return len([x for x in p.iterdir() if x.is_dir()]) if p.exists() else 0

def status_counts(layout: RuntimeLayout) -> dict[str, int]:
    return {
        "themes": count_json(layout.themes_captured),
        "tasks_proposed": count_json(layout.tasks_proposed),
        "tasks_routed": count_json(layout.tasks_routed),
        "tasks_dispatched": count_json(layout.tasks_dispatched),
        "tasks_done": count_json(layout.tasks_done),
        "requests_pending": count_json(layout.requests_pending),
        "requests_done": count_json(layout.requests_done),
        "responses_review": count_json(layout.responses_needs_review),
        "responses_approved": count_json(layout.responses_approved),
        "responses_revision": count_json(layout.responses_revision_requested),
        "responses_rejected": count_json(layout.responses_rejected),
        "responses_failed": count_json(layout.responses_failed),
        "runner_reports": count_dirs(layout.root / "runner-reports"),
        "pult_runs": count_dirs(layout.root / "pult-runs"),
    }
