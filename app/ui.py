from __future__ import annotations

import io
import json
from pathlib import Path
from typing import Dict, List, Optional
import sys

import streamlit as st

# Ensure project root is on sys.path when run via `streamlit run app/ui.py`
_CURRENT_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _CURRENT_DIR.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from app.config import CONFIG
from app.data_models import Candidate, Role, role_from_yaml
from app.orchestrator import Orchestrator
from app.parsing import parse_candidate_folder
from app.utils.io import save_json
from app.role_classifier import classify_role
import plotly.express as px


st.set_page_config(page_title="AI Talent Acquisition & Faculty Management", layout="wide")

# Global styles (dark theme accents, cards, chips, KPI)
ACCENT = "#1fb6aa"  # deep teal accent
st.markdown(
    f"""
    <style>
    html, body, [class*="css"]  {{
        font-family: 'Inter', 'Roboto', system-ui, -apple-system, Segoe UI, Arial, sans-serif;
    }}
    .accent {{ color: {ACCENT}; }}
    .card {{
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px;
        padding: 1rem 1.25rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 2px rgba(0,0,0,0.25);
    }}
    .kpi-card {{
        background: linear-gradient(135deg, rgba(31,182,170,0.15), rgba(31,182,170,0.03));
        border: 1px solid rgba(31,182,170,0.35);
        border-radius: 14px;
        padding: 1rem 1.25rem;
        text-align: center;
    }}
    .kpi-value {{ font-size: 2rem; font-weight: 800; color: {ACCENT}; }}
    .chip {{
        display: inline-block;
        padding: 6px 12px;
        border-radius: 999px;
        border: 1px solid rgba(255,255,255,0.15);
        margin: 4px;
        cursor: pointer;
        transition: all .15s ease;
    }}
    .chip:hover {{
        border-color: {ACCENT};
        background: rgba(31,182,170,0.12);
    }}
    .chip.selected {{
        background: {ACCENT};
        color: #061016;
        border-color: {ACCENT};
    }}
    .progress-wrap {{ height: 8px; background: rgba(255,255,255,0.08); border-radius: 8px; overflow: hidden; }}
    .progress-bar {{ height: 8px; background: {ACCENT}; }}
    .upload-zone {{
        border: 2px dashed rgba(255,255,255,0.18);
        border-radius: 14px;
        padding: 2rem;
        text-align: center;
        background: rgba(255,255,255,0.02);
    }}
    .file-row {{ display:flex; align-items:center; justify-content:space-between; padding:8px 12px; border:1px solid rgba(255,255,255,0.08); border-radius:10px; margin-bottom:8px; }}
    .btn-accent button {{ background: {ACCENT}; color:#061016; border:0; }}
    .btn-accent button:hover {{ filter: brightness(1.05); }}
    /* Tabs styling */
    div.stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {{
        border-bottom: 3px solid {ACCENT};
        color: {ACCENT};
    }}
    /* Compact multiselect */
    .compact-multiselect .stMultiSelect > div {{ max-height: 160px; overflow-y: auto; }}
    </style>
    """,
    unsafe_allow_html=True,
)


DATA_DIR = CONFIG.data_dir
ROLE_DIR = CONFIG.roles_dir
CAND_DIR = CONFIG.candidate_dir
OUTPUT_DIR = CONFIG.output_dir


def load_roles() -> List[Role]:
    roles: List[Role] = []
    ROLE_DIR.mkdir(parents=True, exist_ok=True)
    for p in ROLE_DIR.glob("*.yaml"):
        try:
            roles.append(role_from_yaml(p))
        except Exception:
            continue
    for p in ROLE_DIR.glob("*.yml"):
        try:
            roles.append(role_from_yaml(p))
        except Exception:
            continue
    for p in ROLE_DIR.glob("*.json"):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            roles.append(
                Role(
                    id=data.get("id", p.stem),
                    title=data.get("title", p.stem),
                    department=data.get("department", ""),
                    required_skills=data.get("required_skills", []),
                    preferred_skills=data.get("preferred_skills", []),
                    research_focus=data.get("research_focus", []),
                    teaching_requirements=data.get("teaching_requirements", []),
                )
            )
        except Exception:
            continue
    return roles


def ensure_dirs() -> None:
    for d in [DATA_DIR, ROLE_DIR, CAND_DIR, OUTPUT_DIR]:
        d.mkdir(parents=True, exist_ok=True)


def save_uploaded_resume(file_name: str, bytes_data: bytes) -> Path:
    path = CAND_DIR / file_name
    path.write_bytes(bytes_data)
    return path


def parse_candidate_files() -> List[Candidate]:
    return parse_candidate_folder(CAND_DIR)


