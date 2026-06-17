import datetime


def log_event(event):
    timestamp = datetime.datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    with open("agent.log", "a") as f:
        f.write(
            f"[{timestamp}] {event}\n"
        )