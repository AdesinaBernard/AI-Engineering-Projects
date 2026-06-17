REQUIRED_FILES = [
    "agent.py",
    "coordinator.py",
    "advanced_planner.py",
    "agent_executor.py",
    "tool_selector.py",
    "goal_decomposer.py",
    "long_horizon_agent.py",
    "reflection.py",
    "critic.py",
    "failure_memory.py",
    "repo_analyser_product.py",
    "rag_chat.py"
]


def run_health_check():

    import os

    missing = []

    for file in REQUIRED_FILES:

        if not os.path.exists(file):
            missing.append(file)

    if missing:

        print("\nMissing Files:")

        for item in missing:
            print(item)

    else:

        print(
            "\nAll required files found."
        )


if __name__ == "__main__":
    run_health_check()