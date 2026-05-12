from repo_analyser_product import analyze_repos
from summarizer import summarize_text
from planner import create_plan
from rag import ask_rag


TOOLS = {
    "analyze_repos": analyze_repos,
    "summarizer": summarize_text,
    "planner": create_plan,
    "rag": ask_rag
    }