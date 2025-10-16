from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable, List

import json


def read_text_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def list_files(directory: Path, exts: Iterable[str]) -> List[Path]:
    exts_lower = {e.lower() for e in exts}
    return [p for p in directory.rglob("*") if p.suffix.lower() in exts_lower]


def load_json(path: Path) -> Dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: Dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")

