def route_request(query):

    query_lower = query.lower()

    # -----------------------------
    # RAG QUESTIONS
    # -----------------------------

    if "what is" in query_lower:
        return "rag"

    # -----------------------------
    # REPO ANALYSIS
    # -----------------------------

    elif (
        "analyze" in query_lower
        or "analyse" in query_lower
        or "github" in query_lower
        or "repo" in query_lower
    ):
        return "analyze_repos"

    # -----------------------------
    # SUMMARIZATION
    # -----------------------------

    elif (
        "summarize" in query_lower
        or "summarise" in query_lower
        or "summary" in query_lower
    ):
        return "summarizer"

    # -----------------------------
    # FALLBACK
    # -----------------------------

    return "unknown"