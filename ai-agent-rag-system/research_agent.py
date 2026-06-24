from agent_message import create_message


def research(query):
    notes = {
        "query": query,
        "notes": f"Initial research notes for: {query}",
        "suggested_focus": [
            "background",
            "technical relevance",
            "practical use cases"
        ]
    }

    return create_message(
        sender="Research Agent",
        receiver="Planner Agent",
        content=notes
    )