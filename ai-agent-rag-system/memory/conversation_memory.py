conversation_history = []


def save_message(role, content):

    conversation_history.append({
        "role": role,
        "content": content
    })


def get_history():

    return conversation_history


def get_recent_context(limit=4):

    recent = conversation_history[-limit:]

    combined = []

    for item in recent:

        combined.append(
            f"{item['role']}: {item['content']}"
        )

    return "\n".join(combined)