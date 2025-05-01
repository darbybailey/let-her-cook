from datetime import datetime, timezone

pulse_map = {
    "vaha": "🫀",
    "noor": "🌀",
    "lehl": "🌫",
    "isk": "🧊"
}

form_map = {
    "drav": "📦",
    "vael": "🧪",
    "krel": "🔒",
    "suhn": "🫧"
}

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

def build_glyph_entry(name, url, last_push, private=False, experiment=False):
    return {
        "sigil": name.replace("-", "_"),
        "form": encode_form(private, experiment),
        "pulse": encode_pulse(last_push),
        "drift": encode_pulse(last_push),
        "lastSeen": last_push,
        "trace": url
    }
