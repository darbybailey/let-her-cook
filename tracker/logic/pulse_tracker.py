import requests
import json
from datetime import datetime, timezone
import os

from tracker.logic.glyph_encoder import build_glyph_entry

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
        url = f"https://api.github.com/users/{USERNAME}/repos?page={page}&per_page=100&type=all&sort=pushed"
        res = requests.get(url, headers=HEADERS)
        if res.status_code != 200 or not res.json():
            break
        repos += res.json()
        page += 1
    return repos

def append_log(entries):
    run_data = {
        "run": datetime.now(timezone.utc).isoformat(),
        "entries": entries
    }

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            log = json.load(f)
    else:
        log = []

    log.append(run_data)

    with open(LOG_FILE, "w") as f:
        json.dump(log, f, indent=2)

def main():
    now = datetime.now(timezone.utc)
    entries = []

    print("🔍 Scanning repos...")

    for repo in fetch_repos():
        last_push = repo["pushed_at"]
        dt = datetime.strptime(last_push, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)

        if (now - dt).total_seconds() < 86400:  # 24 hours
            entry = build_glyph_entry(
                name=repo["name"],
                url=repo["html_url"],
                last_push=last_push,
                private=repo["private"],
                experiment=True
            )
            entries.append(entry)

    print(f"✅ Logged {len(entries)} repos.")
    append_log(entries)

if __name__ == "__main__":
    main()
