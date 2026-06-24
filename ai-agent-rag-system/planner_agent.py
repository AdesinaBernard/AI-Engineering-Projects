from advanced_planner import create_advanced_plan
from agent_message import create_message


def plan_from_research(research_message):
    query = research_message["content"]["query"]

    plan = create_advanced_plan(query)

    return create_message(
        sender="Planner Agent",
        receiver="Execution Agent",
        content={
            "query": query,
            "plan": plan,
            "research_notes": research_message["content"]
        }
    )