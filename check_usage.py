import requests
import os
import json
import sys
from dotenv import load_dotenv

# Load .env from repo root if present so users can store keys locally
load_dotenv()


OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    print("[ERROR] OPENAI_API_KEY is not set. Set it in your environment or in a .env file.")
    sys.exit(1)

if not OPENAI_API_BASE:
    print("[ERROR] OPENAI_API_BASE is not set. If you are using the hosted OpenAI platform, set OPENAI_API_BASE to https://api.openai.com/v1")
    sys.exit(1)

base_url = OPENAI_API_BASE.replace("/v1", "") if OPENAI_API_BASE else ""
url = f"{base_url}/key/info"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {OPENAI_API_KEY}",
}

try:
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    parsed = response.json()
except Exception as e:
    print(f"[ERROR] Failed to fetch key info: {e}")
    sys.exit(1)

utilization = {
    "tpm_limit": parsed.get("info", {}).get("tpm_limit"),
    "rpm_limit": parsed.get("info", {}).get("rpm_limit"),
    "max_budget": parsed.get("info", {}).get("max_budget"),
    "budget_utilised": parsed.get("info", {}).get("spend"),
    "remaining_budget": (
        parsed.get("info", {}).get("max_budget") - parsed.get("info", {}).get("spend", 0)
        if parsed.get("info", {}).get("max_budget") is not None
        else None
    ),
}

print(json.dumps(utilization, indent=2))