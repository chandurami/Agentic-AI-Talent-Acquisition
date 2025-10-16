from __future__ import annotations

from typing import List, Tuple

from .data_models import Candidate, Role


def explain_fit(candidate: Candidate, role: Role) -> Tuple[List[str], List[str]]:
    strengths: List[str] = []
    risks: List[str] = []
    text = candidate.resume_text
    # simple keyword presence for explainability
    for s in role.required_skills:
        if s.lower() in text:
            strengths.append(f"Mentions required skill: {s}")
        else:
            risks.append(f"Missing required skill: {s}")
    for s in role.preferred_skills:
        if s.lower() in text:
            strengths.append(f"Mentions preferred skill: {s}")
    for a in role.research_focus:
        if a.lower() in text:
            strengths.append(f"Research focus alignment: {a}")
    for t in role.teaching_requirements:
        if t.lower() in text:
            strengths.append(f"Teaching alignment: {t}")
    return strengths, risks

