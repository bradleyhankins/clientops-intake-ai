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
        "pain_points": [
            "Performance visibility is unclear",
            "Sales follow-up is inconsistent",
            "CRM notes or data are messy",
            "Manager meetings lack clean numbers",
        ],
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
        "pain_points": [
            "Processes live in people’s heads",
            "Training is inconsistent",
            "Reporting takes too much manual work",
            "Customer communication is inconsistent",
        ],
        "current_process": "The team has experienced managers, but most processes are taught verbally and vary by employee.",
        "desired_outcome": "Document repeatable processes and create better training consistency.",
    },
}

TOOL_RECOMMENDATIONS = {
    "performance": {
        "app": "OpsPilot AI",
        "why": "The biggest need is manager visibility, KPI reporting, rep performance review, or lead source analysis.",
        "url": "https://opspilot-ai.streamlit.app/",
    },
    "followup": {
        "app": "FollowUpPilot AI",
        "why": "The biggest need is stronger customer communication, CRM notes, follow-up timing, or sales execution discipline.",
        "url": "https://followuppilot-ai.streamlit.app/",
    },
    "recruiting": {
        "app": "RecruitPilot AI",
        "why": "The biggest need is organizing applicant review, resume notes, interview questions, and candidate tracking context.",
        "url": "https://recruitpilot-ai.streamlit.app/",
    },
    "process": {
        "app": "SOPPilot AI",
        "why": "The biggest need is process documentation, training consistency, SOP creation, or quality control.",
        "url": "https://soppilot-ai.streamlit.app/",
    },
}
