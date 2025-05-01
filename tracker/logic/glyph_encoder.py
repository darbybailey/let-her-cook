import hashlib
import base64
import os

SALT = os.environ.get("LHC_SALT", "changeme-🔐")

def hash_text(text: str) -> str:
    h = hashlib.sha256((SALT + text).encode()).digest()
    return base64.urlsafe_b64encode(h[:8]).decode()  # short 8-byte fingerprint

def build_glyph_entry(name, url, last_push, private=False, experiment=True):
    masked_name = hash_text(name)
    masked_trace = hash_text(url)

    return {
        "sigil": masked_name,
        "form": "drav" if not private else "krel",
        "pulse": "vaha",
        "drift": "vaha",
        "lastSeen": last_push,
        "trace": masked_trace if experiment else None
    }
