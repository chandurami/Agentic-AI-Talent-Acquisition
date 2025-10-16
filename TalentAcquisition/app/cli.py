from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import typer
from rich import print

from .config import CONFIG
from .data_models import role_from_yaml
from .orchestrator import Orchestrator
from .parsing import parse_candidate_folder
from .role_classifier import classify_role


app = typer.Typer(add_completion=False)


@app.command()
def ingest(data: str = typer.Option("data", help="Data directory")) -> None:
    data_dir = Path(data)
    candidates = parse_candidate_folder(data_dir / "candidates")
    print(f"[bold green]Ingested[/] {len(candidates)} candidates from {data_dir / 'candidates'}")


@app.command()
def match(
    role: str = typer.Option(..., help="YAML role file"),
    data: str = typer.Option("data", help="Data directory"),
    out: str = typer.Option("outputs", help="Output directory"),
) -> None:
    orch = Orchestrator()
    report_path = orch.run(Path(role), Path(data), Path(out))
    print(f"[bold green]Report generated:[/] {report_path}")
    print(Path(report_path).read_text(encoding="utf-8")[:4000])


@app.command()
def report(out: str = typer.Option("outputs", help="Output directory")) -> None:
    report_path = Path(out) / "report.json"
    if not report_path.exists():
        print("[red]No report found. Run 'match' first.[/]")
        raise typer.Exit(code=1)
    data = json.loads(report_path.read_text(encoding="utf-8"))
    print(data)


@app.command()
def classify(
    title: str = typer.Argument(..., help="Role title to classify"),
    out: str = typer.Option("data/roles", help="Directory to save role JSON"),
) -> None:
    role_json = classify_role(title)
    out_dir = Path(out)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{role_json['id']}.json"
    path.write_text(json.dumps(role_json, indent=2), encoding="utf-8")
    print(f"[bold green]Saved[/] {path}")


@app.command()
def demo(
    data: str = typer.Option("data", help="Data dir with candidates and roles"),
    out: str = typer.Option("outputs", help="Output directory"),
) -> None:
    role_file = Path(data) / "roles" / "cs_assistant_professor.yaml"
    if not role_file.exists():
        print(f"[yellow]Sample role not found at {role_file}. Creating one...[/]")
        role_file.parent.mkdir(parents=True, exist_ok=True)
        role_file.write_text(
            """
id: cs_asst_prof
title: Assistant Professor of Computer Science
department: Computer Science
required_skills:
  - machine learning
  - data structures
  - teaching
preferred_skills:
  - deep learning
  - natural language processing
research_focus:
  - artificial intelligence
  - data science
teaching_requirements:
  - undergraduate courses
  - curriculum development
            """.strip(),
            encoding="utf-8",
        )
    cand_dir = Path(data) / "candidates"
    cand_dir.mkdir(parents=True, exist_ok=True)
    sample_resume = cand_dir / "jane_doe.txt"
    if not sample_resume.exists():
        sample_resume.write_text(
            """
Jane Doe
Email: jane@example.edu
Experience: Teaching undergraduate courses in data structures and algorithms.
Research: Artificial intelligence, machine learning, and data science.
Skills: machine learning, deep learning, natural language processing, teaching, curriculum development
Publications: 10 peer-reviewed papers in AI venues.
            """.strip(),
            encoding="utf-8",
        )
    orch = Orchestrator()
    report_path = orch.run(role_file, Path(data), Path(out))
    print(f"[bold green]Demo report:[/] {report_path}")
    print(Path(report_path).read_text(encoding="utf-8"))


if __name__ == "__main__":
    app()

