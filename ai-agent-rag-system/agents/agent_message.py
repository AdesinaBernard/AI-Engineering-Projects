def create_message(sender, receiver, content):
    return {
        "sender": sender,
        "receiver": receiver,
        "content": content
    }


def print_message(message):
    print(
        f"\n[{message['sender']} → {message['receiver']}]"
    )
    print(message["content"])