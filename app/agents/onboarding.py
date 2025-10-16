from __future__ import annotations

from typing import List


class OnboardingAgent:
    def plan(self, department: str) -> List[str]:
        return [
            "Complete HR paperwork",
            f"Meet department chair ({department})",
            "Get teaching resources and LMS access",
            "Assign mentorship pairing",
            "Schedule lab/safety orientation",
        ]

