## Architecture

This project is a modular local AI agent system.

Core layers:

- App entrypoint: `app/agent.py`
- Coordination: `core/coordinator.py`
- Execution: `core/agent_executor.py`
- Planning: `planning/`
- Agents: `agents/`
- RAG: `rag/`
- Memory: `memory/`
- Evaluation: `evaluation/`
- Tools: `tools/`
- Data: `data/`

Main capabilities:

- Local LLM inference
- Semantic retrieval
- Conversational RAG
- Autonomous research agent
- Multi-agent collaboration
- Recursive task generation
- Long-term memory
- Reflection and failure handling
- Evaluation scoring

# Local AI Agent + Conversational RAG System

This repository is a modular local AI agent and conversational RAG (retrieval-augmented generation) system. It provides document ingestion, semantic search, a vector store, conversational memory, multi-agent orchestration, planning, and evaluation tooling designed for local development and experimentation.

---

## 🚀 What Changed / Current Status

- The project has been refactored into a multi-package layout with dedicated modules for agents, core orchestration, RAG, memory, planning, evaluation, and tooling.
- Added multiple agent implementations under `agents/` (e.g., `planner_agent.py`, `research_agent.py`, `execution_agent.py`).
- Added evaluation and dashboard utilities under `evaluation/` and `evaluation_suite.py` for running automated checks.
- A Python virtual environment is included at `ai_env/` (optional — you can recreate or use your own).

---

## Project Structure (high level)

- `agent.py`, `agent_message.py` — root CLI entrypoints and message helpers.
- `app/` — higher-level application glue (`app/agent.py`).
- `agents/` — multiple agent implementations and coordinators.
- `core/` — orchestration code: `agent_executor.py`, `coordinator.py`, `router.py`, and task/ tool management.
- `rag/` — RAG pipeline and vector store: `ingest.py`, `rag.py`, `rag_chat.py`, `vector_store.py`, `semantic_search.py`, `rag_evaluator.py`.
- `memory/` — memory implementations and extractors (`conversation_memory.py`, `long_term_memory.py`).
- `planning/` — planners and goal decomposition utilities.
- `evaluation/` and `evaluation_suite.py` — evaluation framework and dashboards.
- `tools/` — helper tools such as `summarizer.py` and `prompt_optimizer.py`.
- `data/` — `documents/`, `long_term_memory.json`, `vector_db.json`, `evaluations.json` used by ingestion and testing.
- `tests/` — unit/integration tests for core behaviors.

Refer to the source files for implementation details and docstrings.

---

## 🔧 Requirements

- Python 3.10+ (3.11 recommended).
- Install dependencies from `requirements.txt`.

If you want to use GPU-accelerated models or local LLMs, ensure you have the appropriate frameworks installed (PyTorch, CUDA drivers, etc.).

---

## ⚙️ Installation (recommended)

Use a virtual environment and install dependencies:

```bash
cd ai-agent-rag-system
python3 -m venv .venv    # or reuse included `ai_env/` if desired
source .venv/bin/activate
pip install -r requirements.txt
```

---

## ▶️ Common Commands / Quick Start

- Run the root interactive agent (CLI):

```bash
python agent.py
```

- Run the app-level agent:

```bash
python -m app.agent
```

- Ingest documents into the vector store (RAG ingestion):

```bash
python -m rag.ingest
```

- Start a conversational RAG demo (module):

```bash
python -m rag.rag_chat
```

- Run the evaluation dashboard:

```bash
python -m evaluation.evaluation_dashboard
```

- Run tests:

```bash
pytest -q
```

---

## 🔎 Notes & Conventions

- Short-lived session memory is kept in-memory by default; `memory/long_term_memory.py` contains examples for persistence.
- The `data/documents/` folder and `data/*json` files are used as sample inputs for ingestion and evaluation.
- Many components can be used programmatically — import the modules and call the helper functions from scripts or notebooks.

---

## 🚧 Future Work / Next Steps

- Harden CLI argument parsing and add better help text for scripts under `rag/` and `agents/`.
- Add optional persistent memory backends and alternate vector indices (FAISS, Annoy, etc.).
- Add example notebooks and end-to-end demo scripts.

---

If you'd like, I can (1) run the test suite, (2) run the evaluation dashboard to confirm examples, or (3) create a compact CONTRIBUTING.md and quick developer guide.