def export_markdown(role: Role, matches: List[Dict]) -> str:
    lines = [f"# Matching Report — {role.title} [{role.department}]", ""]
    for m in matches:
        lines.append(f"## Candidate: {m['candidate_id']} — Fit: {m['fit_score']}")
        lines.append("**Strengths**:")
        for s in m.get("strengths", []):
            lines.append(f"- {s}")
        lines.append("**Risks**:")
        for r in m.get("risks", []):
            lines.append(f"- {r}")
        lines.append("")
    return "\n".join(lines)


def ui() -> None:
    ensure_dirs()
    st.markdown("<h1 style='text-align:center; color:#1fb6aa;'>🤖 Agentic AI Talent Acquisition & Faculty Management</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; opacity:.85;'>Upload resumes, select or define a role, compute fit, and review an interactive dashboard.</p>", unsafe_allow_html=True)

    with st.sidebar:
        st.header("📂 Data Upload")
        uploaded = st.file_uploader("Upload resumes (.txt, .pdf)", type=["txt", "pdf"], accept_multiple_files=True)
        if uploaded:
            for f in uploaded:
                save_uploaded_resume(f.name, f.getbuffer())
            st.success("Candidates Loaded")
        files_sb = list(CAND_DIR.glob("*"))
        if files_sb:
            st.markdown("**Uploaded Files**")
            for p in files_sb[:12]:
                st.write(f"- {p.name}")
            if len(files_sb) > 12:
                st.write(f"… and {len(files_sb)-12} more")

    roles = load_roles()
    role_map = {f"{r.title} [{r.department}]": r for r in roles}
    selected_role: Optional[Role] = None
    if st.session_state.get("expanded_role"):
        try:
            selected_role = st.session_state["expanded_role"]  # type: ignore[assignment]
        except Exception:
            selected_role = None
    # Tabs for navigation
    setup_tab, results_tab = st.tabs(["Setup & Definition", "Results Dashboard"])

    with setup_tab:
        st.subheader("Define Role (Classifier)")
        card_role = st.container()
        with card_role:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            title_only = st.text_input("Enter Role Title", placeholder="Lecturer in Data Science", key="role_title_input")
            colc1, colc2 = st.columns([1, 1])
            with colc1:
                classify_btn = st.button("Classify Title", key="btn_classify")
            with colc2:
                save_btn = st.button("Save Role Profile", key="btn_save", disabled=not bool(st.session_state.get("classified_role_json")))

            if classify_btn and title_only:
                classified = classify_role(title_only)
                st.session_state["classified_role_json"] = classified
                # also set selected role for analysis
                selected_role = Role(
                    id=classified["id"],
                    title=classified["title"],
                    department=classified["department"],
                    required_skills=classified.get("required_skills", []),
                    preferred_skills=classified.get("preferred_skills", []),
                    research_focus=classified.get("research_focus", []),
                    teaching_requirements=classified.get("teaching_requirements", []),
                )
                st.session_state["expanded_role"] = selected_role
                st.success("Role profile generated.")

            if st.session_state.get("classified_role_json"):
                st.markdown("#### Generated Role Profile")
                st.json(st.session_state["classified_role_json"])
                # ensure selected_role reflects latest classified profile
                cr = st.session_state["classified_role_json"]
                selected_role = Role(
                    id=cr["id"],
                    title=cr["title"],
                    department=cr["department"],
                    required_skills=cr.get("required_skills", []),
                    preferred_skills=cr.get("preferred_skills", []),
                    research_focus=cr.get("research_focus", []),
                    teaching_requirements=cr.get("teaching_requirements", []),
                )
                st.session_state["expanded_role"] = selected_role

            if save_btn and st.session_state.get("classified_role_json"):
                save_json(ROLE_DIR / f"{st.session_state['classified_role_json']['id']}.json", st.session_state["classified_role_json"])
                st.success("Saved to data/roles.")

            st.markdown('</div>', unsafe_allow_html=True)
        st.subheader("Candidates")
        candidates = parse_candidate_files()
        cand_ids = [c.id for c in candidates]
        if not cand_ids:
            st.markdown('<div class="upload-zone">Drag & drop resumes via sidebar, or use the uploader there.</div>', unsafe_allow_html=True)
        # Status counter above widget
        sel_default = cand_ids
        selected = st.multiselect("Select Candidates", options=cand_ids, default=sel_default, help="Use to include/exclude candidates", key="cand_multiselect")
        chosen = [c for c in candidates if c.id in set(selected)]
        st.caption(f"Selected {len(chosen)} / {len(candidates)} candidates")

        col_a, col_b = st.columns([1, 2])
        with col_a:
            # Auto-classify from title input if no selected_role present
            if not selected_role:
                auto_title = st.session_state.get("role_title_input")
                if auto_title:
                    cr = classify_role(auto_title)
                    selected_role = Role(
                        id=cr["id"],
                        title=cr["title"],
                        department=cr["department"],
                        required_skills=cr.get("required_skills", []),
                        preferred_skills=cr.get("preferred_skills", []),
                        research_focus=cr.get("research_focus", []),
                        teaching_requirements=cr.get("teaching_requirements", []),
                    )
                    st.session_state["expanded_role"] = selected_role
            disabled = not (selected_role and chosen)
            if st.button("Compute Fit & Generate Report", help="Compute fit and navigate to dashboard", key="analyze", use_container_width=True, disabled=disabled):
                orch = Orchestrator()
                matches = orch.screening.rank_candidates(chosen, selected_role)  # type: ignore[arg-type]
                st.session_state["matches"] = [m.__dict__ for m in matches]
                st.session_state["role"] = selected_role.__dict__  # type: ignore[union-attr]
                st.success("Analysis complete. Displaying results…")
                st.rerun()

    with results_tab:
        matches = st.session_state.get("matches", [])
        if not matches:
            st.info("Results Dashboard will appear after analysis is computed on the Setup & Definition tab.")
            return
        st.markdown("## Results Dashboard")
        best = max(matches, key=lambda m: m.get("fit_score", 0)) if matches else None
        k1, k2, k3 = st.columns(3)
        with k1:
            st.markdown('<div class="kpi-card" style="padding: 1.5rem 1.75rem; margin-top: .5rem;"><div style="font-size:0.95rem; opacity:.8;">Top Fit Score</div>' + (f'<div class="kpi-value" style="font-size:3rem;">{best["fit_score"]:.3f}</div>' if best else '<div class="kpi-value" style="font-size:3rem;">—</div>') + '</div>', unsafe_allow_html=True)
        with k2:
            st.markdown(f'<div class="kpi-card" style="padding: 1.5rem 1.75rem; margin-top: .5rem;"><div style="font-size:0.95rem; opacity:.8;">Candidates Evaluated</div><div class="kpi-value" style="font-size:3rem;">{len(matches)}</div></div>', unsafe_allow_html=True)
        with k3:
            balance = f"{len(best.get('strengths', []))}/{len(best.get('risks', []))}" if best else "—"
            st.markdown(f'<div class="kpi-card" style="padding: 1.5rem 1.75rem; margin-top: .5rem;"><div style="font-size:0.95rem; opacity:.8;">Strength/Risk Balance</div><div class="kpi-value" style="font-size:3rem;">{balance}</div></div>', unsafe_allow_html=True)

        # Dense, sortable table
        df_rows = [
            {
                "candidate": m["candidate_id"],
                "fit_score": float(m.get("fit_score", 0.0)),
                "strengths": len(m.get("strengths", [])),
                "risks": len(m.get("risks", [])),
            }
            for m in matches
        ]
        if df_rows:
            # Basic bar visualization of fit scores
            fig = px.bar(df_rows, x="candidate", y="fit_score", title="Fit Scores", color="fit_score", color_continuous_scale="Tealgrn")
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(df_rows, use_container_width=True, hide_index=True)

        # Details panel
        for m in matches:
            with st.container():
                st.markdown('<div class="card" style="padding:1.25rem 1.5rem;">', unsafe_allow_html=True)
                c1, c2, c3 = st.columns([3, 6, 1])
                with c1:
                    st.markdown(f"### {m['candidate_id']}")
                with c2:
                    pct = max(0.0, min(1.0, float(m.get("fit_score", 0.0))))
                    st.markdown(f'<div class="progress-wrap"><div class="progress-bar" style="width:{pct*100:.1f}%"></div></div>', unsafe_allow_html=True)
                    strengths_num = len(m.get("strengths", []))
                    risks_num = len(m.get("risks", []))
                    st.caption(f"Fit {pct:.4f}  •  ↑ {strengths_num}  ↓ {risks_num}")
                with c3:
                    if st.button("View Details", key=f"vd_{m['candidate_id']}"):
                        st.session_state["detail_candidate"] = m
                st.markdown('</div>', unsafe_allow_html=True)

        if st.session_state.get("detail_candidate"):
            det = st.session_state["detail_candidate"]
            st.markdown("### Candidate Details")
            cold1, cold2 = st.columns(2)
            with cold1:
                st.markdown("**Strengths**")
                for s in det.get("strengths", []):
                    st.write(f"- {s}")
            with cold2:
                st.markdown("**Risks**")
                for r in det.get("risks", []):
                    st.write(f"- {r}")
        # Export section
        st.markdown("---")
        export_col1, export_col2 = st.columns([1, 1])
        with export_col1:
            if st.session_state.get("matches"):
                from json import dumps
                st.download_button("Download JSON Report", data=dumps({"role": st.session_state.get("role"), "matches": st.session_state.get("matches")}, indent=2), file_name="report.json")

            st.divider()
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Export JSON"):
                    out = OUTPUT_DIR / "ui_report.json"
                    payload = {"role": st.session_state.get("role"), "matches": matches}
                    save_json(out, payload)
                    st.success(f"Saved {out}")
            with c2:
                if st.button("Export Markdown") and selected_role:
                    md = export_markdown(selected_role, matches)
                    st.download_button("Download report.md", data=md, file_name="report.md")


if __name__ == "__main__":
    ui()

