import requests
import json

LLM_URL = "http://localhost:8080/completion"


def route_request(user_input):

    user_lower = user_input.lower()

    # 🔹 FAST RULE-BASED ROUTING
    repo_keywords = [
        "repo",
        "github",
        "library",
        "libraries",
        "project",
        "projects"
    ]

    summary_keywords = [
        "summarize",
        "summary",
        "explain briefly"
    ]

    if any(word in user_lower for word in repo_keywords):
        return "analyze_repos"

    if any(word in user_lower for word in summary_keywords):
        return "summarizer"

    # 🔹 FALLBACK TO LLM
    prompt = f"""
You are a routing classifier.

Choose ONE tool:

- analyze_repos
- summarizer
- unknown

Return ONLY JSON.

Examples:

User: Analyze GitHub repositories
{{"tool":"analyze_repos"}}

User: Find Python libraries
{{"tool":"analyze_repos"}}

User: Summarize this article
{{"tool":"summarizer"}}

User:
{user_input}

Output:
"""

    payload = {
        "prompt": prompt,
        "n_predict": 30,
        "temperature": 0.1,
        "stop": ["\n\n"]
    }

    try:
        response = requests.post(
            LLM_URL,
            json=payload,
            timeout=30
        )

        data = response.json()

        content = data.get("content", "").strip()

        start = content.find("{")
        end = content.rfind("}") + 1

        cleaned = content[start:end]

        parsed = json.loads(cleaned)

        return parsed.get("tool", "unknown")

    except Exception:
        return "unknown"