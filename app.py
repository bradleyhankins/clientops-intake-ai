import streamlit as st

from ai_helpers import enhance_text, stable_cache_key
from core.diagnostics import run_diagnostic
from core.prompts import build_ai_prompt, build_rules_summary
from core.report_builder import build_report
from data.sample_data import (
    BUSINESS_TYPES,
    PAIN_POINTS,
    REVENUE_STAGES,
    SAMPLE_SCENARIOS,
    TEAM_SIZES,
    TOOL_MATURITY,
    URGENCY_LEVELS,
)
from pdf_helpers import markdown_to_pdf

st.set_page_config(page_title="ClientOps Intake AI", page_icon="🧭", layout="wide")

CSS = """
<style>
.block-container{max-width:1180px;padding-top:1.35rem;padding-bottom:3rem}
[data-testid="stSidebar"]{background:#111827}
[data-testid="stSidebar"] h1,[data-testid="stSidebar"] h2,[data-testid="stSidebar"] h3,[data-testid="stSidebar"] p,[data-testid="stSidebar"] li,[data-testid="stSidebar"] span,[data-testid="stSidebar"] label{color:#f9fafb!important}
[data-testid="stSidebar"] li::marker{color:#93c5fd!important}.hero{padding:1.9rem 2rem;border-radius:20px;background:linear-gradient(135deg,#111827 0%,#1f2937 52%,#334155 100%);color:#fff;box-shadow:0 18px 36px rgba(17,24,39,.18);margin-bottom:1rem;border:1px solid rgba(255,255,255,.08)}
.eyebrow{text-transform:uppercase;letter-spacing:.13em;font-size:.75rem;font-weight:800;color:#93c5fd;margin-bottom:.65rem}.hero-title{font-size:2.25rem;line-height:1.08;font-weight:850;margin-bottom:.65rem}.hero-subtitle{font-size:1.02rem;line-height:1.62;color:#e5e7eb;max-width:900px}.hero-pills span{display:inline-block;padding:.35rem .65rem;margin:.75rem .28rem 0 0;border-radius:999px;background:rgba(255,255,255,.10);border:1px solid rgba(255,255,255,.16);font-weight:700;font-size:.78rem;color:#f8fafc}
.section-title{margin-top:1.25rem;margin-bottom:.55rem;font-size:1.4rem;font-weight:850;color:#111827}.section-lede{color:#4b5563;line-height:1.6;margin-bottom:1rem;max-width:950px}.form-group-title{font-size:.9rem;font-weight:850;text-transform:uppercase;letter-spacing:.06em;color:#64748b;margin:.35rem 0 .15rem 0}
.metric-card,.output-card,.warning-card,.success-card,.workflow-card{background:#fff;border:1px solid #e5e7eb;border-radius:18px;box-shadow:0 8px 20px rgba(15,23,42,.055)}.metric-card{height:138px;padding:1rem;margin-bottom:.75rem}.metric-label{color:#6b7280;font-size:.78rem;font-weight:800;text-transform:uppercase;letter-spacing:.05em;margin-bottom:.5rem}.metric-value{color:#111827;font-size:1.35rem;line-height:1.18;font-weight:900;overflow-wrap:break-word}.metric-note{color:#64748b;font-size:.85rem;margin-top:.55rem}.output-card,.warning-card,.success-card,.workflow-card{padding:1.15rem;margin-bottom:.8rem}.output-card{border-left:5px solid #111827}.warning-card{border-left:5px solid #f59e0b}.success-card{border-left:5px solid #059669}.workflow-card{border-left:5px solid #1d4ed8}.output-card h3,.warning-card h3,.success-card h3,.workflow-card h3{font-size:1.05rem;font-weight:850;color:#111827;margin-bottom:.4rem}.output-card p,.warning-card p,.success-card p,.workflow-card p,.output-card li,.warning-card li,.success-card li,.workflow-card li{color:#4b5563;line-height:1.52;font-size:.93rem}.note-box{padding:.9rem 1rem;border-radius:14px;background:#f8fafc;color:#334155;border:1px solid #e2e8f0;font-weight:650;margin:.9rem 0;font-size:.92rem}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

PRIVACY_NOTE = "Public demo note: Use fictional/sample data for demos. Do not enter sensitive, confidential, or regulated business information. If AI is enabled, entered text may be processed by the configured AI provider for output enhancement."


def section_title(title: str, lede: str | None = None) -> None:
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
    if lede:
        st.markdown(f'<div class="section-lede">{lede}</div>', unsafe_allow_html=True)


def form_group(title: str) -> None:
    st.markdown(f'<div class="form-group-title">{title}</div>', unsafe_allow_html=True)


def metric_card(label: str, value: str, note: str | None = None) -> None:
    note_html = f'<div class="metric-note">{note}</div>' if note else ""
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div>{note_html}</div>',
        unsafe_allow_html=True,
    )


def html_card(title: str, body: str, css_class: str = "output-card") -> None:
    st.markdown(f'<div class="{css_class}"><h3>{title}</h3>{body}</div>', unsafe_allow_html=True)


def html_list(items: list[str]) -> str:
    return "<ul>" + "".join(f"<li>{item}</li>" for item in items) + "</ul>"


def md_to_html(text: str) -> str:
    return text.replace("\n", "<br>")


def render_sidebar() -> None:
    with st.sidebar:
        st.title("ClientOps Intake AI")
        st.caption("Version 1.3")
        st.markdown("Diagnostic intake assistant for workflow bottlenecks, maturity scoring, automation opportunities, and 30-day roadmaps.")
        st.divider()
        st.markdown("### Outputs")
        st.markdown("- Maturity score\n- Primary bottleneck\n- Recommended toolkit app\n- Automation opportunities\n- 30-day roadmap\n- PDF diagnostic report")


def render_hero() -> None:
    st.markdown(
        """
