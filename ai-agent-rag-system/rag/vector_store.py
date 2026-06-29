from sentence_transformers import SentenceTransformer
import numpy as np
import json
import os
from conversation_memory import (
    save_message,
    get_recent_context
)

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

VECTOR_DB_FILE = "data/vector_db.json"


def create_vector_db():

    vectors = []

    embeddings = model.encode(
        knowledge_base
    )

    for text, embedding in zip(
        knowledge_base,
        embeddings
    ):

        vectors.append({
            "text": text,
            "embedding": embedding.tolist()
        })

    with open(
        VECTOR_DB_FILE,
        "w"
    ) as f:

        json.dump(vectors, f)

    print(
        "Vector database created."
    )


def load_vector_db():

    if not os.path.exists(
        VECTOR_DB_FILE
    ):

        create_vector_db()

    with open(
        VECTOR_DB_FILE,
        "r"
    ) as f:

        return json.load(f)


def cosine_similarity(a, b):

    a = np.array(a)
    b = np.array(b)

    return np.dot(a, b) / (
        np.linalg.norm(a) *
        np.linalg.norm(b)
    )

def semantic_search(query):

    db = load_vector_db()

    contextual_query = build_contextual_query(
    query
    )

    query_embedding = model.encode(
    [contextual_query]
    )[0]

    scores = []

    for item in db:

        similarity = cosine_similarity(
            query_embedding,
            item["embedding"]
        )

        scores.append({
            "source": item["source"],
            "text": item["text"],
            "score": similarity
        })

    ranked = sorted(
        scores,
        key=lambda x: x["score"],
        reverse=True
    )

    return ranked[:3]

def build_contextual_query(query):

    history = get_recent_context()

    if not history:
        return query

    return f"""
        Conversation History:
        {history}

        Current Query:
        {query}
        """

if __name__ == "__main__":

    while True:

        query = input(
            "\nAsk something: "
        )

        if query.lower() == "exit":
            break
        save_message("user", query)
        results = semantic_search(
            query
        )

        print("\nTop Matches:\n")

        for item in results:

            if item["score"] > 0.2:
                print(f"Score: {item['score']:.4f}")
                print(f"Source: {item['source']}")
                print(item["text"])
                print("-" * 40)
                save_message(
                "assistant",
                results[0]["text"]
            )