from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class AppConfig:
    data_dir: Path = Path("data")
    output_dir: Path = Path("outputs")
    candidate_dir: Path = Path("data/candidates")
    roles_dir: Path = Path("data/roles")
    use_langchain: bool = False
    use_crewai: bool = False


CONFIG = AppConfig()

