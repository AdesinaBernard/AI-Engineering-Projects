import requests

LLM_URL = "http://localhost:8080/completion"


def load_knowledge_base():

    with open("knowledge_base.txt", "r") as f:
        return f.read()


def chunk_text(text, chunk_size=2):

    lines = [
        line.strip()
        for line in text.split("\n")
        if line.strip()
    ]

    chunks = []

    for i in range(0, len(lines), chunk_size):

        chunk = "\n".join(
            lines[i:i + chunk_size]
        )

        chunks.append(chunk)

    return chunks

def score_chunk(query, chunk):

    query_words = query.lower().split()

    chunk_lower = chunk.lower()

    score = 0

    for word in query_words:

        if word in chunk_lower:
            score += 1

    return score

def retrieve_context(query, knowledge_text):

    chunks = chunk_text(knowledge_text)

    scored_chunks = []

    for chunk in chunks:

        score = score_chunk(query, chunk)

        scored_chunks.append(
            (score, chunk)
        )

    ranked = sorted(
        scored_chunks,
        key=lambda x: x[0],
        reverse=True
    )

    best_chunks = [
        chunk
        for score, chunk in ranked
        if score > 0
    ]

    return "\n\n".join(best_chunks[:2])


def ask_rag(query):

    knowledge = load_knowledge_base()

    context = retrieve_context(
        query,
        knowledge
    )

    prompt = f"""
You are a helpful AI assistant.

Answer the question using ONLY the context below.

If the answer is not in the context, say:
"I could not find that information in the knowledge base."

CONTEXT:
{context}

QUESTION:
{query}

ANSWER:
"""

    payload = {
        "prompt": prompt,
        "n_predict": 120,
        "temperature": 0.2
    }

    try:

        response = requests.post(
            LLM_URL,
            json=payload,
            timeout=60
        )

        response.raise_for_status()

        data = response.json()

        return data.get("content", "").strip()

    except Exception as e:
        return f"RAG Error: {e}"