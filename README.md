# Agentic AI Talent Acquisition & Faculty Management System

A runnable, local-first Python project that demonstrates an agentic, multi-agent pipeline for academic faculty recruitment and ongoing development. It uses classic NLP and scikit-learn for an out-of-the-box experience without paid keys, and optionally integrates LangChain and CrewAI if installed.

## Features
- Sourcing, Screening, Interview, Onboarding, and Performance & Development agents
- Resume ingestion (CSV/JSON/Folder of text/PDF via simple extraction), role definitions, and candidate-job fit scoring
- Local TF-IDF embeddings by default; optional Sentence-Transformers via LangChain
- Orchestrator that coordinates agents and produces structured reports
- CLI for ingesting data, matching candidates, and generating reports

## Quickstart

```bash
# from project root
python -m venv .venv
. .venv/Scripts/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m nltk.downloader punkt stopwords

# Run end-to-end demo
python app/cli.py demo --data ./data --out ./outputs

# Run Streamlit UI
streamlit run app/ui.py
```

## CLI

```bash
python app/cli.py ingest --data ./data
python app/cli.py match --role ./data/roles/cs_assistant_professor.yaml --out ./outputs
python app/cli.py report --out ./outputs
python app/cli.py demo --data ./data --out ./outputs
```

## Optional Integrations
- Install optional libs (uncomment in `requirements.txt`): LangChain, sentence-transformers, CrewAI.
- If available, the system will prefer semantic embeddings from Sentence-Transformers and orchestrate with CrewAI.

## Project Structure
```
app/
  __init__.py
  cli.py
  config.py
  data_models.py
  embeddings.py
  parsing.py
  scoring.py
  orchestrator.py
  agents/
    __init__.py
    sourcing.py
    screening.py
    interview.py
    onboarding.py
    development.py
  utils/
    __init__.py
    io.py
    text.py
  reports/
    __init__.py
    generator.py
  workflows/
    __init__.py
    demo.py

data/
  candidates/
  roles/
outputs/
```

## Notes
- PDFs are parsed best-effort (simple text extractor). For production, integrate a robust PDF/OCR pipeline.
- This project emphasizes fairness and transparency with explainable scoring features.
- All code runs locally; internet access is not required for the default flow.

