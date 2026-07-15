from tools.repo_analyser_product import analyze_repos
from tools.summarizer import summarize_text
from rag.rag import ask_rag


TOOLS = {
    "analyze_repos": analyze_repos,
    "summarizer": summarize_text,
    "rag": ask_rag
}