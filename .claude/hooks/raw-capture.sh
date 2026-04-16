#!/usr/bin/env bash
# Stop hook: capture session data to raw/ landing zone for /compile processing
# Karpathy-inspired: immutable raw/ folder, append-only, timestamped
# /compile Phase 1.2 already knows to Glob raw/*.md — this populates it
#
# Output: none (writes to .claude/memory/raw/)

# Skip subagent Stop events
HOOK_INPUT=$(cat 2>/dev/null || true)
echo "$HOOK_INPUT" | grep -q '"agent_type"' && exit 0

# Anchor to project root via script location — prevents CWD-dependent writes
# (previous bug: hook ran from .claude/memory/learnings/ → created nested anomaly tree)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
MEMORY_DIR="$PROJECT_ROOT/.claude/memory"
RAW_DIR="$MEMORY_DIR/raw"
LOG="$MEMORY_DIR/activity-log.md"
STATE="$MEMORY_DIR/state.md"
CHECKPOINT="$MEMORY_DIR/checkpoint.md"
NEWS="$MEMORY_DIR/news.md"

# Ensure raw dir exists
mkdir -p "$RAW_DIR/processed" 2>/dev/null

# Skip if no activity log
[ ! -f "$LOG" ] && exit 0

# Count significant operations
count_matches() {
  local result
  result=$(grep -cE "$1" "$2" 2>/dev/null) || true
  echo "${result:-0}"
}

writes=$(count_matches "\| (Write|Edit|MultiEdit) \|" "$LOG")
agents=$(count_matches "\| Agent " "$LOG")
skills=$(count_matches "\| Skill \|" "$LOG")
total=$((writes + agents + skills))

# Only capture non-trivial sessions (3+ significant ops)
[ "$total" -lt 3 ] && exit 0

TODAY=$(date +"%Y-%m-%d")
TIMESTAMP=$(date +"%Y-%m-%dT%H:%M:%S")

# Build slug from task goal
slug="session"
if [ -f "$STATE" ]; then
  task=$(grep -A1 "^## Active Task" "$STATE" 2>/dev/null | tail -1 | sed 's/^\*\*Goal\*\*: *//')
  if [ -n "$task" ] && ! echo "$task" | grep -qi "no active task"; then
    # Convert task to kebab-case slug (first 40 chars)
    slug=$(echo "$task" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-//;s/-$//' | head -c 40)
    slug="${slug:-session}"
  fi
fi

OUTFILE="$RAW_DIR/${TODAY}-${slug}.md"

# Don't overwrite — append sequence number if exists
if [ -f "$OUTFILE" ]; then
  seq=2
  while [ -f "$RAW_DIR/${TODAY}-${slug}-${seq}.md" ]; do
    seq=$((seq + 1))
  done
  OUTFILE="$RAW_DIR/${TODAY}-${slug}-${seq}.md"
fi

# Extract skill names
skill_names=$(grep -oE "Skill:[a-zA-Z_-]+" "$LOG" 2>/dev/null | sort -u | sed 's/Skill://' | tr '\n' ', ' | sed 's/,$//')

# Extract files touched (top 15)
files_touched=$(grep -E "\| (Write|Edit|MultiEdit) \| [^e]" "$LOG" 2>/dev/null | \
  sed -n 's/.*| \(Write\|Edit\|MultiEdit\) | \(.*\) | exit=.*/\2/p' | \
  sort | uniq -c | sort -rn | head -15 | while IFS= read -r line; do
    fname=$(echo "$line" | sed 's/^ *[0-9]* //')
    count=$(echo "$line" | sed 's/^ *//' | cut -d' ' -f1)
    printf "- %s (%s edits)\n" "$fname" "$count"
  done)

# Extract agent outputs from log (sub-agent completions)
agent_outputs=$(grep -E "\| Agent " "$LOG" 2>/dev/null | head -10 | while IFS= read -r line; do
    printf "- %s\n" "$line"
  done)

# Recent commits this session
first_ts=$(grep "^- " "$LOG" 2>/dev/null | head -1 | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}')
commits=""
if [ -n "$first_ts" ]; then
  commits=$(git log --oneline --since="$first_ts" 2>/dev/null | head -10 | while IFS= read -r line; do
    printf "- %s\n" "$line"
  done)
fi

# Task state snapshot
task_state="_No active task_"
if [ -f "$STATE" ]; then
  task_goal=$(grep -A1 "^## Active Task" "$STATE" 2>/dev/null | tail -1 | sed 's/^\*\*Goal\*\*: *//')
  if [ -n "$task_goal" ] && ! echo "$task_goal" | grep -qi "no active task"; then
    done_count=$(count_matches "\| done" "$STATE")
    total_count=$(count_matches "^\| [0-9]" "$STATE")
    task_state="$task_goal ($done_count/$total_count subtasks)"
  fi
fi

# Write raw capture file
cat > "$OUTFILE" <<RAW
---
date: $TODAY
timestamp: $TIMESTAMP
type: session-capture
writes: $writes
agents: $agents
skills_count: $skills
---

# Raw Session Capture: $TODAY

**Task**: $task_state
**Skills**: ${skill_names:-none}
**Activity**: $writes writes, $agents agents, $skills skill calls

## Files Touched

${files_touched:-_No file edits_}

## Agent Activity

${agent_outputs:-_No agent spawns_}

## Commits

${commits:-_No commits_}

## Key Decisions & Outputs

_(Auto-captured from session. /compile will synthesize into wiki articles.)_
RAW

exit 0
