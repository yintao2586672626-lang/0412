#!/usr/bin/env python3
"""Extract inline JS from index.html to app-main.js"""
import os, re

INDEX_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index.html')
OUTPUT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app-main.js')

with open(INDEX_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract the script block that starts with "const { createApp" and ends with ".mount('#app');"
pattern = r'<script>\s*(const \{ createApp.*?\.mount\(\'#app\'\);)\s*</script>'
match = re.search(pattern, content, re.DOTALL)

if match:
    js_content = match.group(1)
    
    # Add header comment
    js_output = """/* app-main.js - Auto-extracted from index.html */
/* Generated for performance optimization */
/* Contains: Vue app setup, components, all business logic */

"""
    js_output += js_content + "\n"
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(js_output)
    
    size_kb = len(js_content.encode('utf-8')) / 1024
    print(f"Extracted JS: {OUTPUT_FILE}")
    print(f"Size: {size_kb:.1f} KB")
    print(f"Lines: {js_content.count(chr(10))}")
else:
    print("ERROR: Could not find the main script block in index.html")
