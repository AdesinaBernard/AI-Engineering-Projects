import sys
import requests
import os
import datetime


def fetch_repo_data(repo):
    url = f"https://api.github.com/repos/{repo}"
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        return {
            "success": True,
            "data": {
                "name": data.get("full_name"),
                "stars": data.get("stargazers_count", 0),
                "forks": data.get("forks_count", 0),
                "issues": data.get("open_issues_count", 0),
                "language": data.get("language")
            }
        }

    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"Error fetching {repo}: {e}"
        }


def main():
    repo_names = sys.argv[1:]

    if not repo_names:
        print("Usage: python repo_analyzer.py <repo1> <repo2> ...")
        sys.exit(1)

    results = []

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(os.path.dirname(__file__), f"report_{timestamp}.txt")

    with open(report_path, "w") as f:
        for repo in repo_names:
            result = fetch_repo_data(repo)

            if result["success"]:
                repo_data = result["data"]
                results.append(repo_data)

                message = f"Fetched: {repo_data['name']} ({repo_data['stars']} stars)"
                print(message)
                sys.stdout.flush()
                f.write(message + "\n")
            else:
                print(result["error"])
                sys.stdout.flush()
                f.write(result["error"] + "\n")

        if not results:
            print("No valid repos were fetched.")
            sys.stdout.flush()
            f.write("No valid repos were fetched.\n")
            return

        # 🔹 Compute engagement score
        for repo in results:
            repo["engagement_score"] = repo["stars"] + repo["forks"] * 2

        # 🔹 Rank repos
        ranked = sorted(results, key=lambda x: x["engagement_score"], reverse=True)

        print("\nTop repos by engagement score:")
        sys.stdout.flush()
        f.write("\nTop repos by engagement score:\n")

        for repo in ranked:
            line = f"- {repo['name']}: {repo['engagement_score']} (Stars: {repo['stars']}, Forks: {repo['forks']})"
            print(line)
            sys.stdout.flush()
            f.write(line + "\n")

    print(f"\nReport saved to: {report_path}")
    sys.stdout.flush()


if __name__ == "__main__":
    main()