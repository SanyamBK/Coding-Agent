import os
import json
import sys
import requests
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    print("[ERROR] OPENAI_API_KEY is not set. Create a .env file or export the variable and try again.")
    sys.exit(1)

if not OPENAI_API_BASE:
    print("[ERROR] OPENAI_API_BASE is not set. Create a .env file or export the variable and try again.")
    sys.exit(1)

# Ensure the base URL includes a scheme (default to https://)
base_url = OPENAI_API_BASE.strip()
if not base_url.startswith("http://") and not base_url.startswith("https://"):
    base_url = "https://" + base_url

base_url = base_url.replace('/v1', '')
url = f"{base_url}/key/info"

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {OPENAI_API_KEY}'
}

try:
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
except requests.RequestException as exc:
    print(f"[ERROR] Failed to fetch usage info: {exc}")
    sys.exit(1)

data = resp.json()
info = data.get('info', {}) if isinstance(data, dict) else {}

utilization = {
    "tpm_limit": info.get('tpm_limit'),
    "rpm_limit": info.get('rpm_limit'),
    "max_budget": info.get('max_budget'),
    "budget_utilised": info.get('spend'),
    "remaining_budget": (info.get('max_budget') - info.get('spend', 0)) if info.get('max_budget') is not None else None
}

print(json.dumps(utilization, indent=2))