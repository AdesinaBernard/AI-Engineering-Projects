import requests
import json

LLM_URL = "http://localhost:8080/completion"


def basic_evaluator(result):
    if result is None:
        return False, "Result is None"

    result_text = str(result).strip()

    if len(result_text) < 20:
        return False, "Result too short"

    failure_phrases = [
        "unknown request",
        "i could not find",
        "error",
        "invalid",
        "none",
        "no repository results"
    ]

    lower = result_text.lower()

    for phrase in failure_phrases:
        if phrase in lower:
            return False, f"Detected failure phrase: {phrase}"

    return True, "Basic evaluation passed"


def evaluate_repo_result(result):
    if not result:
        return False, "No repository results returned"

    if not isinstance(result, list):
        return False, "Repo result is not a list"

    for item in result:
        if "repo" not in item or "stars" not in item:
            return False, "Missing expected repo fields"

    return True, "Repo result passed"


def evaluate_summary_result(result):
    text = str(result).strip()

    if len(text) < 30:
        return False, "Summary too short"

    return True, "Summary passed"


def evaluate_rag_result(result):
    text = str(result).lower()

    if "could not find" in text:
        return False, "RAG could not find context"

    return True, "RAG passed"


def llm_as_judge(tool, tool_input, result):
    prompt = f"""
You are an evaluator for an AI agent.

Tool: {tool}
Input: {tool_input}
Output: {result}

Decide if the output successfully answers the input.

Return ONLY valid JSON:
{{
  "passed": true,
  "reason": "short reason"
}}
"""

    payload = {
        "prompt": prompt,
        "n_predict": 80,
        "temperature": 0.1
    }

    try:
        response = requests.post(LLM_URL, json=payload, timeout=60)
        response.raise_for_status()

        data = response.json()
        content = data.get("content", "").strip()

        start = content.find("{")
        end = content.rfind("}") + 1
        parsed = json.loads(content[start:end])

        return parsed.get("passed", False), parsed.get("reason", "No reason")

    except Exception as e:
        return False, f"Judge error: {e}"


def evaluate_result(tool, tool_input, result, use_llm_judge=False):
    if tool == "analyze_repos":
        passed, reason = evaluate_repo_result(result)

    elif tool == "summarizer":
        passed, reason = evaluate_summary_result(result)

    elif tool == "rag":
        passed, reason = evaluate_rag_result(result)

    else:
        passed, reason = basic_evaluator(result)

    if not passed:
        return False, reason

    if use_llm_judge:
        return llm_as_judge(tool, tool_input, result)

    return True, reason