"""
Glyph Encoder Module
This module contains functions to encode repository activity into symbolic glyphs.
"""

import json
import random
import datetime

# Define some symbolic characters to use as glyphs
GLYPH_SYMBOLS = [
    "◆", "◇", "◈", "■", "□", "▢", "▣", "▤", "▥", "▦", "▧", "▨", "▩", "▪", "▫",
    "○", "◌", "◍", "◎", "●", "◐", "◑", "◒", "◓", "◔", "◕", "◖", "◗", "◘", "◙",
    "◚", "◛", "◜", "◝", "◞", "◟", "◠", "◡", "◢", "◣", "◤", "◥", "◦", "◧", "◨",
    "◩", "◪", "◫", "◬", "◭", "◮", "◯", "☀", "☁", "☂", "☃", "☄", "★", "☆", "☇",
    "☈", "☉", "☊", "☋", "☌", "☍", "☎", "☏", "☐", "☑", "☒", "☓", "☔", "☕", "☖",
    "☗", "☘", "☙", "☚", "☛", "☜", "☝", "☞", "☟", "☠", "☡", "☢", "☣", "☤", "☥"
]

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
            "commits": random.randint(0, 5),
            "files_changed": random.randint(0, 10),
            "lines_added": random.randint(0, 100),
            "lines_removed": random.randint(0, 50)
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
        glyphs += random.choice(GLYPH_SYMBOLS) * min(commit_count, 5)
    
    # Add glyphs based on changes
    files_changed = repo_activity.get("files_changed", 0)
    if files_changed > 0:
        glyphs += random.choice(GLYPH_SYMBOLS) * min(files_changed // 2, 3)
    
    # Create the glyph entry
    glyph_entry = {
        "timestamp": timestamp,
        "glyphs": glyphs,
        "pulse": random.random() > 0.3  # Random pulse indicator
    }
    
    return glyph_entry