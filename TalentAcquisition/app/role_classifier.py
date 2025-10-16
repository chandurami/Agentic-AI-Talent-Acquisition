from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List


def _snake_case(text: str) -> str:
    return (
        text.strip()
        .replace("/", " ")
        .replace("-", " ")
        .replace("(", " ")
        .replace(")", " ")
        .replace(",", " ")
        .replace("&", " and ")
        .lower()
        .split()
    )


def title_to_id(title: str) -> str:
    return "_".join(_snake_case(title))


def infer_department(title: str) -> str:
    t = title.lower()
    if "data science" in t:
        return "Data Science"
    if "computer science" in t or "cs" in t:
        return "Computer Science"
    if "ai ethics" in t or ("ethics" in t and ("ai" in t or "artificial intelligence" in t)):
        # Interdisciplinary, closest academic home typically CS
        return "Computer Science"
    if "ai" in t or "artificial intelligence" in t:
        return "Artificial Intelligence"
    if "mathematics" in t or "statistics" in t:
        return "Mathematics"
    if "electrical" in t or "ece" in t:
        return "Electrical and Computer Engineering"
    if "finance" in t:
        return "Finance"
    if "economics" in t:
        return "Economics"
    if "marketing" in t:
        return "Marketing"
    if "accounting" in t:
        return "Accounting"
    if "psychology" in t:
        return "Psychology"
    if "biology" in t or "biological" in t:
        return "Biology"
    if "chemistry" in t or "chemical" in t:
        return "Chemistry"
    if "physics" in t:
        return "Physics"
    if "mechanical" in t:
        return "Mechanical Engineering"
    if "civil" in t:
        return "Civil Engineering"
    if "biomedical" in t:
        return "Biomedical Engineering"
    if "cybersecurity" in t or "security" in t:
        return "Cybersecurity"
    if "nlp" in t or "natural language" in t:
        return "Natural Language Processing"
    if "computer vision" in t or "vision" in t:
        return "Computer Vision"
    return "Academic Affairs"


