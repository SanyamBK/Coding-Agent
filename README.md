
# Mini Coding Agent

## Overview

This repository contains a small, test-driven coding agent plus three example Flask projects used for development, learning, and validation. The agent's role is to discover the subprojects under `projects/`, run their test suites, and—when necessary—apply small, well-scoped fixes to make the tests pass. The repository includes the source code, tests, and a short implementation report in `docs/`.

This README is focused on how to run and validate the projects; it does not contain assignment or implementation prompts.

This repository contains a small, test-driven coding agent and three example Flask projects used for development and validation.

Contents
- `agent.py` — lightweight agent to discover projects and run tests.
- `tests.py` — top-level test runner that aggregates project tests.
- `projects/` — three example Flask apps: `flask-easy`, `flask-intermediate`, `flask-hard`.
- `docs/report.tex` and `docs/report.pdf` — implementation summary and artifacts.

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

# How to run (local)
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



Notes
- Do not commit `.env` or virtual environment folders. Use CI secrets for sensitive keys.
- If you push to an upstream that enforces protected files, coordinate with the maintainers before changing those files.


