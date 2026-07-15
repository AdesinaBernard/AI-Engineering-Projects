from rag.vector_store import semantic_search


CONFIDENCE_THRESHOLD = 0.15


def ask_rag(query):
    results = semantic_search(
        query,
        top_k=3,
        use_history=False
    )

    if not results:
        return "I could not find that information in the knowledge base."

    top_score = results[0]["score"]

    if top_score < CONFIDENCE_THRESHOLD:
        return "I could not find that information in the knowledge base."

    context = "\n\n".join([
        item["text"]
        for item in results
        if item["score"] >= CONFIDENCE_THRESHOLD
    ])

    if not context.strip():
        return "I could not find that information in the knowledge base."

    return context