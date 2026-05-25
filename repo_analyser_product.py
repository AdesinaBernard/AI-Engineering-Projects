import sys
import requests
import json

LLM_URL = "http://localhost:8080/completion"


def ask_llm(prompt):
    payload = {
        "prompt": prompt,
        "n_predict": 120,
        "temperature": 0.1,
        "top_k": 40,
        "top_p": 0.9,
        "repeat_penalty": 1.2,
        "stop": ["\n\n"]
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
        return json.dumps({
            "summary": "LLM request failed",
            "strength": str(e),
            "use_case": "Troubleshooting required"
        })


def build_repo_prompt(repo):
    return f"""
You are a strict API JSON generator.

TASK:
Analyze the repository and return ONLY valid JSON.

RULES:
- Output ONLY ONE JSON object
- No markdown
- No explanations
- No extra text
- No code blocks
- No comments

REQUIRED FORMAT:

{{
  "summary": "short summary",
  "strength": "main strength",
  "use_case": "primary use case"
}}

REPOSITORY DATA:
Name: {repo['name']}
Stars: {repo['stars']}
Forks: {repo['forks']}
Language: {repo['language']}

JSON:
"""


def fetch_repo_data(repo):
    url = f"https://api.github.com/repos/{repo}"

    try:
        response = requests.get(url, timeout=10)

        response.raise_for_status()

        data = response.json()

        return {
            "name": data.get("full_name"),
            "stars": data.get("stargazers_count", 0),
            "forks": data.get("forks_count", 0),
            "issues": data.get("open_issues_count", 0),
            "language": data.get("language") or "Unknown"
        }

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {repo}: {e}")
        return None


def analyze_repos(repo_names):

    results = []

    for repo in repo_names:

        repo_data = fetch_repo_data(repo)

        if repo_data:

            repo_data["engagement_score"] = (
                repo_data["stars"] +
                repo_data["forks"] * 2
            )

            results.append(repo_data)

    if not results:
        return []

    ranked = sorted(
        results,
        key=lambda x: x["engagement_score"],
        reverse=True
    )

    output = []

    for repo in ranked[:3]:

        prompt = build_repo_prompt(repo)

        insight = ask_llm(prompt)

        insight = (
            insight
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        try:
            parsed = json.loads(insight)

        except json.JSONDecodeError:

            parsed = {
                "summary": "Invalid JSON output",
                "strength": insight,
                "use_case": "Prompt tuning needed"
            }

        output.append({
            "repo": repo["name"],
            "stars": repo["stars"],
            "forks": repo["forks"],
            "language": repo["language"],
            "engagement_score": repo["engagement_score"],
            "ai_insight": parsed
        })

    return output


def main():

    repo_names = sys.argv[1:]

    if not repo_names:

        print("Usage:")
        print(
            "python repo_analyser_product.py "
            "python/cpython numpy/numpy"
        )

        sys.exit(1)

    results = analyze_repos(repo_names)

    print(json.dumps(results, indent=4))


if __name__ == "__main__":
    main()