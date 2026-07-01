def test_imports():
    from app.agent import main
    from core.coordinator import coordinate
    from core.agent_executor import execute_task, execute_plan
    from agents.autonomous_research_agent import run_autonomous_research
    from evaluation.evaluation_framework import evaluate_execution
    from rag.rag import ask_rag

    print("All core imports passed.")


if __name__ == "__main__":
    test_imports()