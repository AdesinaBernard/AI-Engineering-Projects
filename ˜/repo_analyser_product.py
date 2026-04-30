import sys
import requests
import os
import datetime
import json

class Args:
    def __init__(self, repos, sort_by, top, min_stars, json_output):
        self.repos = repos
        self.sort_by = sort_by
        self.top = top
        self.min_stars = min_stars
        self.json_output = json_output

def parse_arguments():
    import sys
    args = sys.argv[1:]
    repos = []
    sort_by = 'engagement'
    top = 3
    min_stars = 0
    i = 0
    json_output = None

    while i < len(args):
        if args[i].startswith('--'):
            if args[i] == '--sort-by':
                if i+1 < len(args):
                    sort_by = args[i+1]
                    i += 2
                else:
                    print("Missing value for --sort-by")
                    sys.exit(1)
            elif args[i] == '--top':
                if i+1 < len(args):
                    top = int(args[i+1])
                    i += 2
                else:
                    print("Missing value for --top")
                    sys.exit(1)
            elif args[i] == '--min-stars':
                if i+1 < len(args):
                    min_stars = int(args[i+1])
                    i += 2
                else:
                    print("Missing value for --min-stars")
                    sys.exit(1)
            elif args[i] == '--json-output':
                if i+1 < len(args):
                    json_output = args[i+1]
                    i += 2
                else:
                    print("Missing value for --json-output")
                    sys.exit(1)
            else:
                print(f"Unknown option: {args[i]}")
                sys.exit(1)
        else:
            repos.append(args[i])
            i += 1
    if not repos:
        print("No repos provided. Usage: python script.py <repo1> <repo2> ... [--sort-by engagement|stars|forks] [--top N] [--min-stars N] [--json-output FILE]")
        sys.exit(1)
    if sort_by not in ['engagement', 'stars', 'forks']:
        print("Invalid sort-by value. Must be engagement, stars, or forks")
        sys.exit(1)
    return Args(repos, sort_by, top, min_stars, json_output)

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
    args = parse_arguments()
    repo_names = args.repos
    top_n = args.top
    min_stars = args.min_stars
    sort_by = args.sort_by
    json_output = args.json_output

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

        filtered_results = [r for r in results if r["stars"] >= min_stars]

        if not filtered_results:
            print("No repos match the minimum star threshold.")
            sys.stdout.flush()
            f.write("No repos match the minimum star threshold.\n")
            return

        # 🔹 Rank repos based on sort_by
        sort_map = {
                    "engagement": lambda x: x["engagement_score"],
                    "stars": lambda x: x["stars"],
                    "forks": lambda x: x["forks"]
                }

        sort_key = sort_map[sort_by]
        ranked = sorted(filtered_results, key=sort_key, reverse=True)

        print(f"\nTop repos by {sort_by}:")
        sys.stdout.flush()
        f.write(f"\nTop repos by {sort_by}:\n")

        for repo in ranked:
            value = repo["engagement_score"] if sort_by == "engagement" else repo[sort_by]
            line = f"- {repo['name']}: {value} ({sort_by})"
            print(line)
            sys.stdout.flush()
            f.write(line + "\n")

        top_results = ranked[:top_n]

        print("\n=== Top Repositories ===")
        sys.stdout.flush()
        f.write("\n=== Top Repositories ===\n")

        for i, repo in enumerate(top_results, 1):
            output_line = (
                f"{i}. {repo['name']}\n"
                f"   Stars: {repo['stars']}\n"
                f"   Forks: {repo['forks']}\n"
                f"   Score: {repo['engagement_score']}\n"
            )
            print(output_line)
            sys.stdout.flush()
            f.write(output_line + "\n")

    print(f"\nReport saved to: {report_path}")
    sys.stdout.flush()

    if json_output:
        json_data = {
            "generated_at": timestamp,
            "sort_by": sort_by,
            "top_n": top_n,
            "min_stars": min_stars,
            "repos": [
                {
                    "name": repo["name"],
                    "stars": repo["stars"],
                    "forks": repo["forks"],
                    "issues": repo.get("issues", 0),
                    "language": repo.get("language"),
                    "engagement_score": repo["engagement_score"]
                }
                for repo in top_results
            ]
        }

        with open(json_output, "w") as jf:
            json.dump(json_data, jf, indent=2)

        print(f"JSON report saved to: {json_output}")
        sys.stdout.flush()

if __name__ == "__main__":
    main()