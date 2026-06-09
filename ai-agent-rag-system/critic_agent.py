from critic import llm_critique


def review(query, results):
    return llm_critique(
        query,
        results
    )