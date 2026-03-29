#!/usr/bin/env bash
# Stop hook: capture session metadata to JSON for auto-scribe processing
# Pure bash, no LLM — must complete in <5s
# Output: none (writes to intermediate/session-summary.json)
# Windows-compatible: no grep -P, explicit defaults for all vars

MEMORY_DIR=".claude/memory"
LOG="$MEMORY_DIR/activity-log.md"
STATE="$MEMORY_DIR/state.md"
OUTPUT="$MEMORY_DIR/intermediate/session-summary.json"

# Ensure intermediate dir exists
mkdir -p "$MEMORY_DIR/intermediate" 2>/dev/null

# If no activity log, nothing to summarize
if [ ! -f "$LOG" ]; then
  exit 0
fi

# Count activity types (grep -c returns 1 on no match, so use || true and default)
count_matches() {
  local pattern="$1"
  local file="$2"
  local result
  result=$(grep -cE "$pattern" "$file" 2>/dev/null) || true
  echo "${result:-0}"
}

writes=$(count_matches "\| (Write|Edit|MultiEdit) \|" "$LOG")
agents=$(count_matches "\| Agent " "$LOG")
skills=$(count_matches "\| Skill \|" "$LOG")
bash_sig=$(count_matches "\| Bash \(significant\) \|" "$LOG")
errors=$(count_matches "exit=[^0]" "$LOG")
total=$((writes + agents + skills + bash_sig))

# Skip trivial sessions (< 2 significant operations)
# Lowered from 3 to 2 to bootstrap the auto-scribe pipeline
if [ "$total" -lt 2 ]; then
  exit 0
fi

# Extract error lines as JSON array items
error_lines=$(grep "exit=[^0]" "$LOG" 2>/dev/null | head -5 | sed 's/^- //' | while IFS= read -r line; do
  printf '"%s",' "$line"
done | sed 's/,$//')

# Skills — extract skill names from activity log (Skill:name format from fixed hook)
skill_names=$(grep -oE "Skill:[a-zA-Z_-]+" "$LOG" 2>/dev/null | sort -u | sed 's/Skill://' | while IFS= read -r name; do
  printf '"%s",' "$name"
done | sed 's/,$//')
skill_names="${skill_names:-}"

# State snapshot (one-liner)
state_snapshot="none"
if [ -f "$STATE" ]; then
  task=$(grep -A1 "^## Active Task\|^## Current Task" "$STATE" 2>/dev/null | tail -1 | sed 's/^\*\*Goal\*\*: *//')
  if [ -n "$task" ] && ! echo "$task" | grep -qi "no active task"; then
    done_count=$(count_matches "\| done" "$STATE")
    total_count=$(count_matches "^| [0-9]" "$STATE")
    state_snapshot="$task | $done_count/$total_count done"
  fi
fi

# Timestamp
ts=$(date +"%Y-%m-%dT%H:%M:%S")

# Duration approximation (first and last entry timestamps)
# Use grep -oE instead of -oP for Windows compatibility
first_ts=$(grep "^- " "$LOG" 2>/dev/null | head -1 | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}')
last_ts=$(grep "^- " "$LOG" 2>/dev/null | tail -1 | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}')
duration_min=0
if [ -n "$first_ts" ] && [ -n "$last_ts" ]; then
  first_epoch=$(date -d "$first_ts" +%s 2>/dev/null || echo 0)
  last_epoch=$(date -d "$last_ts" +%s 2>/dev/null || echo 0)
  if [ "$first_epoch" -gt 0 ] && [ "$last_epoch" -gt 0 ]; then
    duration_min=$(( (last_epoch - first_epoch) / 60 ))
  fi
fi

# Write JSON atomically (write to .tmp then rename)
cat > "${OUTPUT}.tmp" <<EOF
{
  "timestamp": "$ts",
  "duration_approx_min": $duration_min,
  "activity": {
    "writes": $writes,
    "agents": $agents,
    "skills": $skills,
    "bash_sig": $bash_sig,
    "errors": $errors,
    "total": $total
  },
  "skills_invoked": [${skill_names}],
  "errors_detail": [${error_lines}],
  "state_snapshot": "$(echo "$state_snapshot" | sed 's/"/\\"/g')"
}
EOF

mv "${OUTPUT}.tmp" "$OUTPUT" 2>/dev/null

# --- Append to persistent sessions.jsonl scorecard ---
SESSIONS_LOG="$MEMORY_DIR/sessions.jsonl"
CORRECTIONS_LOG="$MEMORY_DIR/corrections.jsonl"
VIOLATIONS_LOG="$MEMORY_DIR/violations.jsonl"

# Count corrections logged this session (entries within last ~2 hours by timestamp prefix)
TODAY=$(date +"%Y-%m-%dT")
corrections_today=0
if [ -f "$CORRECTIONS_LOG" ]; then
  corrections_today=$(grep -c "\"timestamp\":\"$TODAY" "$CORRECTIONS_LOG" 2>/dev/null) || true
  corrections_today="${corrections_today:-0}"
fi

# Count violations caught this session
violations_today=0
if [ -f "$VIOLATIONS_LOG" ]; then
  violations_today=$(grep -c "\"timestamp\":\"$TODAY" "$VIOLATIONS_LOG" 2>/dev/null) || true
  violations_today="${violations_today:-0}"
fi

# Append session scorecard (keep only last 100 entries)
cat >> "$SESSIONS_LOG" <<EOF
{"timestamp":"$ts","activity":{"writes":$writes,"agents":$agents,"skills":$skills,"errors":$errors},"corrections_today":$corrections_today,"violations_today":$violations_today,"state":"$(echo "$state_snapshot" | sed 's/"/\\"/g' | head -c 100)"}
EOF

# Prune sessions.jsonl to last 100 entries
if [ -f "$SESSIONS_LOG" ]; then
  lines=$(wc -l < "$SESSIONS_LOG" 2>/dev/null) || true
  if [ "${lines:-0}" -gt 100 ]; then
    tail -100 "$SESSIONS_LOG" > "${SESSIONS_LOG}.tmp" && mv "${SESSIONS_LOG}.tmp" "$SESSIONS_LOG"
  fi
fi

exit 0
