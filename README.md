
# Mini Coding Agent

This repository contains a small, test-driven coding agent plus three example Flask projects used for development, learning, and validation.

## Overview

 The agent's role is to discover the subprojects under `projects/`, run their test suites, and—when necessary—apply small, well-scoped fixes to make the tests pass. The repository includes the source code, tests, and a short implementation report in `docs/`.

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
                # Mini Coding Agent

                Purpose
                -------
                A compact, test-driven example showing an automated coding agent that discovers subprojects, runs tests, and applies small, targeted fixes where required. The repository contains three sample Flask projects and tooling used during development.

                Repository layout
                -----------------
                - `agent.py` — discovery driver and lightweight agent (supports `--dry-run`).
                - `tests.py` — top-level test runner that aggregates individual project tests.
                - `projects/` — example applications:
                        - `flask-easy` — simple REST endpoints and model tests.
                        - `flask-intermediate` — JWT authentication and protected routes.
                        - `flask-hard` — log ingestion, Pydantic models, threaded processing, metrics.
                - `docs/` — implementation summary (`report.tex` and `report.pdf`).

                Quick start (local)
                -------------------
                1. Create and activate a virtual environment (PowerShell):

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

                4. Run a single project's tests (example):

                ```powershell
                cd projects\flask-hard
                pytest -q
                ```

                5. Preview agent actions without making changes:

                ```powershell
                python agent.py --dry-run
                ```

                Notes
                -----
                - Avoid committing `.env` or virtual environment folders. Add them to `.gitignore`.
                - The upstream may enforce server-side hooks that protect specific files (e.g., `check_usage.py`). If a push is rejected referencing a protected file, restore the file from upstream or coordinate with maintainers.

                Attribution
                -----------
                Prepared by SanyamBK with development assistance from GitHub Copilot (local edits and validation performed in this workspace).

                If you'd like this README tailored (shorter, PR-ready, or maintainer-focused), tell me the target and I'll produce a variant.


