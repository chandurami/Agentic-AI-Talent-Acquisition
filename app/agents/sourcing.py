from __future__ import annotations

from pathlib import Path
from typing import List

from ..data_models import Candidate
from ..parsing import parse_candidate_folder


class SourcingAgent:
    def run(self, candidate_dir: Path) -> List[Candidate]:
        return parse_candidate_folder(candidate_dir)

