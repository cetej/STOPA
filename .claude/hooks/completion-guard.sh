#!/usr/bin/env bash
# completion-guard.sh — Stop event hook
# Warns if active task has incomplete subtasks (prevents premature session end)
# Inspired by oh-my-claudecode's ralph persistence, but as WARNING not blocker.

# Anchor to project root via script location — prevents CWD-dependent reads
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
STATE_FILE="$PROJECT_ROOT/.claude/memory/state.md"

# Skip for subagent Stop events (agent_type present = subagent)
HOOK_INPUT=$(cat 2>/dev/null || true)
echo "$HOOK_INPUT" | grep -q '"agent_type"' && exit 0

# Silent exit if no state file
[ -f "$STATE_FILE" ] || exit 0

# Check if there's an active task (not "_No active task._")
if grep -q "^_No active task._$" "$STATE_FILE" 2>/dev/null; then
  exit 0
fi

# Check if Active Task section exists with in_progress status
if ! grep -q "in_progress" "$STATE_FILE" 2>/dev/null; then
  exit 0
fi

# Count incomplete subtasks (not "done" and not "skipped")
# Use tr -d to strip CR from Windows line endings
# Count data rows: lines starting with | that contain a digit (subtask number)
TOTAL=$(grep -cE "^\| [0-9]" "$STATE_FILE" 2>/dev/null | tr -d '\r' || true)
DONE=$(grep -cE "\| done \|" "$STATE_FILE" 2>/dev/null | tr -d '\r' || true)
SKIPPED=$(grep -cE "\| skipped \|" "$STATE_FILE" 2>/dev/null | tr -d '\r' || true)
TOTAL=${TOTAL:-0}
DONE=${DONE:-0}
SKIPPED=${SKIPPED:-0}

INCOMPLETE=$((TOTAL - DONE - SKIPPED))

if [ "$INCOMPLETE" -gt 0 ]; then
  TASK_NAME=$(grep "^\*\*Goal\*\*:" "$STATE_FILE" 2>/dev/null | head -1 | sed 's/\*\*Goal\*\*: //')
  cat <<EOF
=== COMPLETION GUARD ===
Active task has $INCOMPLETE incomplete subtask(s) out of $TOTAL.
Task: $TASK_NAME
Consider finishing the task or running /checkpoint before stopping.
EOF
fi

exit 0
