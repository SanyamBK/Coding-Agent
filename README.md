# Mini Coding Agent

Implement a coding agent using Python and your preferred agentic framework like LangGraph, CrewAI, etc. The agent should analyse and implement the project requirements from the various projects present under the `projects/` directory.

## Overview

The agent goes through the projects in the `projects/` directory, each project potentially using different programming languages and frameworks. The agent should,

- Read the README.md file of each project to understand the requirements
- Implement any missing functionality like APIs, functions, models, etc....
- Runs unit tests available at each project to validate the correctness of the implementations.
- Be able to handle various programming languages and frameworks.

The agent should be able to handle various implementation needs such as but not limited to:

- Implementing API endpoints and routes
- Implementing function and method definitions
- Implement data models and schemas
- Define utility functions and helpers

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

Each project should have:

- A `README.md` file with requirements that needs to be fulfilled.
# Mini Coding Agent

This repository contains a small, test-driven coding agent and three example Flask projects used for exercise and validation.

This fork contains the following changes and artifacts (created while developing and validating the agent):

- Implementations and tests for three example projects in `projects/`:
   - `flask-easy` — REST endpoints and SQLAlchemy fixes (tests green)
   - `flask-intermediate` — JWT login and protected endpoints (tests green)
   - `flask-hard` — Pydantic logs, threaded LogProcessor, metrics and notifications (tests green)
- A lightweight agent in `agent.py` with a `--dry-run` mode and a minimal `analyze()` runner that discovers subprojects and runs pytest.
- Documentation PDF in `docs/report.pdf` (also present as `docs/report.tex`).

Agent features
- Discover projects under `projects/` and run tests when `tests/` exists.
- Perform small code edits and implement missing endpoints/models where tests require.
- Dry-run mode to show planned actions without executing them.

How to run (local)
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

Push to your GitHub (example)

If you want to push this repository to your own GitHub, these are the commands you provided:

```powershell
git remote add origin https://github.com/SanyamBK/Coding-Agent.git
git branch -M main
git push -u origin main
```

Notes
- Do not commit `.env` or virtual environment folders. Use CI secrets for sensitive keys.
- The file `check_usage.py` in the original upstream may be protected by a server-side hook. If a push fails referencing that file, restore it to the upstream state or coordinate with the repository maintainers.

Contact / author
This fork was prepared by SanyamBK with development assistance from GitHub Copilot (local edits and test validation performed in this workspace).
