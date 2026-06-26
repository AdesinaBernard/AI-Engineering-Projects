def select_tool(task_description):

    task_lower = task_description.lower()

    if (
        "repo" in task_lower
        or "repository" in task_lower
        or "github" in task_lower
    ):
        reasoning = "Need repository analysis."
        tool = "analyze_repos"

    elif (
        "summarize" in task_lower
        or "summarise" in task_lower
    ):
        reasoning = "Need text summarization."
        tool = "summarizer"

    else:
        reasoning = "Need factual retrieval."
        tool = "rag"

    print(f"[Tool Selector] {tool} -> {reasoning}")

    return tool