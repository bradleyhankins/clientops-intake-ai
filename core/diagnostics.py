from data.sample_data import TOOL_RECOMMENDATIONS


def score_maturity(tool_maturity: str, pain_points: list[str], urgency: str, team_size: str) -> tuple[int, str]:
    score = {
        "Mostly manual": 25,
        "Basic spreadsheets": 40,
        "CRM or project tool": 58,
        "Multiple tools but disconnected": 62,
        "Strong systems in place": 82,
    }.get(tool_maturity, 45)
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
        "performance": [
            "Performance visibility is unclear",
            "Manager meetings lack clean numbers",
            "Lead source quality is hard to compare",
            "Reporting takes too much manual work",
        ],
        "followup": [
            "Sales follow-up is inconsistent",
            "CRM notes or data are messy",
            "Customer communication is inconsistent",
        ],
        "recruiting": ["Hiring/applicant review is inconsistent"],
        "process": ["Processes live in people’s heads", "Training is inconsistent"],
    }
    scores = {key: sum(1 for point in pain_points if point in values) for key, values in categories.items()}
    if not pain_points:
        return "performance"
    return max(scores, key=scores.get)


def automation_opportunities(primary_key: str, pain_points: list[str]) -> list[str]:
    base = {
        "performance": [
            "Create a weekly KPI scorecard",
            "Standardize rep and lead source reporting",
            "Build a manager brief template",
        ],
        "followup": [
            "Standardize CRM notes",
            "Create copy-ready follow-up templates",
            "Add a next-best-action workflow",
        ],
        "recruiting": [
            "Create a resume review packet",
            "Standardize interview questions",
            "Add a candidate tracker export",
        ],
        "process": [
            "Document top recurring workflows",
            "Create SOP checklists",
            "Add process ownership and review dates",
        ],
    }.get(primary_key, [])
    if "Reporting takes too much manual work" in pain_points:
        base.append("Automate recurring report generation")
    if "CRM notes or data are messy" in pain_points:
        base.append("Define required CRM fields and note structure")
    return base[:5]


def roadmap(primary_key: str) -> list[str]:
    roadmaps = {
        "performance": [
            "Week 1: Define the 5-7 KPIs managers need every week",
            "Week 2: Clean sample data and build a repeatable scorecard",
            "Week 3: Review rep and lead source performance patterns",
            "Week 4: Use the scorecard to run one manager meeting and adjust",
        ],
        "followup": [
            "Week 1: Map current lead statuses and follow-up gaps",
            "Week 2: Build text/email/voicemail templates",
            "Week 3: Standardize CRM notes and next-step language",
            "Week 4: Review missed opportunities and coach follow-up discipline",
        ],
        "recruiting": [
            "Week 1: Define role requirements and applicant review criteria",
            "Week 2: Standardize resume review packets",
            "Week 3: Build follow-up questions and candidate tracking fields",
            "Week 4: Review hiring process consistency",
        ],
        "process": [
            "Week 1: Pick the top 3 repeatable processes causing confusion",
            "Week 2: Draft SOPs and checklists",
            "Week 3: Train the team using the new documentation",
            "Week 4: Review adoption, gaps, and next SOP priority",
        ],
    }
    return roadmaps.get(primary_key, roadmaps["performance"])


def action_plan(primary_key: str, business_name: str) -> list[str]:
    name = business_name or "the business"
    return {
        "performance": [
            f"Audit the current weekly reporting process for {name}.",
            "Define the manager scorecard before adding new tools.",
            "Start with OpsPilot AI to turn activity data into action items.",
        ],
        "followup": [
            f"Map how {name} currently follows up after each customer interaction.",
            "Create required CRM notes and next-step language.",
            "Start with FollowUpPilot AI to standardize customer communication.",
        ],
        "recruiting": [
            f"Collect the current job description and applicant review process for {name}.",
            "Define what information should be reviewed by humans before interviews.",
            "Start with RecruitPilot AI to organize applicant review packets.",
        ],
        "process": [
            f"Identify the process at {name} that gets explained repeatedly.",
            "Turn that workflow into an SOP, checklist, and training plan.",
            "Start with SOPPilot AI to document and package the process.",
        ],
    }[primary_key]


def run_diagnostic(inputs: dict) -> dict:
    score, label = score_maturity(
        inputs["tool_maturity"],
        inputs["pain_points"],
        inputs["urgency"],
        inputs["team_size"],
    )
    primary_key = classify_bottleneck(inputs["pain_points"])
    recommendation = TOOL_RECOMMENDATIONS[primary_key]
    opportunities = automation_opportunities(primary_key, inputs["pain_points"])
    roadmap_steps = roadmap(primary_key)
    actions = action_plan(primary_key, inputs["business_name"])
    return {
        "score": score,
        "label": label,
        "primary_key": primary_key,
        "recommendation": recommendation,
        "opportunities": opportunities,
        "roadmap_steps": roadmap_steps,
        "actions": actions,
    }
