from agents.research_agent import research
from core.agent_executor import execute_plan
from agents.critic_agent import review
from planning.advanced_planner import create_advanced_plan
from agents.long_horizon_agent import run_goal


def coordinate(query):

    query_lower = query.lower()

    if (
        "research" in query_lower
        and "numpy" in query_lower
    ):
        print("\n[Long Horizon Agent]")
        return run_goal(query)

    print("\n[Research Agent]")
    research_result = research(query)

    print(research_result)

    print("\n[Planning Agent]")
    plan = create_advanced_plan(query)

    print(plan)

    print("\n[Execution Agent]")
    results = execute_plan(plan)

    print("\n[Critic Agent]")
    critique = review(query, results)

    return {
        "research": research_result,
        "results": results,
        "critique": critique
    }