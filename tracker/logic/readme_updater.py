"""
README Updater Module

This script updates the README.md file with the latest glyph data
from cook-log.json. This ensures the README always shows the current state
without requiring JavaScript.
"""

import os
import sys
import json
import re
import datetime
from pathlib import Path

# Ensure the project root is in the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def format_glyphs_for_display(glyphs, width=15):
    """
    Format glyphs into a multi-line display with fixed width.
    
    Args:
        glyphs (str): String of glyphs
        width (int): Width of each line in characters
    
    Returns:
        str: Formatted multi-line string
    """
    # If glyphs is too short, repeat it to make it more visually interesting
    if len(glyphs) < 30:
        glyphs = glyphs * (30 // len(glyphs) + 1)
    
    # Break into lines of specified width
    lines = []
    for i in range(0, len(glyphs), width):
        lines.append(glyphs[i:i+width])
    
    return '\n'.join(lines)

def update_readme_with_glyphs(log_path, readme_path):
    """
    Update the README file with the latest glyph data.
    
    Args:
        log_path (str): Path to the cook-log.json file
        readme_path (str): Path to the README.md file
    """
    try:
        # Check if the files exist
        if not os.path.exists(log_path):
            print(f"Error: Log file {log_path} does not exist.")
            return
        
        if not os.path.exists(readme_path):
            print(f"Error: README file {readme_path} does not exist.")
            return
        
        # Read the log data
        with open(log_path, 'r') as file:
            try:
                log_data = json.load(file)
                if not log_data:
                    print("Log file is empty. No updates to make.")
                    return
            except json.JSONDecodeError:
                print("Error: Log file contains invalid JSON.")
                return
        
        # Sort by timestamp to get the most recent entry
        sorted_data = sorted(log_data, key=lambda x: x.get('timestamp', ''), reverse=True)
        latest_entry = sorted_data[0] if sorted_data else None
        
        if not latest_entry:
            print("No entries found in log file.")
            return
        
        # Read the README
        with open(readme_path, 'r') as file:
            readme_content = file.read()
        
        # Format the latest glyphs for display
        glyphs_display = format_glyphs_for_display(latest_entry.get('glyphs', ''))
        
        # Get the timestamp in a readable format
        try:
            timestamp = datetime.datetime.fromisoformat(latest_entry.get('timestamp', '')).strftime('%Y-%m-%d %H:%M:%S UTC')
        except (ValueError, TypeError):
            timestamp = latest_entry.get('timestamp', 'Unknown')
        
        # Extract metadata
        meta = latest_entry.get('meta', {})
        resonance = meta.get('resonance', 'Unknown')
        cycle = meta.get('cycle', '?')
        pattern = meta.get('pattern', 'Unknown')
        
        # Update the glyphs section in the README
        glyph_section_pattern = r'```\n(.*?)\n```'
        if re.search(glyph_section_pattern, readme_content, re.DOTALL):
            updated_readme = re.sub(
                glyph_section_pattern, 
                f'```\n{glyphs_display}\n```', 
                readme_content, 
                count=1, 
                flags=re.DOTALL
            )
        else:
            print("Warning: Could not find the code block for glyphs in README.")
            updated_readme = readme_content
        
        # Update the metadata in the README
        timestamp_pattern = r'\*\*Timestamp\*\*: \[(.*?)\]'
        resonance_pattern = r'\*\*Resonance\*\*: \[(.*?)\]'
        cycle_pattern = r'\*\*Cycle\*\*: \[(.*?)\]'
        pattern_pattern = r'\*\*Pattern\*\*: \[(.*?)\]'
        
        updated_readme = re.sub(timestamp_pattern, f'**Timestamp**: [{timestamp}]', updated_readme)
        updated_readme = re.sub(resonance_pattern, f'**Resonance**: [{resonance}]', updated_readme)
        updated_readme = re.sub(cycle_pattern, f'**Cycle**: [{cycle}]', updated_readme)
        updated_readme = re.sub(pattern_pattern, f'**Pattern**: [{pattern}]', updated_readme)
        
        # Write the updated README
        with open(readme_path, 'w') as file:
            file.write(updated_readme)
        
        print(f"README updated with latest glyphs from {timestamp}")
        
    except Exception as e:
        print(f"Error updating README: {e}")

def main():
    """
    Main function to run the README updater.
    """
    print("Starting README updater...")
    
    # Get paths
    log_path = os.path.join(project_root, "cook-log.json")
    readme_path = os.path.join(project_root, "README.md")
    
    print(f"Log file path: {log_path}")
    print(f"README file path: {readme_path}")
    
    # Update the README
    update_readme_with_glyphs(log_path, readme_path)
    
    print("README updater completed.")

if __name__ == "__main__":
    main()