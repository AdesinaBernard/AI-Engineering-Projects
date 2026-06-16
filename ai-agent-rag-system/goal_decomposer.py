def decompose_goal(goal):

    goal_lower = goal.lower()

    tasks = []

    if "numpy" in goal_lower:

        tasks.append({
            "tool": "analyze_repos",
            "input": ["numpy/numpy"]
        })

        tasks.append({
            "tool": "rag",
            "input": "What is NumPy?"
        })

        tasks.append({
            "tool": "summarizer",
            "input": (
                "Summarize NumPy "
                "and explain why it matters."
            )
        })

    return tasks