#!/bin/bash
# task-completed.sh — Auto-scribe when a task finishes
# Hook event: TaskCompleted
# Reminds to record learnings after agent/skill task completion

STATE_FILE=".claude/memory/state.md"

if [ -f "$STATE_FILE" ]; then
    # Check if there's an active task with done subtasks
    if grep -q "in_progress\|done" "$STATE_FILE" 2>/dev/null; then
        echo "Task completed. Remember to record learnings with /scribe if significant patterns emerged."
        # Telegram notify — fire-and-forget
        TASK=$(grep -m1 '^\*\*Goal\*\*:' "$STATE_FILE" 2>/dev/null | sed 's/\*\*Goal\*\*: *//' || echo "unknown")
        bash .claude/hooks/telegram-notify.sh "✅ *Task completed:* ${TASK}" &
    fi
fi
