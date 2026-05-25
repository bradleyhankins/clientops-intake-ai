# ClientOps Intake AI

ClientOps Intake AI is an AI-enhanced diagnostic intake assistant for small-business operators, managers, and consultants. It helps identify workflow bottlenecks, score operational maturity, recommend automation opportunities, match the user to the right AI Ops Toolkit app, and generate a 30-day improvement roadmap.

## Live Demo

[Launch ClientOps Intake AI](https://clientops-intake-ai.streamlit.app/)

## Current Version: v1.3

ClientOps Intake AI combines a deterministic rules-based diagnostic engine with embedded AI-enhanced summary generation.

The app is designed to work in two layers:

1. **Rules-based core:** scores maturity, identifies bottlenecks, recommends the right toolkit app, builds automation opportunities, and creates a 30-day roadmap.
2. **Embedded AI layer:** when an OpenAI token is available, the app quietly enhances the executive diagnostic summary with a more polished consulting-style explanation.

If the AI call fails or an API key is unavailable, the app silently falls back to the rules-based diagnostic. The user experience stays the same.

## Architecture

ClientOps has been refactored from a single-file prototype into a modular Streamlit application.

```text
clientops-intake-ai/
├── app.py
├── ai_helpers.py
├── pdf_helpers.py
├── requirements.txt
├── core/
│   ├── __init__.py
│   ├── diagnostics.py
│   ├── prompts.py
│   └── report_builder.py
├── data/
│   ├── __init__.py
│   └── sample_data.py
└── tests/
    └── test_diagnostics.py
```

### Module Responsibilities

- `app.py` handles Streamlit layout, form inputs, rendering, and orchestration.
- `core/diagnostics.py` contains scoring, bottleneck classification, opportunity logic, roadmap logic, and the main diagnostic runner.
- `core/prompts.py` contains rules-based summary and AI prompt construction.
- `core/report_builder.py` builds the structured report content used for PDF export.
- `data/sample_data.py` stores sample scenarios, selectbox options, pain points, and toolkit routing data.
- `ai_helpers.py` manages OpenAI access, guardrails, prompt length control, and silent fallback behavior.
- `pdf_helpers.py` converts structured report text into a downloadable PDF.

## AI Design Pattern

The guiding principle is:

```text
Rules decide. AI polishes. Guardrails constrain. Fallback protects.
```

The rules-based diagnostic remains the source of truth for:

- Maturity score
- Primary bottleneck
- Recommended toolkit app
- Automation opportunities
- 30-day roadmap
- Manager action plan

The AI layer is used only to improve the clarity and usefulness of the executive diagnostic summary. It should not change scores, recommendations, app routing, or business facts.

## Privacy and Responsible Use

This public demo is designed for fictional or sample data.

Users should not enter sensitive, confidential, or regulated business information. When AI enhancement is enabled, text entered into the app may be processed by the configured AI provider for output enhancement.

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
- Downloadable PDF diagnostic report

## Export Strategy

Current user-facing export:

- PDF diagnostic report for a manager/client-ready deliverable

The app no longer exposes Markdown as the primary user-facing download because non-technical users expect a polished PDF report.

## Suggested Test Flow

1. Launch the live app.
2. Load the sample scenario or enter a fictional business profile.
3. Select the biggest workflow problems.
4. Generate the diagnostic report.
5. Review the maturity score, primary bottleneck, recommended toolkit app, AI-enhanced diagnostic summary, and 30-day roadmap.
6. Download the PDF diagnostic report.

## Automated Tests

This repo includes unit tests for the deterministic diagnostic logic.

Run tests locally with:

```bash
py -m pip install -r requirements.txt
py -m pip install pytest
py -m pytest
```

GitHub Actions runs the test suite automatically on push and pull request events.

## Screenshots

Screenshots will be refreshed after the final UI and PDF polish pass.

## Tech Stack

- Python
- Streamlit
- OpenAI API integration
- Rules-based diagnostic logic
- Modular app architecture
- Silent AI fallback pattern
- PDF report export
- Pytest
- GitHub Actions
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
