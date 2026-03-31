#!/usr/bin/env bash
# SessionStart hook: Unified Improvement Funnel
# Aggregates corrections.jsonl, violations.jsonl, sessions.jsonl into
# .claude/memory/improvement-queue.md — a priority-sorted failure collection point.
# Injects top items into Claude context as "Improvement Opportunities".

# Profile: standard
source .claude/hooks/lib/profile-check.sh 2>/dev/null && require_profile standard

MEMORY_DIR=".claude/memory"
CORRECTIONS="$MEMORY_DIR/corrections.jsonl"
VIOLATIONS="$MEMORY_DIR/violations.jsonl"
SESSIONS="$MEMORY_DIR/sessions.jsonl"
QUEUE="$MEMORY_DIR/improvement-queue.md"

# Check if any signal files exist
HAS_DATA=false
[ -f "$CORRECTIONS" ] && HAS_DATA=true
[ -f "$VIOLATIONS" ] && HAS_DATA=true
[ -f "$SESSIONS" ] && HAS_DATA=true

if [ "$HAS_DATA" = false ]; then
    exit 0
fi

# Generate queue via Python — handles JSON parsing and priority scoring
python3 -c "
import json, sys, os
from datetime import datetime, timedelta
from collections import Counter

MEMORY = '.claude/memory'
now = datetime.now()
week_ago = now - timedelta(days=7)

items = []  # [{priority, type, pattern, count, source, action}]

# 1. Corrections — group by summary keywords, weight = 2
corrections_file = os.path.join(MEMORY, 'corrections.jsonl')
if os.path.isfile(corrections_file):
    with open(corrections_file, 'r', encoding='utf-8', errors='replace') as f:
        corrections = [json.loads(l) for l in f if l.strip()]

    # Group by summary (rough dedup via first 50 chars)
    groups = Counter()
    latest = {}
    for c in corrections:
        key = c.get('summary', '')[:50].lower().strip()
        if len(key) < 5:
            continue
        groups[key] += 1
        latest[key] = c

    for key, count in groups.most_common(10):
        if count >= 2:
            c = latest[key]
            items.append({
                'priority': count * 2,
                'type': 'correction',
                'pattern': c.get('summary', key)[:80],
                'count': count,
                'source': 'corrections.jsonl',
                'action': '/evolve' if count >= 3 else '/scribe'
            })

# 2. Violations — each is unique, weight = 3
violations_file = os.path.join(MEMORY, 'violations.jsonl')
if os.path.isfile(violations_file):
    with open(violations_file, 'r', encoding='utf-8', errors='replace') as f:
        violations = [json.loads(l) for l in f if l.strip()]

    # Group by source+label
    groups = Counter()
    latest = {}
    for v in violations:
        key = f\"{v.get('source', '')}:{v.get('label', '')}\"
        groups[key] += 1
        latest[key] = v

    for key, count in groups.most_common(10):
        v = latest[key]
        items.append({
            'priority': count * 3,
            'type': 'violation',
            'pattern': v.get('label', key)[:80],
            'count': count,
            'source': v.get('source', 'violations.jsonl'),
            'action': '/evolve --escalate' if count >= 3 else 'fix rule or code'
        })

# 3. Session regression — rising correction rate, weight = 1
sessions_file = os.path.join(MEMORY, 'sessions.jsonl')
if os.path.isfile(sessions_file):
    with open(sessions_file, 'r', encoding='utf-8', errors='replace') as f:
        sessions = [json.loads(l) for l in f if l.strip()]

    if len(sessions) >= 5:
        last5 = sessions[-5:]
        prev5 = sessions[-10:-5] if len(sessions) >= 10 else sessions[:max(1, len(sessions)-5)]

        avg_corr_last = sum(s.get('corrections_today', 0) for s in last5) / len(last5)
        avg_corr_prev = sum(s.get('corrections_today', 0) for s in prev5) / max(len(prev5), 1)

        if avg_corr_last > avg_corr_prev + 0.5:
            items.append({
                'priority': 4,
                'type': 'regression',
                'pattern': f'Correction rate rising: {avg_corr_prev:.1f} -> {avg_corr_last:.1f}/session',
                'count': int(avg_corr_last * 5),
                'source': 'sessions.jsonl',
                'action': '/evolve'
            })

# Sort by priority desc
items.sort(key=lambda x: x['priority'], reverse=True)

# Write improvement-queue.md
queue_path = os.path.join(MEMORY, 'improvement-queue.md')
with open(queue_path, 'w', encoding='utf-8') as f:
    f.write(f'# Improvement Queue\\n\\n')
    f.write(f'Generated: {now.strftime(\"%Y-%m-%d %H:%M\")}\\n\\n')
    if not items:
        f.write('No improvement items found. System is clean.\\n')
    else:
        f.write('| Priority | Type | Pattern | Count | Action |\\n')
        f.write('|----------|------|---------|-------|--------|\\n')
        for item in items[:15]:
            f.write(f'| {item[\"priority\"]} | {item[\"type\"]} | {item[\"pattern\"]} | {item[\"count\"]} | {item[\"action\"]} |\\n')

# Output top 5 to Claude context
top = items[:5]
if top:
    print(f'=== Improvement Opportunities ({len(items)} total) ===')
    for i, item in enumerate(top, 1):
        flag = ' ⚠' if item['priority'] >= 6 else ''
        print(f'{i}. [{item[\"type\"].upper()}] {item[\"pattern\"]} (×{item[\"count\"]}){flag} → {item[\"action\"]}')

    urgent = [i for i in items if i['priority'] >= 6]
    if urgent:
        print(f'\\n→ {len(urgent)} item(s) at priority ≥6. Run /evolve to address recurring patterns.')
" 2>/dev/null

exit 0
