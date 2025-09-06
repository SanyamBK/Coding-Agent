
# Mini Coding Agent

This repository was created for the "Build Your Own Coding Agent" hackathon, organized by HackerRank, which took place from 5 September 2025 at 05:30 IST to 8 September 2025 at 05:30 IST.

## Overview

This project is intended as a practical developer tool and lab: it demonstrates an automated, test-driven workflow where a small agent inspects subprojects under `projects/`, runs their tests, and reports actions taken. Key points:

- Design intent: keep fixes minimal and focused — the agent performs small, deterministic edits (e.g., bugfixes, missing return values, simple refactors) so test behavior changes are easy to review.
- Validation model: every change is validated by running the affected project's test suite; results are reported as JSON summaries and human-readable logs.
- Extensibility: agent logic is intentionally modular — add new project detectors, test runners, or language handlers by implementing small adapters under the top-level agent module.
- Safety and reproducibility: the agent avoids committing secrets, writes no persistent side effects outside project directories, and can run in dry-run mode to preview planned edits.
- Usage notes: configure required environment variables (no .env assumed), run `python tests.py` to run all projects' tests, and use `python agent.py --dry-run` to preview actions before applying them.


Supported projects:
- flask-easy — basic event ticketing example
- flask-intermediate — JWT authentication example
- flask-hard — log processing and notification example

Primary workflows:
- Run all tests: `python tests.py`
- Run the agent in dry-run mode: `python agent.py --dry-run`
- Run a single project tests: see `projects/<project>/README.md`


## High Level Structure

```
mini-coding-agent/
├── agent.py (implement your agent here)
├── tests.py (for running all the test cases)
├── check_usage.py (for checking LLM resource utilisation)
├── projects
        ├── project_1
                ├── app/
                ├── README.md
        ├── project_2
                ├── app/
                ├── README.md
└── requirements.txt
```

## How to run (local)
1. Create and activate a virtual environment (recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run all tests (top-level):

```powershell
python tests.py
```

4. Run the agent in dry-run to see planned actions:

```powershell
python agent.py --dry-run
```


