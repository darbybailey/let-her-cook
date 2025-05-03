"""
Glyph Encoder Module
This module contains functions to encode repository activity into symbolic glyphs.
"""

import json
import random
import datetime
import hashlib

# Define some symbolic characters to use as glyphs
GLYPH_SYMBOLS = [
    "◆", "◇", "◈", "■", "□", "▢", "▣", "▤", "▥", "▦", "▧", "▨", "▩", "▪", "▫",
    "○", "◌", "◍", "◎", "●", "◐", "◑", "◒", "◓", "◔", "◕", "◖", "◗", "◘", "◙",
    "◚", "◛", "◜", "◝", "◞", "◟", "◠", "◡", "◢", "◣", "◤", "◥", "◦", "◧", "◨",
    "◩", "◪", "◫", "◬", "◭", "◮", "◯", "☀", "☁", "☂", "☃", "☄", "★", "☆", "☇",
    "☈", "☉", "☊", "☋", "☌", "☍", "☎", "☏", "☐", "☑", "☒", "☓", "☔", "☕", "☖",
    "☗", "☘", "☙", "☚", "☛", "☜", "☝", "☞", "☟", "☠", "☡", "☢", "☣", "☤", "☥"
]

# Define patterns for visual styling
PATTERNS = ["alpha", "beta", "gamma", "delta", "epsilon", "zeta"]
LAYOUTS = ["constellation", "orbital", "spiral", "radial", "linear"]

# Define color palettes - each tuple is (primary, secondary)
COLOR_PALETTES = [
    ("#3A86FF", "#FF006E"),  # Blue/Pink
    ("#8338EC", "#FFBE0B"),  # Purple/Yellow
    ("#FB5607", "#8AC926"),  # Orange/Green
    ("#FF006E", "#FFBE0B"),  # Pink/Yellow
    ("#3A86FF", "#8AC926"),  # Blue/Green
    ("#8338EC", "#FB5607")   # Purple/Orange
]

def get_deterministic_choice(seed, choices):
    """
    Make a deterministic choice based on a seed.
    
    Args:
        seed (str): A seed string to determine the choice
        choices (list): List of choices to select from
        
    Returns:
        The selected choice
    """
    hash_val = int(hashlib.md5(seed.encode()).hexdigest(), 16)
    return choices[hash_val % len(choices)]

def build_glyph_entry(repo_activity=None):
    """
    Encode repository activity into a glyph entry.
    
    Args:
        repo_activity (dict, optional): Data about repository activity. 
                                       If None, will generate example data.
    
    Returns:
        dict: A glyph entry with encoded activity
    """
    # If no activity provided, create example data
    if repo_activity is None:
        repo_activity = {
            "repositories": ["let-her-cook"],
            "commits": random.randint(1, 5),
            "files_changed": random.randint(1, 10),
            "lines_added": random.randint(10, 100),
            "lines_removed": random.randint(5, 50)
        }
    
    # Generate timestamp for the entry
    timestamp = datetime.datetime.now().isoformat()
    
    # Encode the activity into glyphs
    glyphs = ""
    
    # Add a glyph for each repository
    for _ in repo_activity.get("repositories", []):
        glyphs += random.choice(GLYPH_SYMBOLS)
    
    # Add glyphs based on commit count
    commit_count = repo_activity.get("commits", 0)
    if commit_count > 0:
        for _ in range(min(commit_count, 5)):
            glyphs += random.choice(GLYPH_SYMBOLS)
    
    # Add glyphs based on changes
    files_changed = repo_activity.get("files_changed", 0)
    if files_changed > 0:
        for _ in range(min(files_changed // 2, 3)):
            glyphs += random.choice(GLYPH_SYMBOLS)
    
    # Add randomness if too few glyphs
    if len(glyphs) < 5:
        additional_glyphs = random.sample(GLYPH_SYMBOLS, 5 - len(glyphs))
        glyphs += ''.join(additional_glyphs)
    
    # Calculate intensity based on activity
    intensity = min(1.0, ((commit_count * 0.2) + (files_changed * 0.05)) / 3)
    if intensity < 0.4:  # Ensure minimum intensity
        intensity = 0.4 + random.random() * 0.3
    
    # Determine pulse (usually true but occasionally false)
    pulse = random.random() > 0.2
    
    # Determine cycle based on timestamp
    current_date = datetime.datetime.now()
    cycle = ((current_date.month - 1) * 30 + current_date.day) // 7 + 1
    
    # Generate deterministic values based on timestamp to ensure consistency
    seed = timestamp + glyphs
    resonance = get_deterministic_choice(seed, ["low", "medium", "high", "resonant", "dissonant"])
    pattern = get_deterministic_choice(seed + "pattern", PATTERNS)
    layout = get_deterministic_choice(seed + "layout", LAYOUTS)
    colors = get_deterministic_choice(seed + "colors", COLOR_PALETTES)
    
    # Create the glyph entry
    glyph_entry = {
        "timestamp": timestamp,
        "glyphs": glyphs,
        "pulse": pulse,
        "meta": {
            "cycle": cycle,
            "intensity": round(intensity, 2),
            "resonance": resonance,
            "pattern": pattern
        },
        "visual": {
            "primary": colors[0],
            "secondary": colors[1],
            "layout": layout
        }
    }
    
    return glyph_entry