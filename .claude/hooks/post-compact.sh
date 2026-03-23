#!/bin/bash
# PostCompact hook — auto-save checkpoint before context is lost
# Enhanced: actually writes checkpoint state, not just a reminder

CHECKPOINT=".claude/memory/checkpoint.md"
STATE=".claude/memory/state.md"
BUDGET=".claude/memory/budget.md"
TS=$(date +"%Y-%m-%d %H:%M")
TODAY=$(date +"%Y-%m-%d")

# Extract current task from state.md if it exists
TASK="unknown"
if [ -f "$STATE" ]; then
  TASK=$(grep -m1 '^\*\*Goal\*\*:' "$STATE" 2>/dev/null | sed 's/\*\*Goal\*\*: *//' || echo "unknown")
fi

# Extract branch
BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")

# Build auto-checkpoint
cat > "$CHECKPOINT" << CKEOF
# Auto-Checkpoint (PostCompact)

**Saved**: $TODAY $TS
**Trigger**: Context compaction (automatic)
**Branch**: $BRANCH

## Task
$TASK

## Status
Context was compacted. This checkpoint was auto-saved to preserve session state.
Review and update manually if needed.

## Resume Prompt

> Context was compacted at $TS on $TODAY.
> Branch: $BRANCH
> Task: $TASK
> Check state.md and budget.md for full context.
CKEOF

echo "Auto-checkpoint saved to $CHECKPOINT after context compaction."
