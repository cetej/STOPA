#!/usr/bin/env bash
# PostToolUse hook (matcher: Write|Edit): Suggest checkpoint when task is 70%+ complete
# Advisory only — debounced to max 1 suggestion per 30 minutes.

STATE_FILE=".claude/memory/state.md"
CHECKPOINT_FILE=".claude/memory/checkpoint.md"
MARKER="/tmp/stopa-checkpoint-suggested"

# Skip if no state file
[ ! -f "$STATE_FILE" ] && exit 0

# Debounce: skip if suggested in last 30 minutes
if [ -f "$MARKER" ]; then
  MARKER_AGE=$(( $(date +%s) - $(stat -c %Y "$MARKER" 2>/dev/null || echo 0) ))
  [ "$MARKER_AGE" -lt 1800 ] && exit 0
fi

# Parse state.md for subtask completion
# Look for patterns like: [x] done, [X] done, ✅ done, DONE, completed
TOTAL=$(grep -cE '^\s*[-*]\s*\[.\]|^\s*[-*].*\|.*\|' "$STATE_FILE" 2>/dev/null || echo 0)
DONE=$(grep -ciE '^\s*[-*]\s*\[x\]|^\s*[-*].*completed|^\s*[-*].*DONE|^\s*[-*].*✅' "$STATE_FILE" 2>/dev/null || echo 0)

# Need at least 3 tasks to trigger, and 70%+ completion
[ "$TOTAL" -lt 3 ] && exit 0
RATIO=$((DONE * 100 / TOTAL))
[ "$RATIO" -lt 70 ] && exit 0

# Check if checkpoint already saved recently (last 30 min)
if [ -f "$CHECKPOINT_FILE" ]; then
  CP_AGE=$(( $(date +%s) - $(stat -c %Y "$CHECKPOINT_FILE" 2>/dev/null || echo 0) ))
  [ "$CP_AGE" -lt 1800 ] && exit 0
fi

# Mark suggestion time
touch "$MARKER" 2>/dev/null

cat <<EOF
{"additionalContext": "💾 Task is ${RATIO}% complete (${DONE}/${TOTAL} subtasks done). Consider saving progress with /checkpoint save to prevent work loss."}
EOF
