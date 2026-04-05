#!/bin/bash
# Compound loop trigger — suggest /compile when new learnings accumulate
# Runs at Stop hook. Compares current learnings count to last compile state.

COMPILE_STATE=".claude/memory/wiki/.compile-state.json"
LEARNINGS_DIR=".claude/memory/learnings"
RAW_DIR=".claude/memory/raw"

# Count current learnings
CURRENT_COUNT=$(find "$LEARNINGS_DIR" -name "2*.md" 2>/dev/null | wc -l)

# Count raw agent outputs
RAW_COUNT=0
if [ -d "$RAW_DIR" ]; then
  RAW_COUNT=$(find "$RAW_DIR" -name "*.md" ! -name ".gitkeep" 2>/dev/null | wc -l)
fi

# Get last compile count
LAST_COUNT=0
if [ -f "$COMPILE_STATE" ]; then
  LAST_COUNT=$(python -c "import json; print(json.load(open('$COMPILE_STATE')).get('total_learnings', 0))" 2>/dev/null || echo "0")
fi

NEW_LEARNINGS=$((CURRENT_COUNT - LAST_COUNT))

# Check per-component wiki staleness (wiki-pending.json from auto-relate.py)
WIKI_PENDING=".claude/memory/intermediate/wiki-pending.json"
STALE_COMPONENTS=""
if [ -f "$WIKI_PENDING" ]; then
  STALE_COMPONENTS=$(python -c "
import json
try:
    pending = json.load(open('$WIKI_PENDING'))
    stale = [f'  {comp}: {count} new' for comp, count in pending.items() if count >= 2]
    if stale: print('\n'.join(stale))
except: pass
" 2>/dev/null)
fi

# Trigger suggestion if 3+ new learnings (lowered from 5) or 3+ raw files or stale components
if [ "$NEW_LEARNINGS" -ge 3 ] || [ "$RAW_COUNT" -ge 3 ] || [ -n "$STALE_COMPONENTS" ]; then
  echo "=== Compound Loop Trigger ==="
  echo "New learnings since last compile: $NEW_LEARNINGS"
  echo "Raw agent outputs pending: $RAW_COUNT"
  if [ -n "$STALE_COMPONENTS" ]; then
    echo "Wiki articles with pending learnings:"
    echo "$STALE_COMPONENTS"
  fi
  echo "Suggestion: run /compile --incremental to update wiki and briefings"
  echo "==========================="
fi
