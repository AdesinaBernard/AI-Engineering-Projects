import json
import os

FILE = "data/evaluations.json"


def save_evaluation(report):

    history = []

    if os.path.exists(FILE):

        with open(FILE, "r") as f:
            history = json.load(f)

    history.append(report)

    with open(FILE, "w") as f:
        json.dump(
            history,
            f,
            indent=2
        )