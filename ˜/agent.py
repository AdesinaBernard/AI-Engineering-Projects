from repo_analyser_product import analyze_repos
from router import route_request
from memory import (
    save_repos,
    get_last_repos,
    save_message,
    get_history
)
from tools import TOOLS
from planner import create_plan

def main():

    print("=== AI Agent Started ===")

    while True:

        query = input(
            "\nWhat do you want to do? "
        )
        if "and" in query.lower():

            print("Creating execution plan...\n")

            plan = create_plan(query)

            print("=== PLAN ===")
            print(plan)
            print()

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

        if action in TOOLS:

    # -----------------------------
    # TOOL INPUT HANDLING
    # -----------------------------

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

                tool_input = repos

            elif action == "summarizer":

                article_text = input(
                   "Paste the article text: "
               )

                tool_input = article_text

            else:
                tool_input = query

    # -----------------------------
    # RUN TOOL
    # -----------------------------

            print(f"Running tool: {action}")

            tool_function = TOOLS[action]

            results = tool_function(tool_input)

    # -----------------------------
    # DISPLAY RESULTS
    # -----------------------------

            print("\n=== Agent Results ===\n")

            if action == "analyze_repos":

                if not results:
                   print("No repository results returned.")

                else:

                    for repo in results:

                       print(f"Repo: {repo['repo']}")
                       print(f"Stars: {repo['stars']}")
                       print(f"Forks: {repo['forks']}")
                       print(f"Language: {repo['language']}")

                       print("AI Insight:")
                       print(repo["ai_insight"])

                    print("-" * 50)

            else:

                print(results)

        else:
            print("Unknown request.")

if __name__ == "__main__":
    main()