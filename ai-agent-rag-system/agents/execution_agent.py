from core.agent_executor import execute_plan
from agents.agent_message import create_message


def execute_from_plan(plan_message):
    plan = plan_message["content"]["plan"]
    query = plan_message["content"]["query"]

    results = execute_plan(plan)

    return create_message(
        sender="Execution Agent",
        receiver="Critic Agent",
        content={
            "query": query,
            "results": results,
            "research_notes": plan_message["content"]["research_notes"]
        }
    )