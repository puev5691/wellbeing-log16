from __future__ import annotations

import json
import shutil
import subprocess
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from log16.config import load_config
from log16.health.checks import checks_to_dict, run_checks


@dataclass
class DoctorItem:
    name: str
    status: str
    detail: str

    @property
    def ok(self) -> bool:
        return self.status in {"ok", "info", "warn"}


@dataclass
class DoctorResult:
    repo: str
    runtime: str
    ollama_url: str
    model: str
    items: list[DoctorItem]

    @property
    def failures(self) -> int:
        return sum(1 for item in self.items if item.status == "fail")

    @property
    def warnings(self) -> int:
        return sum(1 for item in self.items if item.status == "warn")

    @property
    def status(self) -> str:
        if self.failures:
            return "FAIL"
        if self.warnings:
            return "WARN"
        return "OK"

    @property
    def ok(self) -> bool:
        return self.failures == 0


def _run(command: list[str], cwd: Path | None = None, timeout: int = 10) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=str(cwd) if cwd else None,
        text=True,
        capture_output=True,
        timeout=timeout,
    )


def _short(text: str, limit: int = 500) -> str:
    cleaned = " ".join((text or "").strip().split())
    if len(cleaned) > limit:
        return cleaned[: limit - 3] + "..."
    return cleaned


def run_doctor(
    repo: str | None = None,
    runtime: str | None = None,
    ollama_url: str = "http://127.0.0.1:11434",
    model: str = "qwen3:8b",
    include_ollama: bool = True,
    include_prepublish: bool = True,
    include_bins: bool = True,
) -> DoctorResult:
    cfg = load_config()
    repo_path = Path(repo) if repo else cfg.repo_root
    runtime_path = Path(runtime) if runtime else cfg.runtime_root

    items: list[DoctorItem] = []

    for cmd in ["bash", "git", "python3", "curl"]:
        found = shutil.which(cmd)
        if found:
            items.append(DoctorItem(f"cmd_{cmd}", "ok", found))
        else:
            items.append(DoctorItem(f"cmd_{cmd}", "fail", "not found"))

    if (repo_path / ".git").exists():
        items.append(DoctorItem("repo_git", "ok", str(repo_path)))
        status = _run(["git", "status", "--short"], cwd=repo_path)
        if status.returncode == 0:
            if status.stdout.strip():
                items.append(DoctorItem("repo_status", "warn", _short(status.stdout)))
            else:
                items.append(DoctorItem("repo_status", "ok", "clean"))
        else:
            items.append(DoctorItem("repo_status", "fail", _short(status.stderr or status.stdout)))
    else:
        items.append(DoctorItem("repo_git", "fail", f"missing .git: {repo_path}"))

    if include_prepublish:
        pre = repo_path / "scripts" / "github-prepublish-check.sh"
        if pre.exists():
            proc = _run([str(pre)], cwd=repo_path, timeout=30)
            if proc.returncode == 0:
                items.append(DoctorItem("prepublish_check", "ok", "passed"))
            else:
                items.append(DoctorItem("prepublish_check", "warn", _short(proc.stdout or proc.stderr)))
        else:
            items.append(DoctorItem("prepublish_check", "warn", "script missing"))

    health = checks_to_dict(run_checks(root=str(runtime_path), include_bins=include_bins))
    for check in health.get("checks", []):
        status = "ok" if check.get("ok") else "fail"
        items.append(DoctorItem(f"health_{check.get('name')}", status, str(check.get("detail"))))

    if include_ollama:
        try:
            with urllib.request.urlopen(f"{ollama_url.rstrip('/')}/api/tags", timeout=3) as response:
                payload = response.read().decode("utf-8", errors="replace")
            data = json.loads(payload)
            names = []
            for item in data.get("models", []):
                name = item.get("name") or item.get("model")
                if name:
                    names.append(name)
            items.append(DoctorItem("ollama_api", "ok", f"{ollama_url}/api/tags"))
            if model in names:
                items.append(DoctorItem("ollama_model", "ok", model))
            else:
                items.append(DoctorItem("ollama_model", "warn", f"{model} not found; available: {', '.join(names)}"))
        except Exception as exc:
            items.append(DoctorItem("ollama_api", "warn", f"{type(exc).__name__}: {exc}"))

    try:
        usage = shutil.disk_usage(runtime_path if runtime_path.exists() else repo_path)
        free_gb = usage.free / (1024 ** 3)
        total_gb = usage.total / (1024 ** 3)
        items.append(DoctorItem("disk", "info", f"free={free_gb:.1f}GiB total={total_gb:.1f}GiB"))
    except Exception as exc:
        items.append(DoctorItem("disk", "warn", f"{type(exc).__name__}: {exc}"))

    ss = shutil.which("ss")
    if ss:
        proc = _run([ss, "-ltn"], timeout=10)
        if proc.returncode == 0:
            hits = []
            for line in proc.stdout.splitlines():
                if any(port in line for port in [":11434", ":8898", ":8794"]):
                    hits.append(line.strip())
            items.append(DoctorItem("ports", "info", " | ".join(hits) if hits else "no related listening ports"))
        else:
            items.append(DoctorItem("ports", "warn", _short(proc.stderr or proc.stdout)))
    else:
        items.append(DoctorItem("ports", "warn", "ss not found"))

    return DoctorResult(
        repo=str(repo_path),
        runtime=str(runtime_path),
        ollama_url=ollama_url,
        model=model,
        items=items,
    )


def doctor_to_dict(result: DoctorResult) -> dict[str, Any]:
    return {
        "ok": result.ok,
        "status": result.status,
        "failures": result.failures,
        "warnings": result.warnings,
        "repo": result.repo,
        "runtime": result.runtime,
        "ollama_url": result.ollama_url,
        "model": result.model,
        "checks": [
            {
                "name": item.name,
                "status": item.status,
                "ok": item.ok,
                "detail": item.detail,
            }
            for item in result.items
        ],
    }