def classify_role(title: str) -> Dict:
    department = infer_department(title)
    # Discipline-first templates to avoid generic placeholders
    templates: Dict[str, Dict[str, List[str]]] = {
        "Mechanical Engineering": {
            "required": ["thermodynamics", "mechanics of materials", "cad", "engineering design"],
            "preferred": ["finite element analysis", "robotics", "sustainable manufacturing"],
            "research": ["fluid dynamics", "heat transfer", "advanced manufacturing"],
            "teaching": ["undergraduate thermodynamics", "mechanical design labs", "capstone project supervision"],
        },
        "Mathematics": {
            "required": ["linear algebra", "calculus", "mathematical proofs", "statistics"],
            "preferred": ["numerical methods", "mathematical modeling", "topology"],
            "research": ["algebraic geometry", "probability theory", "applied mathematics"],
            "teaching": ["undergraduate calculus", "linear algebra courses", "graduate seminars in pure mathematics"],
        },
        "Finance": {
            "required": ["financial modeling", "quantitative analysis", "econometrics", "corporate finance"],
            "preferred": ["blockchain finance", "behavioral economics", "fintech"],
            "research": ["asset pricing", "risk management", "market microstructure"],
            "teaching": ["graduate-level finance", "investments", "financial econometrics"],
        },
        "Artificial Intelligence": {
            "required": ["machine learning", "python", "deep learning", "evaluation methodologies"],
            "preferred": ["deep reinforcement learning", "self-supervised learning"],
            "research": ["representation learning", "responsible ai", "foundation models"],
            "teaching": ["machine learning", "deep learning", "ml systems labs"],
        },
        "Computer Science": {
            "required": ["data structures", "algorithms", "software engineering", "databases"],
            "preferred": ["distributed systems", "computer networks", "security"],
            "research": ["software systems", "distributed computing", "program analysis"],
            "teaching": ["intro to cs", "data structures & algorithms", "software engineering project"],
        },
        "Natural Language Processing": {
            "required": ["nlp", "python", "machine learning", "text processing"],
            "preferred": ["transformers", "information retrieval"],
            "research": ["language modeling", "text mining", "multilingual nlp"],
            "teaching": ["nlp", "ml for text", "nlp project supervision"],
        },
        "Computer Vision": {
            "required": ["computer vision", "deep learning", "python"],
            "preferred": ["3d vision", "multimodal learning"],
            "research": ["object detection", "segmentation", "medical imaging"],
            "teaching": ["computer vision", "deep learning", "vision labs"],
        },
        "Cybersecurity": {
            "required": ["network security", "cryptography", "threat modeling"],
            "preferred": ["cloud security", "secure software"],
            "research": ["intrusion detection", "malware analysis", "privacy"],
            "teaching": ["information security", "cryptography", "secure coding labs"],
        },
        "Economics": {
            "required": ["microeconomics", "macroeconomics", "econometrics"],
            "preferred": ["development economics", "behavioral economics"],
            "research": ["applied microeconomics", "macro policy", "labor economics"],
            "teaching": ["econometrics", "intermediate micro/macro", "policy seminars"],
        },
        "Marketing": {
            "required": ["consumer behavior", "marketing analytics", "research methods"],
            "preferred": ["digital marketing", "causal inference"],
            "research": ["brand strategy", "digital platforms", "market design"],
            "teaching": ["marketing analytics", "consumer behavior", "digital marketing labs"],
        },
        "Accounting": {
            "required": ["financial accounting", "auditing", "data analysis"],
            "preferred": ["forensic accounting", "tax policy"],
            "research": ["disclosure", "earnings quality", "audit quality"],
            "teaching": ["financial accounting", "auditing", "case-based seminars"],
        },
        "Biology": {
            "required": ["molecular biology", "experimental design", "biostatistics"],
            "preferred": ["genomics", "single-cell analysis"],
            "research": ["cell biology", "genetics", "systems biology"],
            "teaching": ["molecular biology", "genetics labs", "research mentorship"],
        },
        "Chemistry": {
            "required": ["organic chemistry", "analytical methods", "spectroscopy"],
            "preferred": ["materials chemistry", "computational chemistry"],
            "research": ["catalysis", "materials synthesis", "electrochemistry"],
            "teaching": ["organic chemistry", "analytical chemistry labs", "synthesis workshops"],
        },
        "Physics": {
            "required": ["classical mechanics", "quantum mechanics", "statistical physics"],
            "preferred": ["condensed matter", "photonics"],
            "research": ["quantum materials", "optics", "astrophysics"],
            "teaching": ["introductory physics", "advanced physics labs", "theory seminars"],
        },
        "Electrical and Computer Engineering": {
            "required": ["signals and systems", "digital logic", "embedded systems"],
            "preferred": ["vlsi", "machine learning hardware"],
            "research": ["signal processing", "wireless systems", "edge ai"],
            "teaching": ["circuits", "digital systems labs", "embedded systems"],
        },
    }

    t = title.lower()
    if "data science" in t:
        required = ["statistics", "machine learning", "python", "data visualization", "teaching"]
        preferred = ["deep learning", "big data", "nlp"]
        research = ["applied machine learning", "data mining", "predictive modeling"]
        teaching = ["intro to data science", "ml courses", "capstone supervision"]
    elif "computer science" in t or "cs" in t:
        required = ["data structures", "algorithms", "teaching", "software engineering"]
        preferred = ["systems", "databases", "ai"]
        research = ["computer science research", "software systems", "ai applications"]
        teaching = ["undergraduate cs core", "project supervision"]
    elif "mathematics" in t or "statistics" in t:
        required = ["calculus", "linear algebra", "probability", "teaching"]
        preferred = ["numerical methods", "stochastic processes"]
        research = ["applied math", "statistical modeling"]
        teaching = ["calc sequence", "probability", "mentoring"]
    elif "finance" in t:
        required = ["financial modeling", "quantitative analysis", "econometrics", "corporate finance"]
        preferred = ["blockchain finance", "behavioral economics", "fintech"]
        research = ["asset pricing", "risk management", "market microstructure"]
        teaching = ["graduate-level finance", "investments", "financial econometrics"]
    elif "economics" in t:
        required = ["microeconomics", "macroeconomics", "econometrics"]
        preferred = ["development economics", "behavioral economics"]
        research = ["applied micro", "macro policy", "labor economics"]
        teaching = ["econometrics", "intermediate micro/macro", "seminar supervision"]
    elif "ai ethics" in t or ("ethics" in t and ("ai" in t or "artificial intelligence" in t)):
        required = ["algorithmic fairness", "responsible ai", "policy analysis"]
        preferred = ["model interpretability", "privacy-preserving ml"]
        research = ["accountability in ai", "ethical governance", "ai regulation"]
        teaching = ["responsible ai", "ethics seminars", "policy workshops"]
    elif "nlp" in t or "natural language" in t:
        required = ["nlp", "python", "machine learning"]
        preferred = ["transformers", "information retrieval"]
        research = ["language modeling", "text mining", "multilingual nlp"]
        teaching = ["nlp", "ml for text", "project supervision"]
    elif "computer vision" in t or "vision" in t:
        required = ["computer vision", "deep learning", "python"]
        preferred = ["3d vision", "self-supervised learning"]
        research = ["object detection", "multimodal learning", "medical imaging"]
        teaching = ["computer vision", "deep learning", "capstone mentorship"]
    elif "cybersecurity" in t or "security" in t:
        required = ["network security", "cryptography", "threat modeling"]
        preferred = ["cloud security", "secure software"]
        research = ["intrusion detection", "malware analysis", "privacy"]
        teaching = ["information security", "crypto", "secure coding"]
    elif "mechanical" in t:
        required = ["mechanics", "cad", "materials", "numerical methods"]
        preferred = ["robotics", "additive manufacturing"]
        research = ["dynamics", "design optimization", "energy systems"]
        teaching = ["mechanics sequence", "cad labs", "design studio"]
    elif "civil" in t:
        required = ["structural analysis", "geotechnical", "project management"]
        preferred = ["sustainable design", "bim"]
        research = ["infrastructure resilience", "transportation systems"]
        teaching = ["structural design", "construction management"]
    elif "biomedical" in t:
        required = ["biomechanics", "signal processing", "medical devices"]
        preferred = ["neural engineering", "bioinstrumentation"]
        research = ["rehabilitation engineering", "biomedical imaging"]
        teaching = ["biomedical instrumentation", "bio-signal processing"]
    elif "psychology" in t:
        required = ["research design", "statistics", "cognitive psychology"]
        preferred = ["neuroimaging", "computational modeling"]
        research = ["cognition", "mental health", "developmental psychology"]
        teaching = ["research methods", "cognitive psychology"]
    elif "marketing" in t:
        required = ["consumer behavior", "marketing analytics", "research methods"]
        preferred = ["digital marketing", "causal inference"]
        research = ["brand strategy", "digital platforms"]
        teaching = ["marketing analytics", "consumer behavior"]
    elif "accounting" in t:
        required = ["financial accounting", "auditing", "data analysis"]
        preferred = ["forensic accounting", "tax policy"]
        research = ["disclosure", "earnings quality", "audit quality"]
        teaching = ["financial accounting", "auditing"]
    elif "biology" in t:
        required = ["molecular biology", "experimental design", "statistics"]
        preferred = ["genomics", "single-cell analysis"]
        research = ["cell biology", "genetics", "systems biology"]
        teaching = ["molecular biology", "lab supervision"]
    elif "chemistry" in t:
        required = ["organic/inorganic chemistry", "spectroscopy", "lab safety"]
        preferred = ["materials chemistry", "computational chemistry"]
        research = ["catalysis", "materials synthesis", "analytical methods"]
        teaching = ["organic chemistry", "laboratory instruction"]
    elif "physics" in t:
        required = ["classical mechanics", "quantum mechanics", "statistical physics"]
        preferred = ["condensed matter", "photonics"]
        research = ["quantum materials", "optics", "astrophysics"]
        teaching = ["intro physics", "advanced labs"]
    else:
        # Use template if available, otherwise synthesize specifics from department
        if department in templates:
            spec = templates[department]
            required = spec["required"]
            preferred = spec["preferred"]
            research = spec["research"]
            teaching = spec["teaching"]
        else:
            dept_lc = department.lower() if department else "interdisciplinary studies"
            # Synthesize concrete, discipline-leaning defaults (avoid generic placeholders)
            required = [f"foundations of {dept_lc}", f"research methods in {dept_lc}", f"data analysis for {dept_lc}"]
            preferred = [f"emerging topics in {dept_lc}", f"industry collaboration in {dept_lc}"]
            research = [f"applied {dept_lc}", f"advanced {dept_lc} techniques"]
            teaching = [f"introductory {dept_lc} courses", f"advanced {dept_lc} seminars"]

    return {
        "id": title_to_id(title),
        "title": title,
        "department": department,
        "required_skills": list(dict.fromkeys(required))[:6],
        "preferred_skills": list(dict.fromkeys(preferred))[:4],
        "research_focus": research,
        "teaching_requirements": teaching,
    }


