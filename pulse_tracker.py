import requests
import base64
import json
from datetime import datetime, timezone
import os

# === CONFIG ===
GITHUB_TOKEN = os.environ["LHC_TOKEN"]
USERNAME = os.environ["LHC_USERNAME"]
LOG_FILE = "cook-log.json"

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# === SYMBOLIC RULES ===
def get_pulse(last_push):
    now = datetime.now(timezone.utc)
    delta = now - datetime.strptime(last_push, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    if delta.days < 1:
        return "🫀"
    elif delta.days < 7:
        return "🌀"
    elif delta.days < 30:
        return "🌫"
    else:
        return "🧊"

def get_kind(is_private):
    return "🔒" if is_private else "📦"

# === FETCH ALL USER REPOS ===
def fetch_repos():
    repos = []
    page = 1
    while True:
        r = requests.get(f"https://api.github.com/user/repos?per_page=100&page={page}", headers=HEADERS)
        if r.status_code != 200:
            print("⚠️ Error fetching repos:", r.text)
            break
        data = r.json()
        if not data:
            break
        repos.extend(data)
        page += 1
    return repos

# === APPEND TO LOG ===
def append_log(entries):
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            existing = json.load(f)
    else:
        existing = []

    existing.append({
        "run": datetime.utcnow().isoformat() + "Z",
        "entries": entries
    })

    with open(LOG_FILE, "w") as f:
        json.dump(existing, f, indent=2)

# === MAIN ===
def main():
    print("🔍 Scanning repos...")
    entries = []
    for repo in fetch_repos():
        entry = {
            "sigil": repo["name"].replace("-", "_"),
            "pulse": get_pulse(repo["pushed_at"]),
            "kind": get_kind(repo["private"]),
            "lastSeen": repo["pushed_at"],
            "ref": repo["html_url"]
        }
        entries.append(entry)

    append_log(entries)
    print(f"✅ Logged {len(entries)} repo snapshots.")

if __name__ == "__main__":
    main()
