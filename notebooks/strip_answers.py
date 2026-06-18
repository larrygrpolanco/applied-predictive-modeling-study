#!/usr/bin/env python3
"""Strip executable code from notebook cells, keeping only comments/TODOs."""
import json, sys

for fname in sys.argv[1:]:
    with open(fname) as f:
        nb = json.load(f)
    
    for cell in nb['cells']:
        if cell['cell_type'] != 'code':
            continue
        if not cell['source']:
            continue
        
        lines = cell['source'] if isinstance(cell['source'], list) else cell['source'].splitlines(True)
        new_lines = []
        for line in lines:
            stripped = line.lstrip()
            # Keep comments, blank lines, and shell commands (starting with !)
            if stripped.startswith('#') or stripped.startswith('!') or stripped.strip() == '':
                new_lines.append(line)
            # Strip everything else (executable code)
        
        cell['source'] = new_lines
    
    with open(fname, 'w') as f:
        json.dump(nb, f, indent=1)
    
    # Count what we kept
    total_original = sum(len(c['source']) for c in nb['cells'] if c['cell_type'] == 'code')
    print(f"✓ {fname} — kept {total_original} comment/shell lines across {sum(1 for c in nb['cells'] if c['cell_type'] == 'code')} code cells")
