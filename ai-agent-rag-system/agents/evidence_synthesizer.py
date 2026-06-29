import requests

LLM_URL = "http://localhost:8080/completion"


def synthesize_evidence(question, raw_context):
    prompt = f"""
You are an evidence synthesis agent.

Question:
{question}

Retrieved Context:
{raw_context}

Write a concise answer using only the retrieved context.

Rules:
- 2 to 4 sentences maximum
- Do not add information outside the context
- If the context does not answer the question, say:
  "I could not find that information in the knowledge base."

Answer:
"""

    payload = {
        "prompt": prompt,
        "n_predict": 120,
        "temperature": 0.1
    }

    try:
        response = requests.post(
            LLM_URL,
            json=payload,
            timeout=60
        )

        response.raise_for_status()

        data = response.json()

        return data.get(
            "content",
            ""
        ).strip()

    except Exception as e:
        return f"Synthesis error: {e}"