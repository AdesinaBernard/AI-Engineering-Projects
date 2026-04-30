import requests

repos_input = input("Enter repos separated by commas (e.g. python/cpython, django/django): ")
repo_names = [repo.strip() for repo in repos_input.split(",") if repo.strip()]

if not repo_names:
    print("No repos provided.")
    raise SystemExit(1)

results = []

for repo in repo_names:
    url = f"https://api.github.com/repos/{repo}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        results.append({
            "repo": data["full_name"],
            "stars": data["stargazers_count"]
        })
        print(f"Repo: {data['full_name']} -> Stars: {data['stargazers_count']}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {repo}: {e}")

if results:
    top_repo = max(results, key=lambda item: item["stars"])
    print("\nTop repo by stars:")
    print(f"{top_repo['repo']} -> {top_repo['stars']} stars")
else:
    print("No valid repos were fetched.")