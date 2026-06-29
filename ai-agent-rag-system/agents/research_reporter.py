def generate_research_report(result):
    goal = result["goal"]
    evidence = result["evidence"]
    confidence = result.get("confidence", 0)

    report = []

    report.append("=" * 50)
    report.append("AUTONOMOUS RESEARCH REPORT")
    report.append("=" * 50)

    report.append("\nGoal")
    report.append("-" * 20)
    report.append(goal)

    report.append("\nSummary")
    report.append("-" * 20)

    valid_evidence = [
        item for item in evidence
        if "could not find" not in item["answer"].lower()
    ]

    if valid_evidence:
        report.append(valid_evidence[0]["answer"])
    else:
        report.append("No valid evidence was found in the knowledge base.")

    report.append("\nEvidence Collected")
    report.append("-" * 20)

    for index, item in enumerate(evidence, 1):
        report.append(f"{index}. Question: {item['question']}")
        report.append(f"   Answer: {item['answer']}")

    report.append("\nConfidence")
    report.append("-" * 20)
    report.append(f"{confidence}%")

    report.append("\nRecommendation")
    report.append("-" * 20)

    if confidence >= 80 and valid_evidence:
        report.append("Enough valid evidence collected. Research complete.")
    else:
        report.append("More valid evidence is needed before this research can be considered complete.")

    return "\n".join(report)