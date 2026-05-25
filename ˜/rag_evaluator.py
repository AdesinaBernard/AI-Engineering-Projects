def evaluate_retrieval(retrieved_chunks, threshold=0.30):
    if not retrieved_chunks:
        return {
            "passed": False,
            "reason": "No chunks retrieved",
            "top_score": 0
        }

    top_score = retrieved_chunks[0]["score"]

    if top_score < threshold:
        return {
            "passed": False,
            "reason": "Top retrieval score below confidence threshold",
            "top_score": top_score
        }

    return {
        "passed": True,
        "reason": "Relevant context found",
        "top_score": top_score
    }


def format_sources(retrieved_chunks):
    sources = []

    for item in retrieved_chunks:
        sources.append({
            "source": item["source"],
            "score": round(item["score"], 4),
            "preview": item["text"][:120]
        })

    return sources