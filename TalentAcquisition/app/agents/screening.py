from __future__ import annotations

from typing import List

import numpy as np

from ..data_models import Candidate, MatchResult, Role
from ..embeddings import build_index
from ..scoring import explain_fit


class ScreeningAgent:
    def rank_candidates(self, candidates: List[Candidate], role: Role) -> List[MatchResult]:
        if not candidates:
            return []
        ids = [c.id for c in candidates]
        texts = [c.resume_text for c in candidates]
        index = build_index(ids, texts)
        role_text = " ".join(
            role.required_skills + role.preferred_skills + role.research_focus + role.teaching_requirements
        )
        sims = index.query([role_text])[0]
        order = list(np.argsort(-sims))
        results: List[MatchResult] = []
        for i in order:
            c = candidates[i]
            strengths, risks = explain_fit(c, role)
            score = float(sims[i])
            next_steps = ["Invite to interview"] if score >= 0.2 and len(risks) <= len(strengths) else ["Needs follow-up"]
            results.append(
                MatchResult(
                    candidate_id=c.id,
                    role_id=role.id,
                    fit_score=round(score, 4),
                    strengths=strengths,
                    risks=risks,
                    next_steps=next_steps,
                )
            )
        return results

