def evaluate_execution(results):

    report = {
        "tasks": len(results),
        "successes": 0,
        "failures": 0,
        "retries": 0,
        "score": 0,
        "tools": {}
    }

    for result in results:

        tool = result["tool"]

        if tool not in report["tools"]:
            report["tools"][tool] = {
                "success": 0,
                "failed": 0
            }

        if result["status"] == "success":
            report["successes"] += 1
            report["tools"][tool]["success"] += 1
        else:
            report["failures"] += 1
            report["tools"][tool]["failed"] += 1

        report["retries"] += result.get("retries", 0)

    base_score = (report["successes"] / report["tasks"]) * 100

    score = base_score
    score -= report["failures"] * 15
    score -= report["retries"] * 5

    report["score"] = round(max(score, 0), 1)

    return report