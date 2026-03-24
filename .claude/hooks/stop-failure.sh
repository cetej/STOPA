#!/bin/bash
# stop-failure.sh — Error recovery guidance when API errors kill a turn
# Hook event: StopFailure
# Logs the failure and suggests recovery steps

BUDGET_FILE=".claude/memory/budget.md"
CHECKPOINT_FILE=".claude/memory/checkpoint.md"

echo "Session stopped due to API error."

# Check if there's active budget (task in progress)
if [ -f "$BUDGET_FILE" ] && grep -q "in_progress\|standard\|deep\|light" "$BUDGET_FILE" 2>/dev/null; then
    echo "Active task detected. Consider running /checkpoint save before retrying."
fi

# Check if checkpoint exists
HAS_CHECKPOINT="no"
if [ -f "$CHECKPOINT_FILE" ] && [ -s "$CHECKPOINT_FILE" ]; then
    echo "Checkpoint exists — next session can resume from where you left off."
    HAS_CHECKPOINT="yes"
fi

# Slack notify — fire-and-forget
TASK="none"
if [ -f "$BUDGET_FILE" ]; then
  TASK=$(grep -m1 '^\*\*Goal\*\*:' ".claude/memory/state.md" 2>/dev/null | sed 's/\*\*Goal\*\*: *//' || echo "none")
fi
python .claude/hooks/slack-notify.py stop_failure checkpoint="$HAS_CHECKPOINT" task="$TASK" &
