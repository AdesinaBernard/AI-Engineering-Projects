from tool_selector import select_tool


def normalize_tool_input(tool, task_description):
    task_lower = task_description.lower()

    if tool == "analyze_repos":
        if "numpy" in task_lower:
            return ["numpy/numpy"]

        if "python" in task_lower or "cpython" in task_lower:
            return ["python/cpython"]

        return []

    return task_description


def decompose_goal(goal):
    goal_lower = goal.lower()

    tasks = []

    if "numpy" in goal_lower:
        subtasks = [
            "Explain NumPy",
            "Analyze the NumPy repository",
            "Summarize NumPy and why it matters"
        ]

        for task in subtasks:
            tool = select_tool(task)

            tasks.append({
                "tool": tool,
                "input": normalize_tool_input(tool, task)
            })

    return tasks