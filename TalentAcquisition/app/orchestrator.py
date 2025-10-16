from __future__ import annotations

from pathlib import Path
from typing import Dict, List

from .agents.development import DevelopmentAgent
from .agents.interview import InterviewAgent
from .agents.screening import ScreeningAgent
from .agents.sourcing import SourcingAgent
from .agents.onboarding import OnboardingAgent
from .config import CONFIG
from .data_models import Candidate, DevelopmentPlan, MatchResult, Role, role_from_yaml
from .reports.generator import generate_reports


class Orchestrator:
    def __init__(self) -> None:
        self.sourcing = SourcingAgent()
        self.screening = ScreeningAgent()
        self.interview = InterviewAgent()
        self.onboarding = OnboardingAgent()
        self.development = DevelopmentAgent()

    def run(self, role_file: Path, data_dir: Path, out_dir: Path) -> Path:
        role = role_from_yaml(role_file)
        candidates = self.sourcing.run(candidate_dir=data_dir / "candidates")
        matches = self.screening.rank_candidates(candidates, role)
        development_plans: Dict[str, DevelopmentPlan] = {
            c.id: self.development.recommend(c) for c in candidates
        }
        generate_reports(out_dir, role, candidates, matches, development_plans)
        return out_dir / "report.json"

    def interview_questions(self, role: Role) -> List[str]:
        return self.interview.generate_questions(role)

    def onboarding_plan(self, role: Role) -> List[str]:
        return self.onboarding.plan(role.department)

