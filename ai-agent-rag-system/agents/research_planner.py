import json
import requests

LLM_URL = "http://localhost:8080/completion"


def generate_research_questions(goal, evidence):
    evidence_text = json.dumps(evidence, indent=2)

    prompt = f"""
You are a research planning agent.

Goal:
{goal}

Evidence collected so far:
{evidence_text}

Generate the next 1-2 best research questions.

Rules:
- Return ONLY valid JSON
- Use this format:
{{
  "questions": [
    "question one",
    "question two"
  ]
}}
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
        content = data.get("content", "").strip()

        start = content.find("{")
        end = content.rfind("}") + 1

        parsed = json.loads(content[start:end])

        return parsed.get("questions", [])

    except Exception:
        if not evidence:
            return [
                f"What is {goal}?",
                f"Why is {goal} important?"
            ]

        return [
            f"What are the practical applications of {goal}?"
        ]