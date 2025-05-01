import hashlib
import hmac
import os
from datetime import datetime, timezone

# === Glyph Vocabulary ===
pulse_map = {
    "vaha": "🫀",  # heartbeat
    "noor": "🌀",  # creative orbit
    "lehl": "🌫",  # drift
    "isk": "🧊"   # frozen
}

form_map = {
    "drav": "📦",  # public container
    "vael": "🧪",  # experiment
    "krel": "🔒",  # private/ritual
    "suhn": "🫧"   # ephemeral
}

# === Secure Salt for Sigil Masking ===
SECRET_SALT = os.environ.get("LHC_SALT", "default_salt")

def mask_name(name):
    digest = hmac.new(SECRET_SALT.encode(), msg=name.encode(), digestmod=hashlib.sha256).hexdigest()
    return "hidden_" + digest[:10]

# === Symbolic Time Encoding ===
def encode_pulse(last_push):
    now = datetime.now(timezone.utc)
    delta = now - datetime.strptime(last_push, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    if delta.days < 1:
        return "vaha"
    elif delta.days < 7:
        return "noor"
    elif delta.days < 30:
        return "lehl"
    else:
        return "isk"

def encode_form(is_private, is_experiment=False):
    if is_experiment:
        return "vael"
    return "krel" if is_private else "drav"

# === Core Glyph Generator ===
def build_glyph_entry(name, url, last_push, private=False, experiment=False):
    masked = private
    return {
        "sigil": mask_name(name) if masked else name.replace("-", "_"),
        "form": encode_form(private, experiment),
        "pulse": encode_pulse(last_push),
        "drift": encode_pulse(last_push),
        "lastSeen": last_push,
        "trace": None if masked else url
    }
