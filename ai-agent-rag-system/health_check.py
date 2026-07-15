import os


REQUIRED_FILES = [
    "app/agent.py",
    "core/coordinator.py",
    "core/agent_executor.py",
    "core/tools.py",
    "core/router.py",
    "agents/autonomous_research_agent.py",
    "agents/research_planner.py",
    "agents/evidence_synthesizer.py",
    "planning/goal_decomposer.py",
    "planning/recursive_planner.py",
    "memory/long_term_memory.py",
    "evaluation/evaluation_framework.py",
    "evaluation/evidence_evaluator.py",
    "rag/rag.py",
    "rag/ingest.py",
    "rag/vector_store.py",
    "tools/repo_analyser_product.py",
    "tools/summarizer.py",
    "data/vector_db.json"
]


def run_health_check():
    missing = []

    for file in REQUIRED_FILES:
        if not os.path.exists(file):
            missing.append(file)

    if missing:
        print("\nMissing files:")
        for file in missing:
            print(f"- {file}")
        return False

    print("\nAll required files found.")
    return True


if __name__ == "__main__":
    run_health_check()