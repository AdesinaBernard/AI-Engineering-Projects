import requests


def fetch_repo_data(repo):
    url = f"https://api.github.com/repos/{repo}"
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        return {
            "name": data.get("full_name"),
            "stars": data.get("stargazers_count", 0),
            "forks": data.get("forks_count", 0),
            "issues": data.get("open_issues_count", 0),
            "language": data.get("language")
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
            print(f"Repo: {repo_data['name']} -> Stars: {repo_data['stars']}")

    if not results:
        print("No valid repos were fetched.")
        return

    # 🔹 Top repo by stars
    top_repo = max(results, key=lambda item: item["stars"])
    print("\nTop repo by stars:")
    print(f"{top_repo['name']} -> {top_repo['stars']} stars")

    # 🔹 Filter high-star repos
    high_star_repos = [repo for repo in results if repo["stars"] > 50000]
    print("\nRepositories with more than 50000 stars:")
    for repo in high_star_repos:
        print(f"{repo['name']} - Stars: {repo['stars']}")

    # 🔹 Group by language
    language_count = {}

    for repo in results:
        lang = repo["language"] or "Unknown"
        language_count[lang] = language_count.get(lang, 0) + 1

    print("\nRepos by Language:")
    for lang, count in language_count.items():
        print(f"{lang}: {count}")

    # 🔹 Engagement score
    for repo in results:
        repo["engagement_score"] = repo["stars"] + repo["forks"] * 2

    top_repo_engagement = max(results, key=lambda x: x["engagement_score"])

    print("\nTop Repo by Engagement:")
    print(f"{top_repo_engagement['name']} -> Score: {top_repo_engagement['engagement_score']}")

    # 🔹 LLM-friendly summaries
    print("\nRepo Summaries:")
    for repo in results:
        summary = (
            f"{repo['name']} has {repo['stars']} stars, "
            f"{repo['forks']} forks, written in {repo['language']}."
        )
        print(summary)


if __name__ == "__main__":
    main()