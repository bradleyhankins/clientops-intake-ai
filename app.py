import streamlit as st

from ai_helpers import enhance_text, stable_cache_key
from pdf_helpers import markdown_to_pdf

st.set_page_config(page_title="ClientOps Intake AI", page_icon="🧭", layout="wide")

BUSINESS_TYPES = ["Home Services", "Field Sales", "Local Service Business", "Professional Services", "Retail / Showroom", "Startup / Small Team", "Other"]
TEAM_SIZES = ["1-3 people", "4-10 people", "11-25 people", "26+ people"]
REVENUE_STAGES = ["Early / Pre-revenue", "Under $500K", "$500K-$1M", "$1M-$3M", "$3M+", "Prefer not to say"]
TOOL_MATURITY = ["Mostly manual", "Basic spreadsheets", "CRM or project tool", "Multiple tools but disconnected", "Strong systems in place"]
URGENCY_LEVELS = ["Low", "Medium", "High", "Critical"]

PAIN_POINTS = [
    "Performance visibility is unclear",
    "Sales follow-up is inconsistent",
    "CRM notes or data are messy",
    "Hiring/applicant review is inconsistent",
    "Processes live in people’s heads",
    "Training is inconsistent",
    "Manager meetings lack clean numbers",
    "Lead source quality is hard to compare",
    "Customer communication is inconsistent",
    "Reporting takes too much manual work",
]

SAMPLE_SCENARIOS = {
    "Blank / Custom": {},
    "Growing Home-Service Team": {
        "business_name": "Summit Home Services",
        "business_type": "Home Services",
        "team_size": "4-10 people",
        "revenue_stage": "$1M-$3M",
        "tool_maturity": "CRM or project tool",
        "urgency": "High",
        "pain_points": ["Performance visibility is unclear", "Sales follow-up is inconsistent", "CRM notes or data are messy", "Manager meetings lack clean numbers"],
        "current_process": "Leads are tracked in a CRM, but managers still rely on daily notes, spreadsheets, and memory to prepare coaching conversations.",
        "desired_outcome": "Cleaner weekly reporting, better rep accountability, and stronger follow-up discipline.",
    },
    "Process-Heavy Small Business": {
        "business_name": "Harbor Operations Group",
        "business_type": "Local Service Business",
        "team_size": "11-25 people",
        "revenue_stage": "$3M+",
        "tool_maturity": "Multiple tools but disconnected",
        "urgency": "Medium",
        "pain_points": ["Processes live in people’s heads", "Training is inconsistent", "Reporting takes too much manual work", "Customer communication is inconsistent"],
        "current_process": "The team has experienced managers, but most processes are taught verbally and vary by employee.",
        "desired_outcome": "Document repeatable processes and create better training consistency.",
    },
}

TOOL_RECOMMENDATIONS = {
    "performance": {"app": "OpsPilot AI", "why": "The biggest need is manager visibility, KPI reporting, rep performance review, or lead source analysis.", "url": "https://opspilot-ai.streamlit.app/"},
    "followup": {"app": "FollowUpPilot AI", "why": "The biggest need is stronger customer communication, CRM notes, follow-up timing, or sales execution discipline.", "url": "https://followuppilot-ai.streamlit.app/"},
    "recruiting": {"app": "RecruitPilot AI", "why": "The biggest need is organizing applicant review, resume notes, interview questions, and candidate tracking context.", "url": "https://recruitpilot-ai.streamlit.app/"},
    "process": {"app": "SOPPilot AI", "why": "The biggest need is process documentation, training consistency, SOP creation, or quality control.", "url": "https://soppilot-ai.streamlit.app/"},
}

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


def section_title(title: str, lede: str | None = None) -> None:
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
    if lede:
        st.markdown(f'<div class="section-lede">{lede}</div>', unsafe_allow_html=True)


def form_group(title: str) -> None:
    st.markdown(f'<div class="form-group-title">{title}</div>', unsafe_allow_html=True)


def metric_card(label: str, value: str, note: str | None = None) -> None:
    note_html = f'<div class="metric-note">{note}</div>' if note else ""
    st.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div>{note_html}</div>', unsafe_allow_html=True)


