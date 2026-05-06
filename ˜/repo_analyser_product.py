
import sys
import requests
import os
import datetime
import json

print("RUNNING UPDATED SCRIPT")

# 🔹 LLM CONFIG
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
        response = requests.post(LLM_URL, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()

        raw_output = data.get("content", "").strip()

        return clean_output(raw_output)

    except Exception as e:
        return f"LLM Error: {e}"


def clean_output(text):
    text = text.strip()

    # Remove markdown artifacts
    text = text.replace("**", "")

    # Extract bullet points only
    lines = text.split("\n")
    bullets = [line for line in lines if line.strip().startswith("-")]

    # Limit to 3 lines
    bullets = bullets[:3]

    return "\n".join(bullets) if bullets else text


def build_repo_prompt(repo):
    return f"""
You are a strict JSON generator.

Rules:
- Output MUST be valid JSON
- Do NOT include explanations
- Do NOT include text outside JSON
- Keys must be: summary, strength, use_case

Example:
{{
  "summary": "A Python library for data analysis",
  "strength": "Widely adopted with strong community",
  "use_case": "Used in data science and analytics"
}}

Now analyze this repository:

Name: {repo['name']}
Stars: {repo['stars']}
Forks: {repo['forks']}
Language: {repo['language']}

Output:
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
            "language": data.get("language")
        }

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {repo}: {e}")
        return None


def main():
    repo_names = sys.argv[1:]

    if not repo_names:
        print("Usage: python repo_analyser_product.py <repo1> <repo2> ...")
        sys.exit(1)

    results = []

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(os.path.dirname(__file__), f"report_{timestamp}.txt")

    with open(report_path, "w") as f:

        # 🔹 Fetch repos
        for repo in repo_names:
            repo_data = fetch_repo_data(repo)

            if repo_data:
                results.append(repo_data)
                print(f"Fetched: {repo_data['name']} ({repo_data['stars']} stars)")
                f.write(f"Fetched: {repo_data['name']} ({repo_data['stars']} stars)\n")

        if not results:
            print("No valid repos were fetched.")
            return

        # 🔹 Compute engagement
        for repo in results:
            repo["engagement_score"] = repo["stars"] + repo["forks"] * 2

        ranked = sorted(results, key=lambda x: x["engagement_score"], reverse=True)

        print("\nTop repos by engagement:")
        f.write("\nTop repos by engagement:\n")

        for repo in ranked:
            line = f"- {repo['name']}: {repo['engagement_score']}"
            print(line)
            f.write(line + "\n")

        # 🔹 Top repos
        top_results = ranked[:3]

        print("\n=== Top Repositories ===")
        f.write("\n=== Top Repositories ===\n")

        for i, repo in enumerate(top_results, 1):

            output_line = (
                f"{i}. {repo['name']}\n"
                f"   Stars: {repo['stars']}\n"
                f"   Forks: {repo['forks']}\n"
                f"   Score: {repo['engagement_score']}\n"
            )

            print(output_line)
            f.write(output_line + "\n")

            # 🔥 LLM INTEGRATION (THIS WAS MISSING BEFORE)
            print("Generating AI insight...")

            prompt = build_repo_prompt(repo)
            insight = ask_llm(prompt)
            insight = insight.strip().replace("```json", "").replace("```", "")

            try:
                parsed = json.loads(insight)

                print("AI Insight (Structured):")
                print(parsed)

                f.write("AI Insight (JSON):\n")
                f.write(json.dumps(parsed, indent=2) + "\n")

            except json.JSONDecodeError:
                print("⚠️ Failed to parse JSON. Raw output:")
                print(insight)

                f.write("Invalid JSON Output:\n")
                f.write(insight + "\n")

    print(f"\nReport saved to: {report_path}")


if __name__ == "__main__":
    main()