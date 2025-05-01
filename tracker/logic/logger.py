import json
from datetime import datetime
import os

LOG_PATH = "cook-log.json"

def log_new_project(name, url, visibility="public", status="created"):
    entry = {
        "name": name,
        "url": url,
        "visibility": visibility,
        "status": status,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

    if not os.path.exists(LOG_PATH):
        with open(LOG_PATH, "w") as f:
            json.dump([entry], f, indent=2)
    else:
        with open(LOG_PATH, "r") as f:
            data = json.load(f)
        data.append(entry)
        with open(LOG_PATH, "w") as f:
            json.dump(data, f, indent=2)

    print(f"🧠 Logged {name} to {LOG_PATH}")