def html_card(title: str, body: str, css_class: str = "output-card") -> None:
    st.markdown(f'<div class="{css_class}"><h3>{title}</h3>{body}</div>', unsafe_allow_html=True)


def html_list(items: list[str]) -> str:
    return "<ul>" + "".join(f"<li>{item}</li>" for item in items) + "</ul>"


def md_to_html(text: str) -> str:
    return text.replace("\n", "<br>")


def score_maturity(tool_maturity: str, pain_points: list[str], urgency: str, team_size: str) -> tuple[int, str]:
    score = {"Mostly manual": 25, "Basic spreadsheets": 40, "CRM or project tool": 58, "Multiple tools but disconnected": 62, "Strong systems in place": 82}.get(tool_maturity, 45)
    score -= min(len(pain_points) * 4, 28)
    score -= {"Low": 0, "Medium": 3, "High": 7, "Critical": 12}.get(urgency, 3)
    score -= {"1-3 people": 0, "4-10 people": 2, "11-25 people": 4, "26+ people": 6}.get(team_size, 2)
    score = max(min(score, 100), 5)
    if score >= 75:
        label = "Strong Foundation"
    elif score >= 55:
        label = "Developing System"
    elif score >= 35:
        label = "Needs Structure"
    else:
        label = "High Friction"
    return score, label


def classify_bottleneck(pain_points: list[str]) -> str:
    categories = {
        "performance": ["Performance visibility is unclear", "Manager meetings lack clean numbers", "Lead source quality is hard to compare", "Reporting takes too much manual work"],
        "followup": ["Sales follow-up is inconsistent", "CRM notes or data are messy", "Customer communication is inconsistent"],
        "recruiting": ["Hiring/applicant review is inconsistent"],
        "process": ["Processes live in people’s heads", "Training is inconsistent"],
    }
    scores = {key: sum(1 for point in pain_points if point in values) for key, values in categories.items()}
    if not pain_points:
        return "performance"
    return max(scores, key=scores.get)


def automation_opportunities(primary_key: str, pain_points: list[str]) -> list[str]:
    base = {
        "performance": ["Create a weekly KPI scorecard", "Standardize rep and lead source reporting", "Build a manager brief template"],
        "followup": ["Standardize CRM notes", "Create copy-ready follow-up templates", "Add a next-best-action workflow"],
        "recruiting": ["Create a resume review packet", "Standardize interview questions", "Add a candidate tracker export"],
        "process": ["Document top recurring workflows", "Create SOP checklists", "Add process ownership and review dates"],
    }.get(primary_key, [])
    if "Reporting takes too much manual work" in pain_points:
        base.append("Automate recurring report generation")
    if "CRM notes or data are messy" in pain_points:
        base.append("Define required CRM fields and note structure")
    return base[:5]


def roadmap(primary_key: str) -> list[str]:
    roadmaps = {
        "performance": ["Week 1: Define the 5-7 KPIs managers need every week", "Week 2: Clean sample data and build a repeatable scorecard", "Week 3: Review rep and lead source performance patterns", "Week 4: Use the scorecard to run one manager meeting and adjust"],
        "followup": ["Week 1: Map current lead statuses and follow-up gaps", "Week 2: Build text/email/voicemail templates", "Week 3: Standardize CRM notes and next-step language", "Week 4: Review missed opportunities and coach follow-up discipline"],
        "recruiting": ["Week 1: Define role requirements and applicant review criteria", "Week 2: Standardize resume review packets", "Week 3: Build follow-up questions and candidate tracking fields", "Week 4: Review hiring process consistency"],
        "process": ["Week 1: Pick the top 3 repeatable processes causing confusion", "Week 2: Draft SOPs and checklists", "Week 3: Train the team using the new documentation", "Week 4: Review adoption, gaps, and next SOP priority"],
    }
    return roadmaps.get(primary_key, roadmaps["performance"])


