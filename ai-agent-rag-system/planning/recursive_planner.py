MAX_DEPTH = 2


def create_subtasks(task, result, depth):
    if depth >= MAX_DEPTH:
        return []

    new_tasks = []

    if task["tool"] == "analyze_repos":
        if result and isinstance(result, list):
            language = result[0].get("language", "")

            if language:
                new_tasks.append({
                    "tool": "rag",
                    "input": f"What is {language} used for?",
                    "depth": depth + 1
                })

    elif task["tool"] == "rag":
        text = str(result).lower()

        if "python" in text:
            new_tasks.append({
                "tool": "rag",
                "input": "What AI frameworks use Python?",
                "depth": depth + 1
            })

    return new_tasks