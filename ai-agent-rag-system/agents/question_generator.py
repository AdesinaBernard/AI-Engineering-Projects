def generate_followup_questions(goal, evidence):

    if len(evidence) == 0:

        return [
            f"What is {goal}?",
            f"Why is {goal} important?"
        ]

    if len(evidence) == 1:

        return [
            f"What are the practical applications of {goal}?"
        ]

    if len(evidence) == 2:

        return [
            f"What are the limitations of {goal}?"
        ]

    return []