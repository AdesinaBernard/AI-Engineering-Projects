from sentence_transformers import SentenceTransformer
import numpy as np
import json
import os

from memory.conversation_memory import (
    save_message,
    get_recent_context
)


model = SentenceTransformer("all-MiniLM-L6-v2")

VECTOR_DB_FILE = "data/vector_db.json"


def load_vector_db():
    if not os.path.exists(VECTOR_DB_FILE):
        raise FileNotFoundError(
            "Vector database not found. Run: python -m rag.ingest"
        )

    with open(VECTOR_DB_FILE, "r") as f:
        return json.load(f)


def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)

    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )


def build_contextual_query(query, use_history=False):
    if not use_history:
        return query

    history = get_recent_context()

    if not history:
        return query

    return f"""
Conversation History:
{history}

Current Query:
{query}
"""


def semantic_search(query, top_k=5, use_history=False):
    db = load_vector_db()

    contextual_query = build_contextual_query(
        query,
        use_history=use_history
    )

    query_embedding = model.encode([contextual_query])[0]

    scores = []

    for item in db:
        similarity = cosine_similarity(
            query_embedding,
            item["embedding"]
        )

        scores.append({
            "source": item.get("source", "unknown"),
            "text": item["text"],
            "score": float(similarity)
        })

    ranked = sorted(
        scores,
        key=lambda x: x["score"],
        reverse=True
    )

    return ranked[:top_k]


if __name__ == "__main__":

    while True:
        query = input("\nAsk something: ").strip()

        if query.lower() == "exit":
            break

        save_message("user", query)

        results = semantic_search(
            query,
            top_k=5,
            use_history=False
        )

        print("\nTop Matches:\n")

        for item in results:
            print(f"Score: {item['score']:.4f}")
            print(f"Source: {item['source']}")
            print(item["text"])
            print("-" * 40)

        if results:
            save_message(
                "assistant",
                results[0]["text"]
            )