# AI Repo Analyzer and Agent

A Python project that combines GitHub repository analysis with AI-assisted workflows.
It includes tools for fetching repository metadata, ranking repositories by engagement, generating AI-driven insights, summarizing text, and routing requests through an interactive agent.

---

## 🚀 What’s Included

- `repo_analyser.py` — fetch GitHub repo metadata, compute engagement scores, rank repositories, and save timestamped reports.
- `repo_analyser_product.py` — analyze GitHub repositories and enrich the top results with AI-generated insights using a local LLM.
- `agent.py` — interactive agent interface that routes user queries to tools, builds execution plans, and uses memory for follow-up actions.
- `summarizer.py` — summarize free-form text into exactly three bullet points.
- `planner.py` — generate ordered tool execution plans from complex user goals.
- `rag.py` — perform retrieval-augmented generation using `knowledge_base.txt`.
- `memory.py` — store lightweight session memory for recent repos and conversation history.

---

## 🔧 Current Features

- GitHub repository metadata retrieval via GitHub API
- Computation of repository engagement score: `stars + forks * 2`
- Top-repo ranking and report generation
- AI insight generation for top repositories via a local LLM endpoint
- Interactive tool routing for repo analysis, summarization, planning, and RAG
- Simple runtime memory for follow-up queries and recent repository context
- Support for knowledge base lookups through RAG

---

## 🧩 Requirements

- Python 3.x
- `requests` library
- Local LLM server available at `http://localhost:8080/completion` for AI/LLM-powered features

---

## ⚙️ Installation

```bash
git clone https://github.com/AdesinaBernard/repo-analyzer.git
cd repo-analyzer
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

If `requirements.txt` is not present, install the runtime dependency manually:

```bash
pip install requests
```

---

## ▶️ Usage Examples

Run simple repository analysis and save a report:

```bash
python repo_analyser.py python/cpython numpy/numpy
```

Run AI-enabled product analysis for top repositories:

```bash
python repo_analyser_product.py python/cpython numpy/numpy
```

Start the interactive agent:

```bash
python agent.py
```

The agent supports natural queries and can route them to available tools such as repo analysis, summarization, and RAG.

---

## 📌 Notes

- AI-powered features depend on a local LLM completion endpoint.
- The agent currently uses in-memory session state, so memory resets when the process exits.
- `knowledge_base.txt` is used by `rag.py` for context retrieval.

---

## 🧠 Progress Summary

The project now includes both a focused CLI repository analyzer and an AI agent interface. It supports data fetching, scoring, ranking, summarizing, planning, and retrieval-augmented question answering.

## 🚧 Future Improvements

- Add JSON/CSV export for report output
- Improve command-line argument parsing and CLI help
- Add authentication support for GitHub API rate limits
- Enhance the agent with more tools and persistent memory
- Extend the knowledge base and retrieval method for better RAG performance
