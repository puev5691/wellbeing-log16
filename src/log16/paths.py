from __future__ import annotations

import os
from pathlib import Path

DEFAULT_RUNTIME_ROOT = Path("/data/wellbeing/obs/log16")
LEGACY_RUNTIME_ROOT = Path("/data/wellbeing/obs/consultant/outbox/log16-kernel")

def runtime_root() -> Path:
    return Path(os.environ.get("LOG16_ROOT", str(DEFAULT_RUNTIME_ROOT)))

def legacy_runtime_root() -> Path:
    return LEGACY_RUNTIME_ROOT

def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]
