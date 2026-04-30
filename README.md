# Repo Analyzer CLI Tool

A command-line tool that fetches and analyzes GitHub repository data using the GitHub API. It provides ranking, filtering, and structured reporting for repository insights.

---

## Features

- Fetch repository data in real-time
- Rank repositories by stars, forks, or engagement
- Filter repositories using minimum star thresholds
- Generate timestamped reports
- CLI-based usage with flexible arguments

---

## Installation

```bash
git clone https://github.com/AdesinaBernard/repo-analyzer.git
cd repo-analyzer
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt


## Usage

python repo_analyzer_product.py python/cpython numpy/numpy pandas-dev/pandas --top 3 --sort-by stars --min-stars 50000

## Example Output
Top repos by stars:
- python/cpython: 52000
- numpy/numpy: 48000

## What I Learned
API integration using Python
Data processing and transformation
CLI tool development with argparse
Structuring reusable and maintainable code

## Future Improvements
JSON export support
Table-based output
Integration with LLMs for deeper analysis
