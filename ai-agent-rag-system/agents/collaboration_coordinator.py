from agents.research_agent import research
from agents.planner_agent import plan_from_research
from agents.execution_agent import execute_from_plan
from agents.critic_agent import review_execution
from agents.agent_message import print_message


def run_collaboration(query):
    research_msg = research(query)
    print_message(research_msg)

    plan_msg = plan_from_research(research_msg)
    print_message(plan_msg)

    execution_msg = execute_from_plan(plan_msg)
    print_message(execution_msg)

    critique_msg = review_execution(execution_msg)
    print_message(critique_msg)

    return {
        "query": query,
        "research": research_msg["content"],
        "plan": plan_msg["content"]["plan"],
        "results": execution_msg["content"]["results"],
        "critique": critique_msg["content"]["critique"]
    }