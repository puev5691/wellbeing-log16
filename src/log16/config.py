from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path

DEFAULT_REPO_ROOT = Path("/data/wellbeing/repos/wellbeing-log16")
DEFAULT_RUNTIME_ROOT = Path("/data/wellbeing/obs/log16")
DEFAULT_LEGACY_RUNTIME_ROOT = Path("/data/wellbeing/obs/consultant/outbox/log16-kernel")
DEFAULT_OUTBOX_ROOT = Path("/data/wellbeing/obs/consultant/outbox")

@dataclass(frozen=True)
class Log16Config:
    repo_root: Path
    runtime_root: Path
    legacy_runtime_root: Path
    outbox_root: Path
    mode: str = "lab"

def load_config() -> Log16Config:
    env_config = os.environ.get("LOG16_CONFIG")
    config_path = Path(env_config) if env_config else DEFAULT_REPO_ROOT / "config" / "paths.json"

    data = {}
    if config_path.exists():
        data = json.loads(config_path.read_text(encoding="utf-8"))

    return Log16Config(
        repo_root=Path(os.environ.get("LOG16_REPO", data.get("repo_root", str(DEFAULT_REPO_ROOT)))),
        runtime_root=Path(os.environ.get("LOG16_ROOT", data.get("runtime_root", str(DEFAULT_RUNTIME_ROOT)))),
        legacy_runtime_root=Path(os.environ.get("LOG16_LEGACY_ROOT", data.get("legacy_runtime_root", str(DEFAULT_LEGACY_RUNTIME_ROOT)))),
        outbox_root=Path(os.environ.get("LOG16_OUTBOX", data.get("outbox_root", str(DEFAULT_OUTBOX_ROOT)))),
        mode=str(data.get("mode", os.environ.get("LOG16_MODE", "lab"))),
    )

def runtime_root() -> Path:
    return load_config().runtime_root

def legacy_runtime_root() -> Path:
    return load_config().legacy_runtime_root

def outbox_root() -> Path:
    return load_config().outbox_root

def repo_root() -> Path:
    return load_config().repo_root
