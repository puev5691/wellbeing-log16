from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

JsonObject = dict[str, Any]

def read_json(path: str | Path) -> JsonObject:
    p = Path(path)
    return json.loads(p.read_text(encoding="utf-8"))

def safe_read_json(path: str | Path) -> JsonObject | None:
    try:
        return read_json(path)
    except Exception:
        return None

def write_json(path: str | Path, data: JsonObject) -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return p

def list_json_cards(directory: str | Path) -> list[Path]:
    d = Path(directory)
    if not d.exists():
        return []
    return sorted(p for p in d.glob("*.json") if p.is_file())

def move_card(src: str | Path, dst_dir: str | Path, updates: JsonObject | None = None) -> Path:
    src_path = Path(src)
    dst = Path(dst_dir)
    dst.mkdir(parents=True, exist_ok=True)

    data = read_json(src_path)
    if updates:
        data.update(updates)

    dst_path = dst / src_path.name
    write_json(dst_path, data)
    src_path.unlink()
    return dst_path

def copy_card(src: str | Path, dst_dir: str | Path, updates: JsonObject | None = None) -> Path:
    src_path = Path(src)
    dst = Path(dst_dir)
    dst.mkdir(parents=True, exist_ok=True)

    data = read_json(src_path)
    if updates:
        data.update(updates)

    dst_path = dst / src_path.name
    write_json(dst_path, data)
    return dst_path

def backup_file(src: str | Path, backup_dir: str | Path) -> Path:
    src_path = Path(src)
    dst = Path(backup_dir)
    dst.mkdir(parents=True, exist_ok=True)
    target = dst / src_path.name
    shutil.copy2(src_path, target)
    return target
