from pydantic import config
from sentence_transformers import SentenceTransformer
import numpy as np

# Load embedding model
model = SentenceTransformer(
    config.EMBEDDING_MODEL
)

knowledge_base = [

    "Python is a programming language used for AI and web development.",

    "NumPy is used for numerical computing and arrays.",

    "Pandas is used for data analysis and DataFrames.",

    "The Premier League is the top football division in England.",

    "RAG combines retrieval systems with language models."
]

# Generate embeddings
knowledge_embeddings = model.encode(
    knowledge_base
)


def cosine_similarity(a, b):

    return np.dot(a, b) / (
        np.linalg.norm(a) *
        np.linalg.norm(b)
    )


def semantic_search(query):

    query_embedding = model.encode([query])[0]

    scores = []

    for i, embedding in enumerate(
        knowledge_embeddings
    ):

        similarity = cosine_similarity(
            query_embedding,
            embedding
        )

        scores.append(
            (similarity, knowledge_base[i])
        )

    ranked = sorted(
        scores,
        key=lambda x: x[0],
        reverse=True
    )

    return ranked[:3]


if __name__ == "__main__":

    while True:

        query = input(
            "\nAsk something: "
        )

        if query.lower() == "exit":
            break

        results = semantic_search(query)

        print("\nTop Matches:\n")

        for score, text in results:

            print(
                f"Score: {score:.4f}"
            )

            print(text)
            print("-" * 40)