#!/usr/bin/env python3
"""Remove leftover inline JS content from index.html"""
import os, re

INDEX_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index.html')

with open(INDEX_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# Find and remove the orphaned JS code (between the script src line and </body>)
# The pattern: everything from "\n\n    const API_BASE" up to ".mount('#app');\n"
pattern = r'\n\s*const API_BASE.*?\.mount\(\'#app\'\);'

match = re.search(pattern, content, re.DOTALL)
if match:
    new_content = content[:match.start()] + content[match.end():]
    
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    orig_size = len(content.encode('utf-8')) / 1024
    new_size = len(new_content.encode('utf-8')) / 1024
    print(f"SUCCESS: {orig_size:.1f} KB -> {new_size:.1f} KB (removed {orig_size-new_size:.1f} KB)")
else:
    print("Pattern not found - trying alternative...")
    # Try finding just the createApp block
    pattern2 = r'\n\s*createApp\(\{[^}]*\}\)\.mount\(\'#app\'\);'
    match2 = re.search(pattern2, content)
    if match2:
        print(f"Found mount at position {match2.start()}")
    else:
        print("Still not found. Checking file structure around line 9730...")
        lines = content.split('\n')
        for i in range(9728, min(9750, len(lines))):
            print(f"{i+1}: {lines[i][:80]}")
