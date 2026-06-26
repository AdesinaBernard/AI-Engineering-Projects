conversation_memory = {
    "last_repos": [],
    "history": []
}


def save_repos(repos):
    conversation_memory["last_repos"] = repos


def get_last_repos():
    return conversation_memory["last_repos"]


def save_message(role, content):

    conversation_memory["history"].append({
        "role": role,
        "content": content
    })


def get_history():
    return conversation_memory["history"]