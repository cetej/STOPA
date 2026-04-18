#!/usr/bin/env bash
# TaskCreated hook: Budget-aware task creation gate
# Hook event: TaskCreated (CC v2.1.89+)
# Fires when TaskCreate tool creates a new task
#
# Checks:
# 1. Total active tasks count — warns if >15 (task sprawl)
# 2. Budget remaining — warns if low budget + new task
#
# Profile: standard

# Anchor to project root via script location — prevents CWD-dependent reads
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

source "$SCRIPT_DIR/lib/profile-check.sh" 2>/dev/null && require_profile standard

BUDGET_FILE="$PROJECT_ROOT/.claude/memory/budget.md"
MAX_ACTIVE_TASKS=15

# Count existing tasks (if task file structure is available)
TASK_DIR="$HOME/.claude/tasks"
ACTIVE_COUNT=0

if [ -d "$TASK_DIR" ]; then
    # Count tasks across all teams
    ACTIVE_COUNT=$(find "$TASK_DIR" -name "*.json" -exec grep -l '"status":"pending"\|"status":"in_progress"' {} \; 2>/dev/null | wc -l)
fi

if [ "$ACTIVE_COUNT" -gt "$MAX_ACTIVE_TASKS" ]; then
    echo "⚠️ Task sprawl warning: $ACTIVE_COUNT active tasks across teams (limit: $MAX_ACTIVE_TASKS). Consider completing existing tasks before creating new ones."
fi

# Budget check — if budget.md exists and shows low balance
if [ -f "$BUDGET_FILE" ]; then
    # Extract remaining percentage (crude grep)
    REMAINING=$(grep -oP 'remaining.*?(\d+)%' "$BUDGET_FILE" 2>/dev/null | grep -oP '\d+' | head -1)
    if [ -n "$REMAINING" ] && [ "$REMAINING" -lt 20 ]; then
        echo "⚠️ Budget warning: ${REMAINING}% remaining. New tasks will consume additional resources."
    fi
fi
