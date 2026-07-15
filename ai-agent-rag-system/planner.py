import requests

LLM_URL = "http://localhost:8080/completion"


VALID_TOOLS = [
    "analyze_repos",
    "summarizer",
    "rag"
]


def validate_plan(plan):

    valid_lines = []

    lines = plan.split("\n")

    for line in lines:

        line = line.strip()

        if not line:
            continue

        line_lower = line.lower()

        for tool in VALID_TOOLS:

            if line_lower.startswith(tool + " "):

                valid_lines.append(line)

                break

    return "\n".join(valid_lines)


def create_plan(query):

    prompt = f"""
You are an AI planning system.

Available tools:

1. analyze_repos
- Use ONLY for GitHub repository analysis
- Requires repo names like python/cpython

2. summarizer
- Use ONLY for summarizing long text or articles

3. rag
- Use for knowledge questions
- Examples:
  - What is NumPy?
  - What is Pandas?
  - What is AI?

Rules:
- Output one action per line
- ALWAYS include the original user request after the tool name
- Never output only the tool name
- Do NOT use markdown
- Do NOT use code blocks
- Do NOT explain

Correct examples:

rag What is Pandas?
rag What is AI?
analyze_repos python/cpython
summarizer Artificial intelligence is changing software engineering

User request:
{query}
"""

    payload = {
        "prompt": prompt,
        "n_predict": 80,
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

        raw_output = data.get("content", "").strip()

        print("\nRAW PLANNER OUTPUT:")
        print(raw_output)

        validated = validate_plan(raw_output)

        return validated

    except Exception as e:

        print(f"Planner error: {e}")

        return ""