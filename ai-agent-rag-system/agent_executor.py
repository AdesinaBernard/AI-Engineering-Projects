from tools import TOOLS
from reflection import evaluate_result
from prompt_optimizer import improve_tool_input
from failure_memory import save_failure
from execution_logger import log_event


def execute_task(task, max_retries=2):
    task_type = task["tool"]
    task_input = task["input"]

    log_event(f"Executing {task_type}")

    if task_type not in TOOLS:
        log_event(f"{task_type} failed: unknown tool")

        return {
            "tool": task_type,
            "input": task_input,
            "result": f"Unknown tool: {task_type}",
            "retries": 0,
            "status": "failed",
            "reason": "Unknown tool"
        }

    tool_function = TOOLS[task_type]

    retries = 0
    current_input = task_input
    last_result = None
    last_reason = ""

    while retries <= max_retries:
        result = tool_function(current_input)
        last_result = result

        passed, reason = evaluate_result(
            task_type,
            current_input,
            result,
            use_llm_judge=False
        )

        if passed:
            log_event(f"{task_type} success")

            return {
                "tool": task_type,
                "input": current_input,
                "result": result,
                "retries": retries,
                "status": "success",
                "reason": reason
            }

        print(f"Reflection failed: {reason}")
        print(f"Retrying {task_type} ({retries + 1})...")

        log_event(f"{task_type} failed: {reason}")

        save_failure(
            task_type,
            current_input,
            result,
            reason
        )

        current_input = improve_tool_input(
            task_type,
            current_input,
            reason
        )

        last_reason = reason
        retries += 1

    return {
        "tool": task_type,
        "input": current_input,
        "result": last_result,
        "retries": retries,
        "status": "failed",
        "reason": last_reason
    }


def execute_plan(plan):
    results = []

    for step in plan:
        print(f"\nExecuting: {step['tool']}")

        output = execute_task(step)
        results.append(output)

    return results