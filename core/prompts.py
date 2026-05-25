def build_rules_summary(inputs: dict, diagnostic: dict) -> str:
    opportunities = diagnostic["opportunities"]
    actions = diagnostic["actions"]
    recommendation = diagnostic["recommendation"]
    return f"""The business is currently at **{diagnostic['label']}** with a workflow maturity score of **{diagnostic['score']}%**. The primary bottleneck appears to be **{diagnostic['primary_key'].title()}**, based on the selected pain points and current operating state.

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
