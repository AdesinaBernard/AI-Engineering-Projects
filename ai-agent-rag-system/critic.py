import requests
import json

LLM_URL = "http://localhost:8080/completion"

def critique_result(query, execution_results):

    if not execution_results:
        return {
            "passed": False,
            "feedback": "No execution results."
        }

    result_text = str(execution_results)

    if len(result_text) < 50:
        return {
            "passed": False,
            "feedback": "Result appears incomplete."
        }

    return {
        "passed": True,
        "feedback": "Result appears sufficient."
    }

def llm_critique(query, execution_results):

    prompt = f"""
You are an AI critic.

User Goal:
{query}

Execution Results:
{execution_results}

Did the agent successfully complete the user's goal?

Return ONLY JSON:

{{
  "passed": true,
  "feedback": "short explanation"
}}
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

        data = response.json()

        content = data.get(
            "content",
            ""
        )

        start = content.find("{")
        end = content.rfind("}") + 1

        parsed = json.loads(
            content[start:end]
        )

        return parsed

    except Exception as e:

        return {
            "passed": False,
            "feedback": str(e)
        }