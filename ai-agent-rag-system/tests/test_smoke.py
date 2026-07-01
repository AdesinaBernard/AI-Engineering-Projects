from rag.rag import ask_rag
from agents.autonomous_research_agent import run_autonomous_research


def test_rag():
    result = ask_rag(
        "Why are NumPy arrays more efficient than Python lists?"
    )

    assert "NumPy" in result or "arrays" in result

    print("RAG smoke test passed.")


def test_autonomous_research():
    result = run_autonomous_research("NumPy")

    assert result["result"]["confidence"] >= 50

    print("Autonomous research smoke test passed.")


if __name__ == "__main__":
    test_rag()
    test_autonomous_research()