from pyparsing import results
import requests


def fetch_repo_data(repo):
    url = f"https://api.github.com/repos/{repo}"
    
    try:
        response = requests.get(url, timeout=5)
        
        if response.status_code == 404:
            print(f"{repo} not found.")
            return None
        
        response.raise_for_status()
        data = response.json()

        return {
            "repo": data.get("full_name"),
            "stars": data.get("stargazers_count", 0)
        }

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {repo}: {e}")
        return None


def main():
    repos_input = input(
        "Enter repos separated by commas (e.g. python/cpython, django/django): "
    )
    
    repo_names = [repo.strip() for repo in repos_input.split(",") if repo.strip()]

    if not repo_names:
        print("No repos provided.")
        return

    results = []

    for repo in repo_names:
        repo_data = fetch_repo_data(repo)
        
        if repo_data:
            results.append(repo_data)
            print(f"Repo: {repo_data['repo']} -> Stars: {repo_data['stars']}")

    if results:
        top_repo = max(results, key=lambda item: item["stars"])
        print("\nTop repo by stars:")
        print(f"{top_repo['repo']} -> {top_repo['stars']} stars")
    else:
        print("No valid repos were fetched.")
    
    if results:
        #Sort the repos by stars in descending order
        sort_repos = sorted(results, key=lambda item: item["stars"], reverse=True)
        print("\nRepos sorted by stars:")
        for repo in sort_repos:
            print(f"{repo['repo']} -> {repo['stars']} stars")


if __name__ == "__main__":
    main()

