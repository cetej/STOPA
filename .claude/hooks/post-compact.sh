#!/bin/bash
# PostCompact hook — auto-save checkpoint before context is lost
# Enhanced: actually writes checkpoint state, not just a reminder

# Anchor to project root via script location — prevents CWD-dependent writes
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

CHECKPOINT="$PROJECT_ROOT/.claude/memory/checkpoint.md"
STATE="$PROJECT_ROOT/.claude/memory/state.md"
BUDGET="$PROJECT_ROOT/.claude/memory/budget.md"
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

# Flush scratchpad/intermediate insights to raw/ for compound loop
SCRATCHPAD="$PROJECT_ROOT/.claude/memory/intermediate/scratchpad.md"
RAW_DIR="$PROJECT_ROOT/.claude/memory/raw"
if [ -f "$SCRATCHPAD" ] && [ -s "$SCRATCHPAD" ]; then
  RAW_FILE="$RAW_DIR/${TODAY}-compaction-flush.md"
  mkdir -p "$RAW_DIR"
  {
    echo "# Pre-Compaction Flush — $TS"
    echo ""
    echo "**Source**: scratchpad (auto-flushed before context compaction)"
    echo "**Task**: $TASK"
    echo ""
    cat "$SCRATCHPAD"
  } > "$RAW_FILE"
  echo "Flushed scratchpad to $RAW_FILE"
fi

# Flush pending decisions from activity log
ACTIVITY="$PROJECT_ROOT/.claude/memory/intermediate/activity-log.md"
if [ -f "$ACTIVITY" ] && [ -s "$ACTIVITY" ]; then
  # Append recent decisions to raw/ for /compile pickup
  DECISION_COUNT=$(grep -c "decision\|DECISION\|rozhodnutí" "$ACTIVITY" 2>/dev/null || echo "0")
  if [ "$DECISION_COUNT" -gt 0 ]; then
    RAW_DECISIONS="$RAW_DIR/${TODAY}-decisions-flush.md"
    mkdir -p "$RAW_DIR"
    grep -A2 "decision\|DECISION\|rozhodnutí" "$ACTIVITY" > "$RAW_DECISIONS" 2>/dev/null
    echo "Flushed $DECISION_COUNT decision entries to $RAW_DECISIONS"
  fi
fi

echo "Auto-checkpoint saved to $CHECKPOINT after context compaction."

# Slack notify — fire-and-forget
python .claude/hooks/slack-notify.py post_compact branch="$BRANCH" task="$TASK" &
