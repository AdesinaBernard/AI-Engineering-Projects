from repo_analyser_product import analyze_repos
from router import route_request
from memory import (
    save_repos,
    get_last_repos,
    save_message,
    get_history
)


def main():

    print("=== AI Agent Started ===")

    while True:

        query = input(
            "\nWhat do you want to do? "
        )

        if query.lower() == "exit":
            print("Goodbye.")
            break

        save_message("user", query)

        # 🔹 MEMORY FOLLOW-UP
        if "language" in query.lower():

            last_repos = get_last_repos()

            if not last_repos:
                print("No repositories in memory.")

            else:
                results = analyze_repos(last_repos)

                for repo in results:
                    print(
                        f"{repo['repo']} uses "
                        f"{repo['language']}"
                    )

            continue

        # 🔹 ROUTING
        action = route_request(query)

        print(f"Agent decided to: {action}")

        if action == "analyze_repos":

            repos_input = input(
                "Enter repos (comma separated): "
            )

            repos = [
                repo.strip()
                for repo in repos_input.split(",")
                if repo.strip()
            ]

            save_repos(repos)

            print("Running repository analysis...")

            results = analyze_repos(repos)

            print("\n=== Agent Results ===\n")

            for repo in results:

                print(f"Repo: {repo['repo']}")
                print(f"Stars: {repo['stars']}")
                print(f"Forks: {repo['forks']}")
                print(f"Language: {repo['language']}")

                print("AI Insight:")
                print(repo["ai_insight"])

                print("-" * 50)

        else:
            print("Unknown request.")

if __name__ == "__main__":
    main()