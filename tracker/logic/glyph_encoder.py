import hashlib
import base64
import os

SALT = os.environ.get("LHC_SALT", "changeme🔐")

def hash_text(text: str) -> str:
    h = hashlib.sha256((SALT + text).encode()).digest()
    return base64.urlsafe_b64encode(h[:8]).decode("utf-8")  # 8-byte fingerprint

def build_glyph_entry(name, url, last_push, private=False, experiment=True):
    return {
        "sigil": hash_text(name),
        "form": "krel" if private else "drav",
        "pulse": "vaha",
        "drift": "vaha",
        "lastSeen": last_push,
        "trace": hash_text(url) if experiment else None
    }
