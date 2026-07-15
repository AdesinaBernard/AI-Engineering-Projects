failure_log = []


def save_failure(tool, tool_input, result, reason):
    failure_log.append({
        "tool": tool,
        "input": tool_input,
        "result": result,
        "reason": reason
    })


def get_failures():
    return failure_log