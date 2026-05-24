import streamlit as st

from ai_helpers import generate_ai_text

st.set_page_config(page_title="ClientOps Intake AI - AI Consultant Summary", page_icon="🧭", layout="wide")

st.title("AI Consultant Summary")
st.caption("Optional AI enhancement for turning a business intake into a consulting-style diagnostic memo.")

st.info(
    "This page is optional. The main ClientOps diagnostic still works without AI. "
    "Set OPENAI_TOKEN in the deployment environment to enable AI output."
)

business_context = st.text_area(
    "Business context / intake notes",
    height=220,
    placeholder="Describe the business, team size, tools, pain points, reporting gaps, follow-up issues, or process problems.",
)
structured_results = st.text_area(
    "Rules-based diagnostic results",
    height=180,
    placeholder="Paste the maturity score, primary bottleneck, recommended app, automation opportunities, and roadmap from ClientOps.",
)
summary_style = st.selectbox(
    "Summary style",
    ["Executive memo", "Consulting discovery note", "30-day implementation plan", "Sales/RevOps recommendation", "Operations audit summary"],
)

if st.button("Generate AI Consultant Summary", use_container_width=True):
    prompt = f"""
You are an AI operations consultant for small and mid-sized businesses.
Write a concise, practical diagnostic memo from the intake notes and structured results.
Keep recommendations realistic and operationally specific.
Do not invent facts that are not provided.

Summary style: {summary_style}

Business context / intake notes:
{business_context}

Structured diagnostic results:
{structured_results}

Return:
1. Executive diagnosis
2. Likely root cause
3. Business risk if nothing changes
4. First recommended workflow improvement
5. 30-day action plan
6. Recommended toolkit app and why
"""
    with st.spinner("Generating AI consultant summary..."):
        st.markdown(generate_ai_text(prompt))

st.divider()
st.markdown(
    "**AI positioning:** This page adds a consulting-style narrative layer on top of ClientOps' structured diagnostic scoring."
)
