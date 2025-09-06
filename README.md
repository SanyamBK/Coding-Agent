# Mini Coding Agent (clean README)

This repository contains a small, test-driven coding agent and three example Flask projects used for development and validation.

Contents
- `agent.py` — lightweight agent to discover projects and run tests.
- `tests.py` — top-level test runner that aggregates project tests.
- `projects/` — three example Flask apps: `flask-easy`, `flask-intermediate`, `flask-hard`.
- `docs/report.tex` and `docs/report.pdf` — implementation summary and artifacts.

Quick start (local)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python tests.py
```

Run the agent in dry-run to preview actions:
```powershell
python agent.py --dry-run
```

Notes
- Do not commit `.env` or virtual environment folders. Use CI secrets for sensitive keys.
- If you push to an upstream that enforces protected files, coordinate with the maintainers before changing those files.

Author
- Prepared by SanyamBK. Development assistance provided by GitHub Copilot for local edits and validation.
