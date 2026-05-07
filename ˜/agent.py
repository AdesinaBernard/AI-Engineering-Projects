from repo_analyser_product import analyze_repos


def agent(user_input):
    user_input = user_input.lower()

    if "repo" in user_input or "github" in user_input:
        return "analyze_repos"

    return "unknown"


def main():
    print("=== AI Agent Started ===")

    query = input("What do you want to do? ")

    action = agent(query)

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

        print("Running repository analysis...")

        results = analyze_repos(repos)

        if not results:
            print("No results returned.")
            return

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