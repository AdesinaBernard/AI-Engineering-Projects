from repo_analyser_product import analyze_repos
from summarizer import summarize_text
from planner import create_plan


TOOLS = {
    "analyze_repos": analyze_repos,
    "summarizer": summarize_text,
    "planner": create_plan
}