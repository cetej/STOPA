#!/bin/bash
# task-created-budget.sh — Auto-track task creation in budget
# Hook event: TaskCreated (CC 2.1.84+)
# Logs new task to budget.md for automatic tracking

# Profile: standard
source .claude/hooks/lib/profile-check.sh 2>/dev/null && require_profile standard

BUDGET_FILE=".claude/memory/budget.md"

if [ -f "$BUDGET_FILE" ]; then
    # Increment task counter
    CURRENT=$(grep -o 'Tasks created: [0-9]*' "$BUDGET_FILE" 2>/dev/null | grep -o '[0-9]*$' || echo "0")
    NEW_COUNT=$((CURRENT + 1))

    if grep -q "Tasks created:" "$BUDGET_FILE" 2>/dev/null; then
        sed -i "s/Tasks created: [0-9]*/Tasks created: $NEW_COUNT/" "$BUDGET_FILE"
    else
        # Add counter if not present
        echo "- Tasks created: $NEW_COUNT" >> "$BUDGET_FILE"
    fi
fi
