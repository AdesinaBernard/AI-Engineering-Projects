import requests

LLM_URL = "http://localhost:8080/completion"


def load_knowledge_base():

    with open("knowledge_base.txt", "r") as f:
        return f.read()


def retrieve_context(query, knowledge_text):

    query_words = query.lower().split()

    lines = knowledge_text.split("\n")

    matches = []

    for line in lines:

        line_lower = line.lower()

        for word in query_words:

            if word in line_lower:
                matches.append(line)
                break

    return "\n".join(matches[:3])


def ask_rag(query):

    knowledge = load_knowledge_base()

    context = retrieve_context(
        query,
        knowledge
    )

    prompt = f"""
Answer the question using ONLY the context below.

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