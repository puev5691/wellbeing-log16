from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from log16.config import runtime_root

@dataclass(frozen=True)
class RuntimeLayout:
    root: Path

    @property
    def themes_captured(self) -> Path:
        return self.root / "themes" / "captured"

    @property
    def tasks_proposed(self) -> Path:
        return self.root / "tasks" / "proposed"

    @property
    def tasks_routed(self) -> Path:
        return self.root / "tasks" / "routed"

    @property
    def tasks_dispatched(self) -> Path:
        return self.root / "tasks" / "dispatched"

    @property
    def tasks_done(self) -> Path:
        return self.root / "tasks" / "done"

    @property
    def requests_pending(self) -> Path:
        return self.root / "requests" / "pending"

    @property
    def requests_running(self) -> Path:
        return self.root / "requests" / "running"

    @property
    def requests_done(self) -> Path:
        return self.root / "requests" / "done"

    @property
    def requests_failed(self) -> Path:
        return self.root / "requests" / "failed"

    @property
    def responses_needs_review(self) -> Path:
        return self.root / "responses" / "needs_review"

    @property
    def responses_approved(self) -> Path:
        return self.root / "responses" / "approved"

    @property
    def responses_revision_requested(self) -> Path:
        return self.root / "responses" / "revision_requested"

    @property
    def responses_rejected(self) -> Path:
        return self.root / "responses" / "rejected"

    @property
    def reviews(self) -> Path:
        return self.root / "reviews"

    @property
    def reviewed_docs(self) -> Path:
        return self.root / "reviewed-docs"

    @property
    def reports(self) -> Path:
        return self.root / "reports"

    @property
    def archives(self) -> Path:
        return self.root / "archives"

    def ensure(self) -> None:
        for path in [
            self.themes_captured,
            self.tasks_proposed,
            self.tasks_routed,
            self.tasks_dispatched,
            self.tasks_done,
            self.requests_pending,
            self.requests_running,
            self.requests_done,
            self.requests_failed,
            self.responses_needs_review,
            self.responses_approved,
            self.responses_revision_requested,
            self.responses_rejected,
            self.reviews,
            self.reviewed_docs,
            self.reports,
            self.archives,
            self.root / "var",
            self.root / "backups",
        ]:
            path.mkdir(parents=True, exist_ok=True)

def current_layout() -> RuntimeLayout:
    return RuntimeLayout(root=runtime_root())
