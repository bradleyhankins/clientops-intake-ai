from core.diagnostics import (
    automation_opportunities,
    classify_bottleneck,
    run_diagnostic,
    score_maturity,
)


def test_score_maturity_returns_score_and_label():
    score, label = score_maturity(
        tool_maturity="CRM or project tool",
        pain_points=["Performance visibility is unclear", "Sales follow-up is inconsistent"],
        urgency="Medium",
        team_size="4-10 people",
    )

    assert isinstance(score, int)
    assert 0 <= score <= 100
    assert label in {"Strong Foundation", "Developing System", "Needs Structure", "High Friction"}


def test_classify_bottleneck_defaults_to_performance_when_no_pain_points():
    assert classify_bottleneck([]) == "performance"


def test_classify_bottleneck_identifies_followup_issue():
    pain_points = [
        "Sales follow-up is inconsistent",
        "CRM notes or data are messy",
        "Customer communication is inconsistent",
    ]

    assert classify_bottleneck(pain_points) == "followup"


def test_automation_opportunities_adds_reporting_opportunity():
    opportunities = automation_opportunities(
        "performance",
        ["Reporting takes too much manual work"],
    )

    assert "Automate recurring report generation" in opportunities


def test_run_diagnostic_returns_expected_keys():
    inputs = {
        "business_name": "Sample Business",
        "business_type": "Home Services",
        "team_size": "4-10 people",
        "revenue_stage": "$1M-$3M",
        "tool_maturity": "CRM or project tool",
        "urgency": "High",
        "pain_points": [
            "Performance visibility is unclear",
            "Manager meetings lack clean numbers",
        ],
        "current_process": "Managers review notes and spreadsheets manually.",
        "desired_outcome": "Cleaner reporting and better accountability.",
    }

    diagnostic = run_diagnostic(inputs)

    assert diagnostic["primary_key"] == "performance"
    assert diagnostic["recommendation"]["app"] == "OpsPilot AI"
    assert isinstance(diagnostic["opportunities"], list)
    assert isinstance(diagnostic["roadmap_steps"], list)
    assert isinstance(diagnostic["actions"], list)
    assert len(diagnostic["roadmap_steps"]) == 4
