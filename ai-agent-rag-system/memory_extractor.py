from long_term_memory import store_fact


IMPORTANT_PATTERNS = [
    "I like",
    "I prefer",
    "I completed",
    "I finished",
    "My goal"
]


def extract_memory(text):
    for pattern in IMPORTANT_PATTERNS:
        if pattern.lower() in text.lower():
            store_fact(text)
            return True

    return False