"""Add <!-- CACHE_BOUNDARY --> marker to all skill files in commands/."""
import re
import os
import glob

COMMANDS_DIR = os.path.join(os.path.dirname(__file__), '..', '.claude', 'commands')
MARKER = '<!-- CACHE_BOUNDARY -->'

# Dynamic section indicators - first match gets the marker placed BEFORE it
DYNAMIC_PATTERNS = [
    r'^## Phase \d',
    r'^## Step \d',
    r'^## Parse Arg',
    r'^## Input$',
    r'^## Process$',
    r'^## Operations$',
]

files = sorted(glob.glob(os.path.join(COMMANDS_DIR, '*.md')))
results = []

for fpath in files:
    with open(fpath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Skip if already has marker
    if any(MARKER in l for l in lines):
        results.append(f'SKIP (already has marker): {os.path.basename(fpath)}')
        continue

    # Find end of frontmatter (second ---)
    fm_end = None
    dash_count = 0
    for i, line in enumerate(lines):
        if line.strip() == '---':
            dash_count += 1
            if dash_count == 2:
                fm_end = i
                break

    if fm_end is None:
        results.append(f'ERROR (no frontmatter): {os.path.basename(fpath)}')
        continue

    # Find first dynamic section after frontmatter
    insert_line = None
    for i in range(fm_end + 1, len(lines)):
        for pat in DYNAMIC_PATTERNS:
            if re.match(pat, lines[i]):
                insert_line = i
                break
        if insert_line is not None:
            break

    if insert_line is None:
        # Fallback: find the SECOND ## heading after frontmatter
        # (first is usually the title/role description section)
        h2_count = 0
        for i in range(fm_end + 1, len(lines)):
            if re.match(r'^## ', lines[i]):
                h2_count += 1
                if h2_count == 2:
                    insert_line = i
                    break

    if insert_line is None:
        results.append(f'MANUAL: {os.path.basename(fpath)} (no dynamic pattern found)')
        continue

    # Insert marker before the dynamic section
    lines.insert(insert_line, MARKER + '\n\n')

    with open(fpath, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    results.append(
        f'OK line {insert_line}: {os.path.basename(fpath)}'
        f' -> before "{lines[insert_line + 1].strip()[:50]}"'
    )

for r in results:
    print(r)
print(f'\nTotal: {len(files)} files')
