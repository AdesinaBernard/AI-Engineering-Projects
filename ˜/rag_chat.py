from sentence_transformers import SentenceTransformer
from conversation_memory import (
    save_message,
    get_recent_context
)

import requests
import numpy as np
import json

LLM_URL = "http://localhost:8080/completion"

VECTOR_DB_FILE = "vector_db.json"

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

CONFIDENCE_THRESHOLD = 0.30

def load_vector_db():

    with open(VECTOR_DB_FILE, "r") as f:
        return json.load(f)


def cosine_similarity(a, b):

    a = np.array(a)
    b = np.array(b)

    return np.dot(a, b) / (
        np.linalg.norm(a) *
        np.linalg.norm(b)
    )


def retrieve_context(query, top_k=3):

    db = load_vector_db()

    query_embedding = model.encode(
        [query]
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

    return ranked[:top_k]

def build_prompt(query, retrieved_chunks):

    history = get_recent_context()

    context_text = "\n\n".join([
    f"[Source: {chunk['source']}]\n{chunk['text']}"
    for chunk in retrieved_chunks
    ])

    return f"""
    You are a helpful AI assistant.

    Use ONLY the retrieved context below to answer.
    Cite the source filename when answering.

    If the answer is not present, say:
    "I could not find that information."

    Conversation History:
    {history}

    Retrieved Context:
    {context_text}

    User Question:
    {query}

    Answer with citations:
    """

def ask_llm(prompt):
    payload = {
        "prompt": prompt,
        "n_predict": 150,
        "temperature": 0.2,
        "stream": True
    }

    try:
        response = requests.post(
            LLM_URL,
            json=payload,
            timeout=60,
            stream=True
        )

        response.raise_for_status()

        full_response = ""

        for line in response.iter_lines():
            if line:
                decoded = line.decode("utf-8")

                if decoded.startswith("data: "):
                    decoded = decoded.replace("data: ", "")

                if decoded.strip() == "[DONE]":
                    break

                try:
                    data = json.loads(decoded)
                    token = data.get("content", "")
                    print(token, end="", flush=True)
                    full_response += token
                except json.JSONDecodeError:
                    pass

        print()
        return full_response.strip()

    except Exception as e:
        return f"RAG chat error: {e}"

if __name__ == "__main__":

    print("=== Conversational RAG Assistant ===")

    while True:

        query = input("\nYou: ")

        if query.lower() == "exit":
            break

        save_message("user", query)

        retrieved = retrieve_context(query)

        top_score = retrieved[0]["score"] if retrieved else 0

        if top_score < CONFIDENCE_THRESHOLD:
            print("\nAssistant:\n")
            print("I could not find enough relevant information in the knowledge base.")
            continue

        prompt = build_prompt(query, retrieved)

        print("\nAssistant:\n")

        answer = ask_llm(prompt)

        print("\nSources:")

        for i, item in enumerate(retrieved, 1):
            print(
                f"{i}. {item['source']} "
                f"(confidence={item['score']:.4f})"
            )

        save_message("assistant", answer)