import os
import sys


# Try to import the optional langchain client. If it's not available,
# we surface a clear error rather than a cryptic ImportError later.
try:
    from langchain_openai import ChatOpenAI
except Exception as _import_err:  # pragma: no cover - runtime helper
    ChatOpenAI = None
    _IMPORT_ERROR = _import_err


class CodingAgent:
    def __init__(self, model_name: str = "gpt-4.1-mini", dry_run: bool = False):
        print("[INIT] Initializing CodingAgent")

        self.dry_run = dry_run

        if dry_run:
            print("[INIT] Dry-run mode: skipping OpenAI client initialization.")
            self.llm = None
            return

        if ChatOpenAI is None:
            raise RuntimeError(
                "Missing dependency 'langchain_openai'. Install requirements: `pip install -r requirements.txt`."
                f" Import error: {_IMPORT_ERROR}"
            )

        # The ChatOpenAI implementation expects the OpenAI API key to be available
        # in the environment. We check and provide a helpful error.
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY environment variable is not set. Create a .env file or export the variable before running."
            )

        # Initialize the model client. Depending on your local langchain version,
        # the constructor signature may vary; the environment key will be used by
        # the client if supported.
        self.llm = ChatOpenAI(model=model_name)

        # Write your agent implementation here
        # Minimal, test-driven agent behavior implemented below via methods

    # --- Agent helpers -------------------------------------------------
    def discover_projects(self):
        """Return a list of project directories under `projects/`."""
        root = os.path.join(os.path.dirname(__file__), "projects")
        if not os.path.isdir(root):
            return []
        return [os.path.join(root, name) for name in os.listdir(root) if os.path.isdir(os.path.join(root, name))]

    def has_tests(self, project_path: str) -> bool:
        return os.path.isdir(os.path.join(project_path, "tests"))

    def run_pytest(self, project_path: str) -> dict:
        """Run pytest in the project directory and return a small report."""
        import subprocess

        cmd = [sys.executable, "-m", "pytest", "-q"]
        try:
            proc = subprocess.run(cmd, cwd=project_path, capture_output=True, text=True, timeout=120)
        except subprocess.TimeoutExpired:
            return {"returncode": 124, "output": "timeout"}

        out = (proc.stdout or "") + (proc.stderr or "")
        lines = out.strip().splitlines()
        return {"returncode": proc.returncode, "output_lines": lines[-20:]}

    def analyze(self) -> dict:
        """Analyze projects: run tests when present and return results as a dict."""
        results = {}
        for proj in self.discover_projects():
            name = os.path.basename(proj)
            info = {"path": proj, "has_tests": False, "tests": None}
            if self.has_tests(proj):
                info["has_tests"] = True
                info["tests"] = self.run_pytest(proj)
            results[name] = info
        return {"projects": results}


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run the coding agent")
    parser.add_argument("--dry-run", action="store_true", help="Run without OpenAI credentials for demo/testing")
    args = parser.parse_args()

    print("[MAIN] Running CodingAgent")
    try:
        agent = CodingAgent(dry_run=args.dry_run)
        if args.dry_run:
            print("[MAIN] Dry-run: agent started in demo mode.")
            # minimal demo action
            print("[DEMO] Agent would analyze projects/ and run tests if implemented.")
    except Exception as e:
        print(f"[ERROR] Failed to start agent: {e}")
        print("- Make sure you installed dependencies: pip install -r requirements.txt")
        print("- Make sure OPENAI_API_KEY is set (or add a .env file). See README.md.")
        sys.exit(1)
    print("[MAIN] Completed running CodingAgent")
