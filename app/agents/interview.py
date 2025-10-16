from __future__ import annotations

from typing import Dict, List

from ..data_models import Candidate, Role


class InterviewAgent:
    def generate_questions(self, role: Role) -> List[str]:
        qs = [
            f"Describe your research vision in {role.department} over the next 3 years.",
            "Tell us about a time you improved student learning outcomes.",
            "How do you integrate diversity, equity, and inclusion in teaching and mentorship?",
        ]
        for s in role.required_skills[:3]:
            qs.append(f"Deep dive: {s} — can you discuss a relevant project?")
        return qs

    def evaluate_transcript(self, transcript: str) -> Dict[str, float]:
        # very simple heuristic evaluation
        pos = sum(w in transcript.lower() for w in ["impact", "students", "research", "collaborate", "community"])  # noqa: E501
        neg = sum(w in transcript.lower() for w in ["don't know", "no idea", "not sure"])  # noqa: E501
        score = max(0.0, min(1.0, 0.5 + 0.1 * (pos - neg)))
        return {"communication": score, "research_vision": score, "teaching_philosophy": score}

