#!/usr/bin/env bash
# SessionStart hook: Auto-Evolve Trigger
# Fires AFTER improvement-funnel.sh. Checks thresholds and nudges /evolve.
# Three triggers:
#   a) Any correction with times_corrected >= 3
#   b) Any violation recurring in 3+ distinct sessions
#   c) More than 10 sessions since last /evolve run

# Anchor to project root via script location — prevents CWD-dependent reads
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Profile: standard
source "$SCRIPT_DIR/lib/profile-check.sh" 2>/dev/null && require_profile standard

MEMORY_DIR="$PROJECT_ROOT/.claude/memory"
CORRECTIONS="$MEMORY_DIR/corrections.jsonl"
EVOLUTION_LOG="$MEMORY_DIR/evolution-log.md"
SESSIONS="$MEMORY_DIR/sessions.jsonl"

STOPA_MEMORY_DIR="$MEMORY_DIR" python3 -c "
import json, os, re, sys
from datetime import datetime

MEMORY = os.environ['STOPA_MEMORY_DIR']
reasons = []

# Check a: corrections with times_corrected >= 3
corrections_file = os.path.join(MEMORY, 'corrections.jsonl')
if os.path.isfile(corrections_file):
    with open(corrections_file, 'r', encoding='utf-8', errors='replace') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                if entry.get('times_corrected', 0) >= 3:
                    reasons.append(f'Correction repeated {entry[\"times_corrected\"]}×: \"{entry.get(\"summary\", \"\")[:60]}\"')
                    break  # One is enough to trigger
            except (json.JSONDecodeError, KeyError):
                continue

# Check b: violations in 3+ distinct recent days (last 7 days)
# Fix 2026-04-18: previous version counted raw occurrences (e.g. 21× same violation
# from one day = false '21 times' alarm). Now: key → set of unique YYYY-MM-DD dates,
# filtered to last 7 days so resolved violations age out naturally.
violations_file = os.path.join(MEMORY, 'violations.jsonl')
if os.path.isfile(violations_file):
    from datetime import timedelta
    cutoff = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    violation_days: dict[str, set[str]] = {}
    with open(violations_file, 'r', encoding='utf-8', errors='replace') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                date = entry.get('timestamp', '')[:10]
                if not date or date < cutoff:
                    continue
                key = f\"{entry.get('source', '')}:{entry.get('label', '')}\"
                violation_days.setdefault(key, set()).add(date)
            except (json.JSONDecodeError, KeyError):
                continue

    for key, days in violation_days.items():
        if len(days) >= 3:
            reasons.append(f'Violation recurring on {len(days)} distinct days (last 7d): {key}')
            break

# Check c: sessions since last /evolve
sessions_file = os.path.join(MEMORY, 'sessions.jsonl')
evolution_log = os.path.join(MEMORY, 'evolution-log.md')

session_count = 0
if os.path.isfile(sessions_file):
    with open(sessions_file, 'r', encoding='utf-8', errors='replace') as f:
        session_count = sum(1 for l in f if l.strip())

last_evolve = None
if os.path.isfile(evolution_log):
    with open(evolution_log, 'r', encoding='utf-8', errors='replace') as f:
        for line in f:
            m = re.search(r'(\d{4}-\d{2}-\d{2})', line)
            if m:
                last_evolve = m.group(1)

# Approximate: if no evolution log, treat all sessions as since-evolve
if last_evolve:
    # Count sessions after last evolve date
    after_count = 0
    if os.path.isfile(sessions_file):
        with open(sessions_file, 'r', encoding='utf-8', errors='replace') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    ts = entry.get('timestamp', '')[:10]
                    if ts > last_evolve:
                        after_count += 1
                except (json.JSONDecodeError, KeyError):
                    continue
    if after_count > 10:
        reasons.append(f'{after_count} sessions since last /evolve run ({last_evolve})')
elif session_count > 10:
    reasons.append(f'{session_count} sessions total, /evolve has never been run')

# Check d: learnings count exceeds threshold (compilation gap signal)
learnings_dir = os.path.join(MEMORY, 'learnings')
if os.path.isdir(learnings_dir):
    learning_files = [f for f in os.listdir(learnings_dir) if f.startswith('2') and f.endswith('.md')]
    if len(learning_files) > 70:
        reasons.append(f'{len(learning_files)} learnings in directory (threshold: 70) — graduation candidates likely')

# Check e: raw/ capture files accumulating without compile
raw_dir = os.path.join(MEMORY, 'raw')
if os.path.isdir(raw_dir):
    raw_files = [f for f in os.listdir(raw_dir) if f.endswith('.md') and not f.startswith('.')]
    if len(raw_files) > 100:
        reasons.append(f'{len(raw_files)} unprocessed raw captures — run /compile to synthesize')

if reasons:
    print('=== Auto-Evolve Trigger ===')
    for r in reasons:
        print(f'  • {r}')
    print('→ Threshold crossed. Run /evolve to analyze accumulated patterns and graduate rules.')
" 2>/dev/null

exit 0
