from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class Candidate:
    id: str
    name: str
    email: Optional[str]
    resume_text: str
    skills: List[str] = field(default_factory=list)
    research_areas: List[str] = field(default_factory=list)
    teaching_experience: List[str] = field(default_factory=list)
    publications: List[str] = field(default_factory=list)
    metadata: Dict[str, str] = field(default_factory=dict)


@dataclass
class Role:
    id: str
    title: str
    department: str
    required_skills: List[str]
    preferred_skills: List[str] = field(default_factory=list)
    research_focus: List[str] = field(default_factory=list)
    teaching_requirements: List[str] = field(default_factory=list)


@dataclass
class MatchResult:
    candidate_id: str
    role_id: str
    fit_score: float
    strengths: List[str]
    risks: List[str]
    next_steps: List[str]


@dataclass
class DevelopmentPlan:
    candidate_id: str
    goals: List[str]
    recommendations: List[str]


def role_from_yaml(path: Path) -> Role:
    import yaml

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return Role(
        id=data.get("id") or path.stem,
        title=data["title"],
        department=data.get("department", ""),
        required_skills=data.get("required_skills", []),
        preferred_skills=data.get("preferred_skills", []),
        research_focus=data.get("research_focus", []),
        teaching_requirements=data.get("teaching_requirements", []),
    )

