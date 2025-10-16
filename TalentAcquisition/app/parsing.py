from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import List

from .data_models import Candidate
from .utils.io import list_files, read_text_file
from .utils.text import normalize


def extract_text_from_pdf(path: Path) -> str:
    # Lightweight, dependency-free placeholder: best-effort raw text read
    # For production, integrate pdfminer.six or PyPDF2.
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def parse_candidate_folder(folder: Path) -> List[Candidate]:
    files = list_files(folder, exts={".txt", ".pdf", ".json"})
    candidates: List[Candidate] = []
    for f in files:
        if f.suffix.lower() == ".pdf":
            text = extract_text_from_pdf(f)
        else:
            text = read_text_file(f)
        if not text:
            continue
        base = f.stem
        name = base.replace("_", " ")
        resume_text = normalize(text)
        candidates.append(
            Candidate(
                id=base,
                name=name.title(),
                email=None,
                resume_text=resume_text,
            )
        )
    return candidates

