from evaluation.critic import llm_critique
from agent_message import create_message


def review(query, results):
    critique = llm_critique(
        query,
        results
    )

    return critique


def review_execution(execution_message):
    query = execution_message["content"]["query"]
    results = execution_message["content"]["results"]

    critique = llm_critique(
        query,
        results
    )

    return create_message(
        sender="Critic Agent",
        receiver="Coordinator",
        content={
            "query": query,
            "results": results,
            "critique": critique,
            "research_notes": execution_message["content"]["research_notes"]
        }
    )