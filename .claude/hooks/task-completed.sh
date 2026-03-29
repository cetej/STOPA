#!/bin/bash
# task-completed.sh — Auto-compound: extract task learnings on completion
# Hook event: TaskCompleted (CC v2.1.84+)
# Timeout: 15s (set in settings.json)
#
# Flow:
# 1. Skip if no orchestrated task ran (no completed subtasks in state.md)
# 2. Run auto-compound-agent.py (Haiku analysis)
#    - confidence >= 0.8 → write learning to learnings/
#    - confidence <  0.8 → print suggestion to stdout (injected into context)
# 3. Telegram notify

set -euo pipefail

STATE_FILE=".claude/memory/state.md"
CAPTURE_SCRIPT=".claude/hooks/auto-compound-agent.py"

# Only proceed if an orchestrated task ran (state.md has completed subtasks)
if [ ! -f "$STATE_FILE" ]; then
    exit 0
fi

if ! grep -qiE "(✅|status.*done|status.*completed|\- \[x\])" "$STATE_FILE" 2>/dev/null; then
    exit 0
fi

# Run auto-compound agent (writes learnings or prints suggestions)
if [ -f "$CAPTURE_SCRIPT" ]; then
    python "$CAPTURE_SCRIPT" 2>/dev/null || true
fi

# Telegram notify — fire-and-forget
TASK=$(grep -m1 '^\*\*Goal\*\*:' "$STATE_FILE" 2>/dev/null | sed 's/\*\*Goal\*\*: *//' || echo "unknown")
bash .claude/hooks/telegram-notify.sh "✅ *Task completed:* ${TASK}" 2>/dev/null &
