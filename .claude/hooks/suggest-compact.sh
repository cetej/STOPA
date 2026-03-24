#!/usr/bin/env bash
# PostToolUse hook: suggest /compact when activity count is high
# Triggers after 30+ tool operations in current session
# Profile: standard+

source .claude/hooks/lib/profile-check.sh 2>/dev/null && require_profile standard

LOG=".claude/memory/activity-log.md"
MARKER="/tmp/stopa-compact-suggested-$$"

# Only suggest once per session (parent PID as session proxy)
PPID_MARKER="/tmp/stopa-compact-suggested-${PPID}"
if [ -f "$PPID_MARKER" ]; then
  exit 0
fi

if [ ! -f "$LOG" ]; then
  exit 0
fi

# Count total entries
total=$(grep -c "^- " "$LOG" 2>/dev/null || echo 0)

# Threshold: suggest at 30+ operations
if [ "$total" -ge 30 ]; then
  touch "$PPID_MARKER"
  echo "=== COMPACT SUGGESTION ==="
  echo "Session has $total tracked operations. Consider running /compact to reduce context size."
  echo "This preserves important results while freeing context window."
fi

exit 0
