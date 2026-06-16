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

        content = data.get("content", "").strip()

        if not content:
            return {
                "passed": False,
                "feedback": "Critic returned empty response"
            }
        start = content.find("{")
        end = content.rfind("}") + 1

        if start == -1 or end == 0:
            return {
                "passed": False,
                "feedback": f"Critic returned non-JSON output: {content}"
        }

        parsed = json.loads(content[start:end])

        return parsed

    except Exception:
        return basic_critique(query, execution_results)
    
def basic_critique(query, execution_results):
    if not execution_results:
        return {
            "passed": False,
            "feedback": "No execution results were produced."
        }

    failed_steps = [
        item for item in execution_results
        if item.get("status") == "failed"
    ]

    if failed_steps:
        return {
            "passed": False,
            "feedback": f"{len(failed_steps)} step(s) failed."
        }

    return {
        "passed": True,
        "feedback": "All execution steps completed successfully."
    }