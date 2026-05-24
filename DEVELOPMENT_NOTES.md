# Development Notes

## Build Philosophy

ClientOps Intake AI is designed as a practical diagnostic assistant for small-business workflow analysis.

The app helps users move from vague operational pain to a clear first improvement path.

## Engineering Priorities

1. Clear diagnostic intake workflow
2. Transparent scoring and recommendation logic
3. Actionable automation opportunities
4. 30-day roadmap generation
5. Public-safe sample scenarios
6. Simple deployment on Streamlit Community Cloud

## Current Tradeoffs

The app currently keeps deployment logic in `app.py` for simplicity and easy review. A future production version should split configuration, scoring, roadmap generation, components, and styling into separate modules.

## Future Refactor Plan

A future production-oriented version should split the app into:

```text
src/config.py
src/diagnostic_logic.py
src/roadmap.py
src/reports.py
src/components.py
src/styles.css
```

## Testing Opportunities

The most valuable future tests would cover:

- Workflow maturity scoring
- Primary bottleneck classification
- Toolkit app recommendation mapping
- Automation opportunity generation
- Roadmap generation
- Markdown diagnostic report generation

## Code Quality Roadmap

Potential future tooling:

- Ruff for linting and formatting
- Pytest for diagnostic logic tests
- Pre-commit hooks
- GitHub Actions smoke checks
