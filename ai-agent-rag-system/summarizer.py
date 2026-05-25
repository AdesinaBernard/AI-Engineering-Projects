import requests

LLM_URL = "http://localhost:8080/completion"


def summarize_text(text):

    prompt = f"""
Summarize this text in EXACTLY 3 short bullet points.

Rules:
- Each bullet must start with "-"
- No extra explanations

TEXT:
{text}

SUMMARY:
"""

    payload = {
        "prompt": prompt,
        "n_predict": 80,
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

        output = data.get("content", "").strip()

        if not output:
            return "No summary generated."

        return output

    except Exception as e:
        return f"Summarizer error: {e}"