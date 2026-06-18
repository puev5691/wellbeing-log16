from __future__ import annotations

import urllib.request
from dataclasses import asdict, dataclass
from pathlib import Path

from log16.config import load_config
from log16.storage.layout import RuntimeLayout

@dataclass(frozen=True)
class CheckResult:
    name: str
    ok: bool
    detail: str

def check_path_exists(name: str, path: Path, kind: str = "any") -> CheckResult:
    if kind == "dir":
        ok = path.is_dir()
    elif kind == "file":
        ok = path.is_file()
    else:
        ok = path.exists()
    return CheckResult(name=name, ok=ok, detail=str(path))

def check_runtime_layout(layout: RuntimeLayout) -> list[CheckResult]:
    return [
        check_path_exists("runtime_root", layout.root, "dir"),
        check_path_exists("themes_captured", layout.themes_captured, "dir"),
        check_path_exists("tasks_dispatched", layout.tasks_dispatched, "dir"),
        check_path_exists("requests_pending", layout.requests_pending, "dir"),
        check_path_exists("requests_done", layout.requests_done, "dir"),
        check_path_exists("responses_needs_review", layout.responses_needs_review, "dir"),
        check_path_exists("responses_approved", layout.responses_approved, "dir"),
        check_path_exists("responses_revision_requested", layout.responses_revision_requested, "dir"),
        check_path_exists("reviews", layout.reviews, "dir"),
        check_path_exists("reviewed_docs", layout.reviewed_docs, "dir"),
        check_path_exists("runner_reports", layout.root / "runner-reports", "dir"),
    ]

def check_critical_bins(layout: RuntimeLayout) -> list[CheckResult]:
    return [
        check_path_exists("bin_log16", layout.root / "bin" / "log16", "file"),
        check_path_exists("bin_log16_pult", layout.root / "bin" / "log16-pult", "file"),
        check_path_exists("bin_log16_dashboard", layout.root / "bin" / "log16-dashboard.sh", "file"),
        check_path_exists("bin_log16_dashboard_py", layout.root / "bin" / "log16-dashboard.py", "file"),
    ]

def check_dashboard_url(url: str, timeout: float = 2.0) -> CheckResult:
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            code = getattr(response, "status", 0)
        return CheckResult(name="dashboard_url", ok=200 <= int(code) < 400, detail=f"{url} -> {code}")
    except Exception as e:
        return CheckResult(name="dashboard_url", ok=False, detail=f"{url} -> {type(e).__name__}: {e}")

def run_checks(
    root: str | Path | None = None,
    include_bins: bool = True,
    dashboard_url: str | None = None,
) -> list[CheckResult]:
    cfg = load_config()
    layout = RuntimeLayout(Path(root) if root else cfg.runtime_root)

    checks = []
    checks.extend(check_runtime_layout(layout))
    if include_bins:
        checks.extend(check_critical_bins(layout))
    if dashboard_url:
        checks.append(check_dashboard_url(dashboard_url))
    return checks

def checks_to_dict(checks: list[CheckResult]) -> dict:
    return {
        "ok": all(c.ok for c in checks),
        "checks": [asdict(c) for c in checks],
    }
