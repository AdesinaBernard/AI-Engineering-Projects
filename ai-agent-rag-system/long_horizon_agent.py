from task_manager import TaskManager
from goal_decomposer import decompose_goal
from agent_executor import execute_task
from critic_agent import review


def run_goal(goal):

    manager = TaskManager()

    tasks = decompose_goal(goal)

    for task in tasks:
        manager.add_task(task)

    results = []

    while manager.has_tasks():

        task = manager.next_task()

        print(
            f"\nExecuting: "
            f"{task['tool']}"
        )

        output = execute_task(task)

        manager.complete_task(task)

        results.append(output)

    critique = review(
        goal,
        results
    )

    return {
        "goal": goal,
        "completed_tasks":
            manager.completed,
        "results": results,
        "critique": critique
    }