<div class="hero"><div class="eyebrow">Client Diagnostic Intake Assistant</div><div class="hero-title">ClientOps Intake AI</div><div class="hero-subtitle">Diagnose business workflow bottlenecks, score operational maturity, recommend automation opportunities, match the right toolkit app, and generate a 30-day improvement roadmap.</div><div class="hero-pills"><span>Workflow Diagnostics</span><span>Operations</span><span>AI Consulting</span><span>Roadmaps</span><span>Streamlit</span></div></div>
""",
        unsafe_allow_html=True,
    )


def build_inputs(scenario: dict) -> dict | None:
    with st.form("clientops_form"):
        form_group("Business profile")
        c1, c2 = st.columns(2)
        with c1:
            business_name = st.text_input("Business Name", value=scenario.get("business_name", ""), placeholder="Example: Summit Home Services")
            business_type = st.selectbox("Business Type", BUSINESS_TYPES, index=BUSINESS_TYPES.index(scenario.get("business_type", "Home Services")))
            team_size = st.selectbox("Team Size", TEAM_SIZES, index=TEAM_SIZES.index(scenario.get("team_size", "4-10 people")))
        with c2:
            revenue_stage = st.selectbox("Revenue Stage", REVENUE_STAGES, index=REVENUE_STAGES.index(scenario.get("revenue_stage", "$1M-$3M")))
            tool_maturity = st.selectbox("Current Tool / Process Maturity", TOOL_MATURITY, index=TOOL_MATURITY.index(scenario.get("tool_maturity", "CRM or project tool")))
            urgency = st.selectbox("Urgency", URGENCY_LEVELS, index=URGENCY_LEVELS.index(scenario.get("urgency", "Medium")))

        form_group("Workflow pain points")
        pain_points = st.multiselect("Select the biggest current problems", PAIN_POINTS, default=scenario.get("pain_points", []))

        form_group("Current state and desired outcome")
        current_process = st.text_area("How does the current workflow operate today?", value=scenario.get("current_process", ""), height=120, max_chars=4000)
        desired_outcome = st.text_area("What outcome would make the biggest difference?", value=scenario.get("desired_outcome", ""), height=120, max_chars=4000)
        submitted = st.form_submit_button("Generate ClientOps Diagnostic", use_container_width=True)

    if not submitted:
        return None

    return {
        "business_name": business_name,
        "business_type": business_type,
        "team_size": team_size,
        "revenue_stage": revenue_stage,
        "tool_maturity": tool_maturity,
        "urgency": urgency,
        "pain_points": pain_points,
        "current_process": current_process,
        "desired_outcome": desired_outcome,
    }


def render_results(inputs: dict, diagnostic: dict, executive_summary: str, pdf_report: bytes) -> None:
    recommendation = diagnostic["recommendation"]

    section_title("Diagnostic snapshot")
    mc1, mc2, mc3, mc4 = st.columns(4)
    with mc1:
        metric_card("Maturity Score", f"{diagnostic['score']}%", diagnostic["label"])
    with mc2:
        metric_card("Primary Bottleneck", diagnostic["primary_key"].title())
    with mc3:
        metric_card("Recommended App", recommendation["app"])
    with mc4:
        metric_card("Urgency", inputs["urgency"])

    section_title("Executive diagnostic summary")
    html_card("Recommended Direction", f"<p>{md_to_html(executive_summary)}</p>", "workflow-card")
    st.link_button(f"Open {recommendation['app']}", recommendation["url"], use_container_width=True)

    section_title("Automation opportunities")
    html_card("Recommended Opportunities", html_list(diagnostic["opportunities"]), "success-card")

    section_title("30-day improvement roadmap")
    road_cols = st.columns(2)
    for idx, step in enumerate(diagnostic["roadmap_steps"]):
        with road_cols[idx % 2]:
            html_card(f"Roadmap Step {idx + 1}", f"<p>{step}</p>", "workflow-card")

    section_title("Manager action plan")
    html_card("Next Actions", html_list(diagnostic["actions"]), "output-card")

    section_title("Download diagnostic report")
    st.download_button(
        "Download Diagnostic Report PDF",
        data=pdf_report,
        file_name="clientops-diagnostic-report.pdf",
        mime="application/pdf",
        use_container_width=True,
    )


def main() -> None:
    render_sidebar()
    render_hero()

    section_title("Diagnostic intake", "Load a sample scenario or enter a fictional business profile to generate a workflow improvement diagnostic.")
    st.markdown(f'<div class="note-box">{PRIVACY_NOTE}</div>', unsafe_allow_html=True)

    scenario_name = st.selectbox("Load Sample Scenario", list(SAMPLE_SCENARIOS.keys()))
    scenario = SAMPLE_SCENARIOS.get(scenario_name, {})
    inputs = build_inputs(scenario)

    if inputs is None:
        st.markdown('<div class="note-box">Complete the intake or load a sample scenario, then generate the diagnostic report.</div>', unsafe_allow_html=True)
        return

    diagnostic = run_diagnostic(inputs)
    rules_summary = build_rules_summary(inputs, diagnostic)
    ai_prompt = build_ai_prompt(inputs, rules_summary, diagnostic["roadmap_steps"])
    executive_summary = enhance_text(ai_prompt, rules_summary, stable_cache_key("clientops_summary", inputs))
    report = build_report(inputs, diagnostic, executive_summary)
    pdf_report = markdown_to_pdf(report, title="ClientOps Intake AI Diagnostic Report")

    render_results(inputs, diagnostic, executive_summary, pdf_report)

    section_title("What this app demonstrates")
    html_card(
        "Portfolio Skills Shown",
        "<ul><li>Modular Streamlit architecture</li><li>AI-enhanced consulting summary with rules-based fallback</li><li>Consulting-style intake workflow design</li><li>Rules-based maturity scoring</li><li>Bottleneck diagnosis and tool routing</li><li>User-friendly PDF reporting</li></ul>",
        "success-card",
    )

    with st.expander("How to use ClientOps Intake AI"):
        st.markdown("1. Load a sample scenario or enter a fictional business profile.\n2. Select the current workflow pain points.\n3. Generate the diagnostic.\n4. Review the maturity score, bottleneck, recommended app, automation opportunities, and roadmap.\n5. Download the PDF diagnostic report.")

    st.markdown(f'<div class="note-box">{PRIVACY_NOTE}</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
