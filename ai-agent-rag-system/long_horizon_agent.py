from task_manager import TaskManager
from goal_decomposer import decompose_goal
from agent_executor import execute_task
from critic_agent import review
from dynamic_planner import (
    generate_followup_tasks
)
from recursive_planner import (
    create_subtasks
)

def run_goal(goal):

    manager = TaskManager()

    tasks = decompose_goal(goal)

    for task in tasks:

        if "depth" not in task:
            task["depth"] = 0

        manager.add_task(task)

    results = []

    while manager.has_tasks():

        task = manager.next_task()

        print(
            f"\nExecuting: "
            f"{task['tool']}"
        )

        output = execute_task(task)

        new_tasks = create_subtasks(
            task,
            output["result"],
            task["depth"]
        )

        if new_tasks:

            print(
                f"Generated "
                f"{len(new_tasks)} "
                f"recursive task(s)"
        )

        manager.add_tasks(
            new_tasks
        )

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