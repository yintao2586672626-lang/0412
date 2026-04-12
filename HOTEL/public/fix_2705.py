import sys
filepath = r'd:/桌面/国际/JD-main/HOTEL/public/index.html'

f = open(filepath, encoding='utf-8')
lines = f.readlines()
f.close()

print(f"Total lines before: {len(lines)}")

# Fix line 2705 (index 2705): truncate at '}}</div>'
line = lines[2705]
pos = line.find('}}</div>')
if pos >= 0:
    lines[2705] = line[:pos + len('}}</div>')].rstrip() + '\n'
    print("Fixed line 2706 - truncated garbage")

print("\nLines to delete (indices 2707-2710):")
for i in [2707, 2708, 2709, 2710]:
    print(f"  {i+1}: {lines[i].strip()[:80]}")

# Remove the duplicate block (indices 2707-2710)
new_lines = lines[:2707] + lines[2711:]
print(f"\nTotal lines after: {len(new_lines)} (removed {len(lines) - len(new_lines)})")

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

# Verify
f = open(filepath, encoding='utf-8')
vlines = f.readlines()
f.close()
print("\nVerification - lines around fix:")
for i in range(2702, min(2715, len(vlines))):
    print(f"  {i+1}: {vlines[i].strip()[:100]}")
