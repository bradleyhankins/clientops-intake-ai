# ClientOps Intake AI

ClientOps Intake AI is an AI-enhanced diagnostic intake assistant for small-business operators, managers, and consultants. It helps identify workflow bottlenecks, score operational maturity, recommend automation opportunities, match the user to the right AI Ops Toolkit app, and generate a 30-day improvement roadmap.

## Live Demo

[Launch ClientOps Intake AI](https://clientops-intake-ai.streamlit.app/)

## Current Version: v1.1

ClientOps Intake AI combines a rules-based diagnostic engine with embedded AI-enhanced summary generation.

The app is designed to work in two layers:

1. **Rules-based core:** scores maturity, identifies bottlenecks, recommends the right toolkit app, builds automation opportunities, and creates a 30-day roadmap.
2. **Embedded AI layer:** when an OpenAI token is available, the app quietly enhances the executive diagnostic summary with a more polished consulting-style explanation.

If the AI call fails or an API key is unavailable, the app silently falls back to the rules-based diagnostic. The user experience stays the same.

## Why this project exists

Small businesses often know that operations feel messy, but they do not always know which workflow to fix first.

ClientOps Intake AI acts as the front door to the Practical AI Ops Toolkit by diagnosing common operating problems across performance visibility, sales follow-up, applicant review, process documentation, and manager reporting.

## What it analyzes

- Performance visibility
- Sales follow-up consistency
- CRM/process documentation
- Applicant review workflow
- SOP and training consistency
- Manager reporting rhythm
- Current tool maturity
- Operational urgency
- Team size and workflow complexity

## Workflow Outputs

- Business profile intake
- Workflow pain-point selection
- Operational maturity score
- Primary bottleneck diagnosis
- Recommended AI Ops Toolkit app
- Automation opportunities
- AI-enhanced executive diagnostic summary with rules-based fallback
- 30-day improvement roadmap
- Manager action plan
- Downloadable diagnostic report

## Export Strategy

Current export:

- Markdown diagnostic report (`.md`) for GitHub-friendly and developer-friendly documentation

Planned next upgrade:

- PDF diagnostic report for a more user-friendly manager/client deliverable

The markdown export is useful for transparency and version control, but PDF is the better format for non-technical users.

## Suggested Test Flow

1. Launch the live app.
2. Load the sample scenario or enter a fictional business profile.
3. Select the biggest workflow problems.
4. Generate the diagnostic report.
5. Review the maturity score, primary bottleneck, recommended toolkit app, AI-enhanced diagnostic summary, and 30-day roadmap.
6. Download the diagnostic report.

## Screenshots

Screenshots will be refreshed after the embedded AI and PDF export pass.

## Tech Stack

- Python
- Streamlit
- OpenAI API integration
- Rules-based diagnostic logic
- Silent AI fallback pattern
- Markdown report export
- GitHub
- Streamlit Community Cloud

## Run Locally

```bash
py -m pip install -r requirements.txt
py -m streamlit run app.py
```

## Environment Variables

To enable embedded AI output:

```bash
OPENAI_TOKEN=your_api_key_here
```

The app still works without this token by using the rules-based fallback.

## Public Demo Note

All sample data, names, companies, and scenarios used in this project are fictional and created for public portfolio demonstration purposes.

## Case Study

### Problem

Small businesses often experience operational friction but lack a clear method for deciding what to fix first. Problems may show up as inconsistent follow-up, weak reporting, scattered applicant review notes, undocumented processes, or limited manager visibility.

### Solution

ClientOps Intake AI guides a user through a structured diagnostic intake, scores workflow maturity, identifies the primary bottleneck, recommends a relevant toolkit app, and creates a 30-day action roadmap. The embedded AI layer improves the executive summary when available while preserving a reliable rules-based fallback.

### Business Value

ClientOps Intake AI helps operators move from vague operational frustration to a clear first action. It supports better prioritization, faster consulting discovery, and more structured workflow improvement planning.

## Built By

Bradley Hankins  
Operations & Revenue Leader | AI Workflow Automation | RevOps & Process Improvement
