FAILURE_PHRASES = [
    "i could not find",
    "not found",
    "no information",
    "not enough relevant information"
]


def is_valid_evidence(item):
    answer = item.get("answer", "").lower().strip()

    if not answer:
        return False

    for phrase in FAILURE_PHRASES:
        if phrase in answer:
            return False

    return True


def evaluate_evidence(state):
    valid_evidence = [
        item for item in state.evidence
        if is_valid_evidence(item)
    ]

    invalid_evidence = len(state.evidence) - len(valid_evidence)

    if len(valid_evidence) >= 3:
        return {
            "complete": True,
            "confidence": 85,
            "reason": "Enough valid evidence collected.",
            "valid_evidence": len(valid_evidence),
            "invalid_evidence": invalid_evidence
        }

    confidence = 30 + (len(valid_evidence) * 20)

    return {
        "complete": False,
        "confidence": min(confidence, 75),
        "reason": "More valid evidence needed.",
        "valid_evidence": len(valid_evidence),
        "invalid_evidence": invalid_evidence
    }