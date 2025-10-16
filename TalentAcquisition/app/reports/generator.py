from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Dict, List

from ..data_models import Candidate, DevelopmentPlan, MatchResult, Role
from ..utils.io import save_json


def candidate_summary(candidate: Candidate) -> Dict:
    return {
        "id": candidate.id,
        "name": candidate.name,
        "email": candidate.email,
        "skills": candidate.skills,
        "research_areas": candidate.research_areas,
        "teaching_experience": candidate.teaching_experience,
        "publications": candidate.publications,
    }


def generate_reports(
    out_dir: Path,
    role: Role,
    candidates: List[Candidate],
    matches: List[MatchResult],
    development_plans: Dict[str, DevelopmentPlan],
) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "role": asdict(role),
        "candidates": [candidate_summary(c) for c in candidates],
        "matches": [asdict(m) for m in matches],
        "development_plans": {cid: asdict(plan) for cid, plan in development_plans.items()},
    }
    save_json(out_dir / "report.json", payload)