def action_plan(primary_key: str, business_name: str) -> list[str]:
    name = business_name or "the business"
    return {
        "performance": [f"Audit the current weekly reporting process for {name}.", "Define the manager scorecard before adding new tools.", "Start with OpsPilot AI to turn activity data into action items."],
        "followup": [f"Map how {name} currently follows up after each customer interaction.", "Create required CRM notes and next-step language.", "Start with FollowUpPilot AI to standardize customer communication."],
        "recruiting": [f"Collect the current job description and applicant review process for {name}.", "Define what information should be reviewed by humans before interviews.", "Start with RecruitPilot AI to organize applicant review packets."],
        "process": [f"Identify the process at {name} that gets explained repeatedly.", "Turn that workflow into an SOP, checklist, and training plan.", "Start with SOPPilot AI to document and package the process."],
    }[primary_key]


def build_rules_summary(inputs: dict, score: int, label: str, primary_key: str, recommendation: dict, opportunities: list[str], actions: list[str]) -> str:
    return f"""The business is currently at **{label}** with a workflow maturity score of **{score}%**. The primary bottleneck appears to be **{primary_key.title()}**, based on the selected pain points and current operating state.

The best starting point is **{recommendation['app']}** because {recommendation['why']}

Recommended first opportunities:
{chr(10).join(f'- {item}' for item in opportunities)}

Recommended first action: {actions[0]}
"""


def build_ai_prompt(inputs: dict, rules_summary: str, roadmap_steps: list[str]) -> str:
    return f"""
You are an AI operations consultant for small and mid-sized businesses.
Use the structured diagnostic below to write a concise executive diagnostic summary.
Do not invent facts. Keep the recommendation practical and action-oriented.

Business profile:
{inputs}

Rules-based diagnostic:
{rules_summary}

Roadmap:
{roadmap_steps}

Return:
1. Executive diagnosis
2. Likely root cause
3. Business risk if nothing changes
4. First workflow improvement to tackle
5. 30-day action plan
"""


def build_report(inputs: dict, score: int, label: str, primary_key: str, recommendation: dict, opportunities: list[str], roadmap_steps: list[str], actions: list[str], executive_summary: str) -> str:
    pain_lines = "\n".join(f"- {item}" for item in inputs["pain_points"]) or "- No pain points selected."
    opp_lines = "\n".join(f"- {item}" for item in opportunities)
    roadmap_lines = "\n".join(f"- {item}" for item in roadmap_steps)
    action_lines = "\n".join(f"- {item}" for item in actions)
    return f"""# ClientOps Intake AI Diagnostic Report

## Executive Diagnostic Summary
{executive_summary}

## Business Profile
Business Name: {inputs['business_name'] or 'N/A'}
Business Type: {inputs['business_type']}
Team Size: {inputs['team_size']}
Revenue Stage: {inputs['revenue_stage']}
Tool Maturity: {inputs['tool_maturity']}
Urgency: {inputs['urgency']}

## Selected Pain Points
{pain_lines}

## Workflow Maturity
Score: {score}%
Status: {label}

## Primary Bottleneck
{primary_key.title()}

## Recommended Toolkit App
{recommendation['app']}

Why: {recommendation['why']}

## Automation Opportunities
{opp_lines}

## 30-Day Improvement Roadmap
{roadmap_lines}

## Manager Action Plan
{action_lines}

## Current Process Notes
{inputs['current_process'] or 'Not provided.'}

## Desired Outcome
{inputs['desired_outcome'] or 'Not provided.'}

---
Generated by ClientOps Intake AI.
"""


with st.sidebar:
    st.title("ClientOps Intake AI")
    st.caption("Version 1.2")
    st.markdown("Diagnostic intake assistant for workflow bottlenecks, maturity scoring, automation opportunities, and 30-day roadmaps.")
    st.divider()
    st.markdown("### Outputs")
    st.markdown("- Maturity score\n- Primary bottleneck\n- Recommended toolkit app\n- Automation opportunities\n- 30-day roadmap\n- PDF diagnostic report")

st.markdown("""
<div class="hero"><div class="eyebrow">Client Diagnostic Intake Assistant</div><div class="hero-title">ClientOps Intake AI</div><div class="hero-subtitle">Diagnose business workflow bottlenecks, score operational maturity, recommend automation opportunities, match the right toolkit app, and generate a 30-day improvement roadmap.</div><div class="hero-pills"><span>Workflow Diagnostics</span><span>Operations</span><span>AI Consulting</span><span>Roadmaps</span><span>Streamlit</span></div></div>
""", unsafe_allow_html=True)

