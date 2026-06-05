import re


def extract_repo_name(query):
    """
    Extract GitHub repo names like owner/repo from the user query.
    Example: numpy/numpy, python/cpython
    """

    matches = re.findall(
        r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+",
        query
    )

    return matches


def create_advanced_plan(query):
    query_lower = query.lower()

    plan = []

    repo_names = extract_repo_name(query)

    # Repo analysis
    if (
        "repo" in query_lower
        or "github" in query_lower
        or repo_names
    ):
        if repo_names:
            repos = repo_names
        elif "numpy" in query_lower:
            repos = ["numpy/numpy"]
        elif "python" in query_lower or "cpython" in query_lower:
            repos = ["python/cpython"]
        else:
            repos = []

        if repos:
            plan.append({
                "tool": "analyze_repos",
                "input": repos
            })

    # RAG / explanation
    if (
        "what is" in query_lower
        or "explain" in query_lower
        or "why" in query_lower
        or "matters" in query_lower
    ):
        plan.append({
            "tool": "rag",
            "input": query
        })

    # Summarization
    if (
        "summarize" in query_lower
        or "summarise" in query_lower
        or "summary" in query_lower
    ):
        plan.append({
            "tool": "summarizer",
            "input": query
        })

    return plan