"""
Pulse Tracker Module
This module tracks repository activity and encodes it into symbolic glyphs.
"""

import os
import sys
import json
import datetime
from pathlib import Path

# Ensure the project root is in the Python path
# This is crucial for the imports to work correctly in GitHub Actions
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Now we can safely import from tracker package
from tracker.logic.glyph_encoder import build_glyph_entry

def get_repo_activity():
    """
    Get repository activity data.
    In a real implementation, this would scan git repositories.
    
    Returns:
        dict: Repository activity data
    """
    # Example data - in a real implementation, this would get actual git data
    return {
        "repositories": ["let-her-cook"],
        "commits": 3,
        "files_changed": 5,
        "lines_added": 52,
        "lines_removed": 12
    }

def update_log_file(log_path, glyph_entry):
    """
    Update the JSON log file with a new glyph entry.
    
    Args:
        log_path (str): Path to the log file
        glyph_entry (dict): Glyph entry to add to the log
    """
    # Create an empty log list if the file doesn't exist or is empty
    if not os.path.exists(log_path) or os.path.getsize(log_path) == 0:
        log_data = []
    else:
        try:
            with open(log_path, 'r') as file:
                log_data = json.load(file)
        except json.JSONDecodeError:
            # If the file exists but isn't valid JSON, start with an empty list
            log_data = []
    
    # Add the new entry
    log_data.append(glyph_entry)
    
    # Write the updated log back to the file
    with open(log_path, 'w') as file:
        json.dump(log_data, file, indent=2)
    
    print(f"Updated log file at {log_path}")

def main():
    """
    Main function that runs the pulse tracker.
    """
    print("Starting Pulse Tracker...")
    
    # Get the path to the cook-log.json file
    log_path = os.path.join(project_root, "cook-log.json")
    print(f"Log file path: {log_path}")
    
    # Get repository activity
    repo_activity = get_repo_activity()
    print(f"Repository activity: {repo_activity}")
    
    # Build a glyph entry
    glyph_entry = build_glyph_entry(repo_activity)
    print(f"Generated glyph entry: {glyph_entry}")
    
    # Update the log file
    update_log_file(log_path, glyph_entry)
    
    print("Pulse Tracker completed successfully.")

if __name__ == "__main__":
    main()