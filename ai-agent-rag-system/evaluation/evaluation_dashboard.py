import json
import os

FILE = "evaluations.json"

if not os.path.exists(FILE):

    print("No evaluations found.")
    exit()

with open(FILE, "r") as f:

    history = json.load(f)

print("\nAgent Evaluation History\n")

for index, run in enumerate(history, 1):

    print(
        f"Run {index}"
    )

    print(
        f"Score: {run['score']}"
    )

    print(
        f"Tasks: {run['tasks']}"
    )

    print(
        f"Retries: {run['retries']}"
    )

    print("-" * 30)