section_title("Diagnostic intake", "Load a sample scenario or enter a fictional business profile to generate a workflow improvement diagnostic.")
scenario_name = st.selectbox("Load Sample Scenario", list(SAMPLE_SCENARIOS.keys()))
scenario = SAMPLE_SCENARIOS.get(scenario_name, {})

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
    current_process = st.text_area("How does the current workflow operate today?", value=scenario.get("current_process", ""), height=120)
    desired_outcome = st.text_area("What outcome would make the biggest difference?", value=scenario.get("desired_outcome", ""), height=120)
    submitted = st.form_submit_button("Generate ClientOps Diagnostic", use_container_width=True)

if not submitted:
    st.markdown('<div class="note-box">Complete the intake or load a sample scenario, then generate the diagnostic report.</div>', unsafe_allow_html=True)
    st.stop()

inputs = {"business_name": business_name, "business_type": business_type, "team_size": team_size, "revenue_stage": revenue_stage, "tool_maturity": tool_maturity, "urgency": urgency, "pain_points": pain_points, "current_process": current_process, "desired_outcome": desired_outcome}
score, label = score_maturity(tool_maturity, pain_points, urgency, team_size)
primary_key = classify_bottleneck(pain_points)
recommendation = TOOL_RECOMMENDATIONS[primary_key]
opportunities = automation_opportunities(primary_key, pain_points)
roadmap_steps = roadmap(primary_key)
actions = action_plan(primary_key, business_name)
rules_summary = build_rules_summary(inputs, score, label, primary_key, recommendation, opportunities, actions)
ai_prompt = build_ai_prompt(inputs, rules_summary, roadmap_steps)
summary_cache_key = stable_cache_key("clientops_summary", inputs)
executive_summary = enhance_text(ai_prompt, rules_summary, summary_cache_key)
report = build_report(inputs, score, label, primary_key, recommendation, opportunities, roadmap_steps, actions, executive_summary)
pdf_report = markdown_to_pdf(report, title="ClientOps Intake AI Diagnostic Report")

section_title("Diagnostic snapshot")
mc1, mc2, mc3, mc4 = st.columns(4)
with mc1:
    metric_card("Maturity Score", f"{score}%", label)
with mc2:
    metric_card("Primary Bottleneck", primary_key.title())
with mc3:
    metric_card("Recommended App", recommendation["app"])
with mc4:
    metric_card("Urgency", urgency)

section_title("Executive diagnostic summary")
html_card("Recommended Direction", f"<p>{md_to_html(executive_summary)}</p>", "workflow-card")
st.link_button(f"Open {recommendation['app']}", recommendation["url"], use_container_width=True)

section_title("Automation opportunities")
html_card("Recommended Opportunities", html_list(opportunities), "success-card")

section_title("30-day improvement roadmap")
road_cols = st.columns(2)
for idx, step in enumerate(roadmap_steps):
    with road_cols[idx % 2]:
        html_card(f"Roadmap Step {idx + 1}", f"<p>{step}</p>", "workflow-card")

section_title("Manager action plan")
html_card("Next Actions", html_list(actions), "output-card")

section_title("Download diagnostic report")
st.download_button("Download Diagnostic Report PDF", data=pdf_report, file_name="clientops-diagnostic-report.pdf", mime="application/pdf", use_container_width=True)

section_title("What this app demonstrates")
html_card("Portfolio Skills Shown", "<ul><li>AI-enhanced consulting summary with rules-based fallback</li><li>Consulting-style intake workflow design</li><li>Rules-based maturity scoring</li><li>Bottleneck diagnosis and tool routing</li><li>Roadmap generation</li><li>User-friendly PDF reporting</li></ul>", "success-card")

with st.expander("How to use ClientOps Intake AI"):
    st.markdown("1. Load a sample scenario or enter a fictional business profile.\n2. Select the current workflow pain points.\n3. Generate the diagnostic.\n4. Review the maturity score, bottleneck, recommended app, automation opportunities, and roadmap.\n5. Download the PDF diagnostic report.")

st.markdown('<div class="note-box">Public demo note: All sample names, companies, and scenarios are fictional and created for portfolio demonstration.</div>', unsafe_allow_html=True)
