def generate_followup_tasks(task, result):

    new_tasks = []

    if task["tool"] == "analyze_repos":

        if result and isinstance(result, list):

            repo = result[0]

            language = repo.get(
                "language",
                ""
            )

            if language:

                new_tasks.append({
                    "tool": "rag",
                    "input":
                    f"What is {language} used for?"
                })

    return new_tasks