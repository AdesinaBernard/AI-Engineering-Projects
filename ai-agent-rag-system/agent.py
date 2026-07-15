from core.agent_executor import execute_plan
from planning.advanced_planner import create_advanced_plan
from memory.memory_extractor import extract_memory
from evaluation.evaluation_framework import evaluate_execution
from tools.summarizer import summarize_text
from rag.rag import ask_rag




def display_repo_results(results):
    if isinstance(results, dict) and results.get("error"):
        print("Repository analysis failed.")
        print(f"Repo: {results.get('repo')}")
        print(f"Reason: {results.get('reason')}")
        return

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


def display_execution_results(results):
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


def main():
    print("=== AI Agent Started ===")

    while True:
        query = input("\nWhat do you want to do? ").strip()

        if query.lower() == "exit":
            print("Goodbye.")
            break

        save_message("user", query)
        extract_memory(query)
        
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

        # Multi-agent flow
        if (
            "analyze" in query.lower()
            or "analyse" in query.lower()
            or "explain" in query.lower()
            or "summarize" in query.lower()
            or "summarise" in query.lower()
        ):

            output = coordinate(query)

            evaluation = evaluate_execution(output["results"])

            print("\n=== EVALUATION ===")

            for key, value in evaluation.items():
                print(f"{key}: {value}")

            save_evaluation(evaluation)

            print("\n=== MULTI-AGENT RESULT ===")
            print(output)

            continue

        # Agentic planning flow
        plan = create_advanced_plan(query)
        facts = get_facts()

        if plan:
            print("\n=== EXECUTION PLAN ===")

            for step in plan:
                print(f"- {step['tool']}")

            results = execute_plan(plan)

            evaluation = evaluate_execution(results)

            print("\n=== EVALUATION ===")

            for key, value in evaluation.items():
                print(f"{key}: {value}")

            save_evaluation(evaluation)

            critique = llm_critique(query, results)

            print("\n=== CRITIC ===")
            print(f"Passed: {critique['passed']}")
            print(f"Feedback: {critique['feedback']}")

            print("\n=== FINAL RESULTS ===")
            display_execution_results(results)

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

        elif action == "summarizer":
            article_text = input("Paste the article text: ")
            tool_input = article_text

        else:
            tool_input = query

        print(f"Running tool: {action}")

        tool_function = TOOLS[action]
        results = tool_function(tool_input)

        print("\n=== Agent Results ===")

        if action == "analyze_repos":
            display_repo_results(results)
        else:
            print(results)
        if "collaborate" in query.lower():
            result = run_collaboration(query)
            print("\n=== COLLABORATIVE AGENT RESULT ===")
            print(result)
            continue


if __name__ == "__main__":
    main()