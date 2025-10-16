from __future__ import annotations

from typing import List

from ..data_models import Candidate, DevelopmentPlan


class DevelopmentAgent:
    def recommend(self, candidate: Candidate) -> DevelopmentPlan:
        goals: List[str] = [
            "Publish in top-tier venues",
            "Enhance teaching effectiveness",
            "Expand interdisciplinary collaborations",
        ]
        recommendations: List[str] = [
            "Join pedagogy workshop series",
            "Identify a senior mentor for grant writing",
            "Present at departmental seminar",
        ]
        return DevelopmentPlan(candidate_id=candidate.id, goals=goals, recommendations=recommendations)

