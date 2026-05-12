import requests

LLM_URL = "http://localhost:8080/completion"


def create_plan(user_goal):

    prompt = f"""
You are an autonomous AI planning system.

Your job:
Break complex goals into ordered actionable steps.

Available tools:
1. analyze_repos
   - analyzes GitHub repositories

2. summarizer
   - summarizes text

Rules:
- Keep steps short
- One step per line
- Mention which tool should be used
- Return only the plan

User Goal:
{user_goal}

Execution Plan:
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

        output = data.get("content", "").strip()

        return output

    except Exception as e:
        return f"Planner error: {e}"