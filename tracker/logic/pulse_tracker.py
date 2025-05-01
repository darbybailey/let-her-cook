import requests
import base64
import json
from datetime import datetime, timezone
import os
from glyph_encoder import build_glyph_entry

# === CONFIG ===
GITHUB_TOKEN = os.environ["LHC_TOKEN"]
USERNAME = os.environ["LHC_USERNAME"]
LOG_FILE = "cook-log.json"

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

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

def main():
    print("🔍 Scanning repos...")
    entries = []
for repo in fetch_repos():
    last_push = repo["pushed_at"]
    dt = datetime.strptime(last_push, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    if (datetime.now(timezone.utc) - dt).days < 1:
        entry = build_glyph_entry(
            name=repo["name"],
            url=repo["html_url"],
            last_push=last_push,
            private=repo["private"],
            experiment=False
        )
        entries.append(entry)

    entries = []

for repo in fetch_repos():
    last_push = repo["pushed_at"]
    dt = datetime.strptime(last_push, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)

    if (datetime.now(timezone.utc) - dt).days < 1:
        entry = build_glyph_entry(
            name=repo["name"],
            url=repo["html_url"],
            last_push=last_push,
            private=repo["private"],
            experiment=False
        )
        entries.append(entry)

# Filter repos by last push time (within last 24h)
entries = []
now = datetime.now(timezone.utc)

for repo in fetch_repos():
    last_push = repo["pushed_at"]
    dt = datetime.strptime(last_push, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    
    if (now - dt).total_seconds() < 86400:  # 24 hours = 86400 seconds
        entry = build_glyph_entry(
            name=repo["name"],
            url=repo["html_url"],
            last_push=last_push,
            private=repo["private"],
            experiment=True  # or False depending on your mask strategy
        )
        entries.append(entry)

append_log(entries)

    append_log(entries)
    print(f"✅ Logged {len(entries)} repos.")

if __name__ == "__main__":
    main()
