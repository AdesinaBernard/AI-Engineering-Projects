from advanced_planner import create_advanced_plan
from agent_executor import execute_plan
from router import route_request
from tools import TOOLS
from memory import save_repos, get_last_repos, save_message
from critic import llm_critique


def display_repo_results(results):
    if not results:
        print("No repository results returned.")
        return

    for repo in results:
        print(f"Repo: {repo['repo']}")
        print(f"Stars: {repo['stars']}")
        print(f"Forks: {repo['forks']}")
        print(f"Language: {repo['language']}")
        print("AI Insight:")
        print(repo["ai_insight"])
        print("-" * 50)


def main():
    print("=== AI Agent Started ===")

    while True:
        query = input("\nWhat do you want to do? ").strip()

        if query.lower() == "exit":
            print("Goodbye.")
            break

        save_message("user", query)

        # Memory follow-up
        if "language" in query.lower():
            last_repos = get_last_repos()

            if not last_repos:
                print("No repositories in memory.")
            else:
                results = TOOLS["analyze_repos"](last_repos)

                for repo in results:
                    print(f"{repo['repo']} uses {repo['language']}")

            continue

        plan = create_advanced_plan(query)
        print("DEBUG PLAN:", plan)

        if plan:
            print("\n=== EXECUTION PLAN ===")

            for step in plan:
                print(f"- {step['tool']}")

            results = execute_plan(plan)
            
            critique = llm_critique(
                    query,
                    results
            )

            print("\n=== CRITIC ===")
            print(
                f"Passed: {critique['passed']}"
            )
            print(
                f"Feedback: {critique['feedback']}"
            )   

            print("\n=== FINAL RESULTS ===\n")

            for item in results:
                print(f"\nTool: {item['tool']}")
                print(f"Status: {item.get('status')}")
                print(f"Retries: {item.get('retries')}")
                print(f"Reason: {item.get('reason')}")
                print("Result:")

                if item["tool"] == "analyze_repos":
                    display_repo_results(item["result"])
                else:
                    print(item["result"])

            continue

        # Fallback router flow
        action = route_request(query)

        print(f"Agent decided to: {action}")

        if action not in TOOLS:
            print("Unknown request.")
            continue

        if action == "rag":
            tool_input = query

        elif action == "analyze_repos":
            repos_input = input("Enter repos (comma separated): ")

            repos = [
                repo.strip()
                for repo in repos_input.split(",")
                if repo.strip()
            ]

            save_repos(repos)
            tool_input = repos
            print(f"Status: {item['status']}")
            print(f"Retries: {item['retries']}")    

        elif action == "summarizer":
            article_text = input("Paste the article text: ")
            tool_input = article_text
            print(f"Status: {item['status']}")
            print(f"Retries: {item['retries']}")

        else:
            tool_input = query

        print(f"Running tool: {action}")

        tool_function = TOOLS[action]
        results = tool_function(tool_input)

        print("\n=== Agent Results ===\n")

        if action == "analyze_repos":
            display_repo_results(results)
        else:
            if item["tool"] == "analyze_repos":
                if not item["result"]:
                    print("No repository results returned.")
                else:
                    display_repo_results(item["result"])
            else:
                print(item["result"])

if __name__ == "__main__":
    main()