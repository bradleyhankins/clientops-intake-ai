# Architecture

ClientOps Intake AI is a Streamlit diagnostic intake assistant for business workflow analysis, operational maturity scoring, automation opportunity mapping, and 30-day roadmap generation.

## Current Architecture

The current version is optimized for simple Streamlit Community Cloud deployment and easy GitHub review.

```text
app.py
README.md
requirements.txt
screenshots/
```

## Application Layers

The app is currently deployed from one Streamlit entrypoint, but the code is organized conceptually into clear layers:

```text
Configuration
- Business type options
- Team size options
- Revenue stage options
- Tool maturity options
- Pain-point library
- Sample scenarios
- Toolkit app mappings

Diagnostic Logic
- Workflow maturity scoring
- Primary bottleneck classification
- Automation opportunity generation
- Toolkit app recommendation logic
- 30-day roadmap generation
- Manager action-plan generation

Report Generation
- Downloadable Markdown diagnostic report

Presentation
- Streamlit intake form
- Diagnostic snapshot cards
- Recommendation section
- Roadmap cards
- Download workflow
```

## Design Choices

ClientOps Intake AI uses transparent rules-based logic to keep the diagnostic explainable and easy to adapt.

Key design goals:

- Help users clarify the first workflow to fix
- Route users to the right toolkit app
- Make business diagnosis simple and actionable
- Create manager-ready roadmap outputs
- Use fictional public-safe sample scenarios

## Why Single-File for This Version

The current single-file app keeps deployment simple for a portfolio project. A production version would separate scoring logic, configuration, components, and report generation.

## Future Production Layout

```text
app.py
src/
  config.py
  diagnostic_logic.py
  roadmap.py
  reports.py
  components.py
  styles.css
tests/
  test_diagnostic_logic.py
  test_reports.py
```

## Future Refactor Plan

1. Move CSS into `styles.css`
2. Move diagnostic scoring into `src/diagnostic_logic.py`
3. Move roadmap generation into `src/roadmap.py`
4. Move report generation into `src/reports.py`
5. Add tests for maturity scoring and tool recommendation logic
