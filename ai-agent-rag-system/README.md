# Local AI Agent + Conversational RAG System

A local AI engineering project that combines local LLM inference, semantic search, vector retrieval, conversational memory, and tool orchestration.

---

## 🚀 Overview

This repository implements a local AI agent and conversational RAG (retrieval-augmented generation) system. It includes document ingestion, semantic search/vector storage, an interactive agent that routes to tools, and utilities for summarization, planning, and evaluation.

---

## What's Included

- `agent.py` — interactive agent that routes user queries to tools and manages short-term memory.
- `router.py` — routes input to the appropriate tool (RAG, summarizer, planner, etc.).
- `ingest.py` — document ingestion pipeline for building the vector store from `documents/`.
- `vector_store.py` — simple persistent vector DB layer (backed by `vector_db.json`).
- `semantic_search.py` — semantic search and embedding utilities.
- `rag.py` — retrieval-augmented generation utilities using `knowledge_base.txt`.
- `rag_chat.py` — conversational RAG interface/runner.
- `rag_evaluator.py` — evaluation helpers for RAG responses.
- `summarizer.py` — text summarization utilities.
- `planner.py` — plan generation for multi-step tool execution.
- `memory.py` and `conversation_memory.py` — in-memory conversation/session memory utilities.
- `tools.py` — assorted helper tools used by the agent.
- `knowledge_base.txt`, `documents/` — content used for RAG and ingestion.
- `requirements.txt` — Python dependencies for running the project.

---

## 🔧 Current Features

- Document ingestion and vectorization pipeline
- Semantic search over ingested documents
- Conversational RAG with source-aware responses
- Interactive agent that can summarize, plan, and route tasks
- Simple in-memory conversational memory for follow-ups
- Evaluation utilities for RAG responses

---

## 🧩 Requirements

- Python 3.10+ (3.11 recommended)
- Install dependencies from `requirements.txt` (includes `requests`, `sentence-transformers`, `transformers`, `torch`, etc.)
- Optional: a local LLM or embedding provider if you want to run large-model inference locally

---

## ⚙️ Installation

```bash
git clone <this-repo-url-or-copy-local-folder>
cd ai-agent-rag-system
python3 -m venv ai_env
source ai_env/bin/activate
pip install -r requirements.txt
```

---

## ▶️ Quick Start / Usage

Ingest documents to build/update the vector store:

```bash
python ingest.py
```

Start a conversational RAG demo:

```bash
python rag_chat.py
```

Start the interactive agent (CLI):

```bash
python agent.py
```

Other utilities:

- `python rag.py` — run RAG utilities (script may be used programmatically).
- `python semantic_search.py` — run or import semantic search helpers.

---

## 📌 Notes

- The project expects `documents/` and `knowledge_base.txt` as inputs for retrieval. Adjust ingestion/config as needed.
- In-memory session state is used by default; persistence can be added later.
- Check `requirements.txt` for exact dependency versions used in development.

---

## 🚧 Future Improvements

- Add JSON/CSV export for report output and evaluation results
- Improve CLI argument parsing and user-facing help
- Add authentication and robust rate-limit handling for external APIs
- Add options for persistent memory backends
- Extend the retrieval pipeline (more advanced index types, ANN indexing)

---

## Architecture (high level)

User Input → Router → Tool Registry → Ingestion / RAG / Summarizer / Planner → LLM/Embedding Provider → Response

---

For details, see the project files and the docstrings in the code.
