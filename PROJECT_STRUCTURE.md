# Project Structure

```text
.
├── app.py                  # Streamlit application entrypoint
├── README.md               # Project overview, case study, and test flow
├── ARCHITECTURE.md         # Architecture and design decisions
├── PROJECT_STRUCTURE.md    # Repository structure reference
├── DEVELOPMENT_NOTES.md    # Implementation notes and future refactor plan
├── requirements.txt        # Python dependencies
└── screenshots/            # README screenshots after deployment
```

## Current File Responsibilities

### `app.py`

Contains the deployed Streamlit diagnostic app.

Responsibilities:

- Page configuration
- Sample scenario data
- Diagnostic intake workflow
- Maturity scoring
- Bottleneck classification
- Toolkit app recommendation logic
- Automation opportunity generation
- 30-day roadmap generation
- Manager action-plan generation
- Markdown report export
- Streamlit UI rendering

## Future Production Structure

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

The current structure prioritizes fast deployment and public portfolio review while documenting a path toward a modular production build.
