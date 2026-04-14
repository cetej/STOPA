#!/usr/bin/env bash
# Stop hook: capture session metadata to JSON for auto-scribe processing
# Pure bash, no LLM — must complete in <5s
# Output: none (writes to intermediate/session-summary.json)
# Windows-compatible: no grep -P, explicit defaults for all vars

# Skip for subagent Stop events (agent_type present = subagent)
HOOK_INPUT=$(cat 2>/dev/null || true)
echo "$HOOK_INPUT" | grep -q '"agent_type"' && exit 0

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
skills=$(count_matches "\| Skill[: ]" "$LOG")
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
  # Escape JSON special chars: backslash, double-quote, control chars
  escaped=$(printf '%s' "$line" | sed 's/\\/\\\\/g; s/"/\\"/g; s/\t/\\t/g')
  printf '"%s",' "$escaped"
done | sed 's/,$//')

# Skills — extract skill names from activity log (Skill:name format from fixed hook)
skill_names=$(grep -oE "Skill:[a-zA-Z_-]+" "$LOG" 2>/dev/null | sort -u | sed 's/Skill://' | while IFS= read -r name; do
  escaped=$(printf '%s' "$name" | sed 's/\\/\\\\/g; s/"/\\"/g')
  printf '"%s",' "$escaped"
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

# Count frustration signals this session (from sentiment field in corrections.jsonl)
frustrations_today=0
if [ -f "$CORRECTIONS_LOG" ]; then
  frustrations_today=$(grep -c '"sentiment":"frustrated"' "$CORRECTIONS_LOG" 2>/dev/null) || true
  frustrations_today="${frustrations_today:-0}"
fi

# Append session scorecard (keep only last 100 entries)
cat >> "$SESSIONS_LOG" <<EOF
{"timestamp":"$ts","activity":{"writes":$writes,"agents":$agents,"skills":$skills,"errors":$errors},"corrections_today":$corrections_today,"violations_today":$violations_today,"frustrations_today":$frustrations_today,"state":"$(echo "$state_snapshot" | sed 's/"/\\"/g' | head -c 100)"}
EOF

# Prune sessions.jsonl to last 100 entries
if [ -f "$SESSIONS_LOG" ]; then
  lines=$(wc -l < "$SESSIONS_LOG" 2>/dev/null) || true
  if [ "${lines:-0}" -gt 100 ]; then
    tail -100 "$SESSIONS_LOG" > "${SESSIONS_LOG}.tmp" && mv "${SESSIONS_LOG}.tmp" "$SESSIONS_LOG"
  fi
fi

# --- Auto-checkpoint: generate checkpoint.md from session data ---
# Only for non-trivial sessions (total >= 5 operations)
CHECKPOINT="$MEMORY_DIR/checkpoint.md"
if [ "$total" -ge 5 ]; then
  BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
  LAST_COMMIT_HASH=$(git log -1 --format="%h" 2>/dev/null || echo "unknown")
  LAST_COMMIT_MSG=$(git log -1 --format="%s" 2>/dev/null || echo "unknown")
  TODAY=$(date +"%Y-%m-%d")

  # Extract task goal from state.md
  task_goal="unknown"
  if [ -f "$STATE" ]; then
    task_goal=$(grep -A1 "^## Active Task" "$STATE" 2>/dev/null | tail -1 | sed 's/^\*\*Goal\*\*: *//')
    if [ -z "$task_goal" ] || echo "$task_goal" | grep -qi "no active task"; then
      # Fallback: use state_snapshot from earlier extraction
      task_goal="$state_snapshot"
    fi
  fi

  # Extract subtask table from state.md (done vs total)
  subtasks_done=0
  subtasks_total=0
  subtasks_remaining=""
  if [ -f "$STATE" ]; then
    subtasks_done=$(grep -cE "\| done" "$STATE" 2>/dev/null) || true
    subtasks_total=$(grep -cE "^\| [0-9]" "$STATE" 2>/dev/null) || true
    subtasks_done="${subtasks_done:-0}"
    subtasks_total="${subtasks_total:-0}"
    # Extract names of pending/in-progress subtasks
    subtasks_remaining=$(grep -E "^\| [0-9]" "$STATE" 2>/dev/null | grep -vE "\| done" | sed 's/^| [0-9]* | //' | sed 's/ |.*$//' | head -5 | while IFS= read -r line; do
      printf "  - %s\n" "$line"
    done)
  fi

  # Extract recent activity summary (last 20 unique tool types)
  activity_summary=""
  if [ -f "$LOG" ]; then
    activity_summary=$(tail -20 "$LOG" 2>/dev/null | grep -oE "\| (Write|Edit|Agent|Skill:[a-zA-Z_-]+|Bash) " | sort | uniq -c | sort -rn | head -5 | while IFS= read -r line; do
      printf "  - %s\n" "$(echo "$line" | sed 's/^ *//')"
    done)
  fi

  # Determine checkpoint status
  ckpt_status="auto-saved (session end)"
  if [ "$subtasks_total" -gt 0 ] && [ "$subtasks_done" -lt "$subtasks_total" ]; then
    ckpt_status="IN PROGRESS — $subtasks_done/$subtasks_total subtasks done"
  elif [ "$subtasks_total" -gt 0 ] && [ "$subtasks_done" -eq "$subtasks_total" ]; then
    ckpt_status="COMPLETE"
  fi

  # --- Files Touched (extract from activity-log) ---
  files_touched=""
  if [ -f "$LOG" ]; then
    # Extract unique filenames from Write/Edit lines that include basename
    files_touched=$(grep -E "\| (Write|Edit|MultiEdit) \| [^e]" "$LOG" 2>/dev/null | \
      sed -n 's/.*| \(Write\|Edit\|MultiEdit\) | \(.*\) | exit=.*/\2/p' | \
      sort | uniq -c | sort -rn | head -10 | while IFS= read -r line; do
        count=$(echo "$line" | sed 's/^ *//' | cut -d' ' -f1)
        fname=$(echo "$line" | sed 's/^ *[0-9]* //')
        printf "| %s | %s edits | %s |\n" "$fname" "$count" "$TODAY"
      done)
  fi

  # --- Key Results (recent git commits this session) ---
  key_results=""
  if [ -n "$first_ts" ]; then
    key_results=$(git log --oneline --since="$first_ts" 2>/dev/null | head -5 | while IFS= read -r line; do
      printf "- %s\n" "$line"
    done)
  fi

  # --- Enhanced checkpoint sections (CC Dream-inspired) ---

  # Errors & Corrections this session
  corrections_recent=""
  CORRECTIONS_LOG="$MEMORY_DIR/corrections.jsonl"
  if [ -f "$CORRECTIONS_LOG" ]; then
    corrections_recent=$(tail -5 "$CORRECTIONS_LOG" 2>/dev/null | python3 -c "
import sys,json
for line in sys.stdin:
    try:
        e=json.loads(line.strip())
        s=e.get('sentiment','')
        prefix='[frustration]' if s=='frustrated' else '[correction]'
        print('- ' + prefix + ' ' + e.get('summary','?')[:80])
    except: pass
" 2>/dev/null)
  fi

  # Learnings created this session
  learnings_today=""
  learnings_count=0
  if [ -d "$MEMORY_DIR/learnings" ]; then
    learnings_count=$(ls "$MEMORY_DIR/learnings/" 2>/dev/null | grep -c "^${TODAY}" 2>/dev/null) || true
    learnings_count="${learnings_count:-0}"
    learnings_today=$(ls "$MEMORY_DIR/learnings/" 2>/dev/null | grep "^${TODAY}" | head -5 | while IFS= read -r f; do
      printf "  - %s\n" "${f%.md}"
    done)
  fi

  # Most recent decision
  recent_decision="none"
  DECISIONS="$MEMORY_DIR/decisions.md"
  if [ -f "$DECISIONS" ]; then
    recent_decision=$(grep "^### " "$DECISIONS" 2>/dev/null | tail -1 | sed 's/^### //') || true
    recent_decision="${recent_decision:-none}"
  fi

  # Build resume prompt: what was done + what remains
  resume_what_done="Session: $writes file edits, $agents agent spawns, $skills skill calls"
  if [ -n "$skill_names" ]; then
    resume_skills=$(echo "$skill_names" | sed 's/"//g; s/,/, /g')
    resume_what_done="$resume_what_done. Skills: $resume_skills"
  fi

  # Write checkpoint atomically
  cat > "${CHECKPOINT}.tmp" <<CKPT
# Session Checkpoint

**Saved**: $TODAY ($ckpt_status)
**Task**: $(echo "$task_goal" | sed 's/"/\\"/g' | head -c 200)
**Branch**: $BRANCH
**Last commit**: \`$LAST_COMMIT_HASH\` $LAST_COMMIT_MSG

---

## Session Activity

$resume_what_done
Duration: ~${duration_min} min

## Files Touched

$(if [ -n "$files_touched" ]; then printf "| File | Operations | Date |\n|------|-----------|------|\n%s\n" "$files_touched"; else echo "_No file edits tracked_"; fi)

## Key Results

$(if [ -n "$key_results" ]; then echo "$key_results"; else echo "_No commits this session_"; fi)

## Errors & Corrections

$(if [ -n "$corrections_recent" ]; then echo "$corrections_recent"; else echo "_No corrections logged this session_"; fi)

## Learnings Captured

learnings_this_session: $learnings_count
$(if [ -n "$learnings_today" ]; then echo "$learnings_today"; else echo "_No new learnings files created_"; fi)

## Workflow Decisions

Most recent: $recent_decision
_(Full trail: .claude/memory/decisions.md)_

## What Remains

$(if [ -n "$subtasks_remaining" ]; then echo "Pending subtasks:"; echo "$subtasks_remaining"; else echo "_No pending subtasks detected in state.md_"; fi)

---

## Resume Prompt

> **Task**: $(echo "$task_goal" | head -c 200)
>
> **Context**: Last commit \`$LAST_COMMIT_HASH\` ($LAST_COMMIT_MSG). Branch: $BRANCH.
> Session had $writes edits, $agents agents, $skills skill calls, $errors errors.
$(if [ "$subtasks_total" -gt 0 ] && [ "$subtasks_done" -lt "$subtasks_total" ]; then echo "> **Remaining**: $((subtasks_total - subtasks_done)) subtasks pending — check state.md for details."; fi)
$(if [ "$errors" -gt 0 ]; then echo "> **Errors detected**: $errors — review before continuing."; fi)
CKPT

  mv "${CHECKPOINT}.tmp" "$CHECKPOINT" 2>/dev/null
fi

exit 0
