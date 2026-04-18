#!/usr/bin/env bash
# Stop hook: remind about /scribe if there's an active task
# Only outputs if state.md has an active task (not placeholder)
# Profile: standard+

# Skip for subagent Stop events (agent_type present = subagent)
HOOK_INPUT=$(cat 2>/dev/null || true)
echo "$HOOK_INPUT" | grep -q '"agent_type"' && exit 0

# Anchor to project root via script location — prevents CWD-dependent reads
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

source "$SCRIPT_DIR/lib/profile-check.sh" 2>/dev/null && require_profile standard

STATE="$PROJECT_ROOT/.claude/memory/state.md"

if [ ! -f "$STATE" ]; then
  exit 0
fi

# Check if state has an active task (not just "No active task")
if grep -q "Status: in_progress\|Status: active\|## Current Task" "$STATE" 2>/dev/null; then
  if ! grep -q "No active task\|_No active" "$STATE" 2>/dev/null; then
    # Output to stderr → shown as hook feedback (not injected as context)
    echo "Reminder: Aktivní task detekován. Zapiš rozhodnutí/poznatky pomocí /scribe." >&2
  fi
fi

# Slack notify — fire-and-forget (always notify on session stop)
TASK="none"
if [ -f "$STATE" ] && grep -q "## Current Task" "$STATE" 2>/dev/null; then
  TASK=$(grep -m1 '^\*\*Goal\*\*:' "$STATE" 2>/dev/null | sed 's/\*\*Goal\*\*: *//' || echo "none")
fi
python "$SCRIPT_DIR/slack-notify.py" session_stop task="$TASK" &

exit 0
