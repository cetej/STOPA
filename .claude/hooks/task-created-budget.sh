#!/bin/bash
# task-created-budget.sh — Auto-track task creation in budget
# Hook event: TaskCreated (CC 2.1.84+)
# Logs new task to budget.md for automatic tracking

BUDGET_FILE=".claude/memory/budget.md"

if [ -f "$BUDGET_FILE" ]; then
    # Increment task counter
    CURRENT=$(grep -oP 'Tasks created: \K\d+' "$BUDGET_FILE" 2>/dev/null || echo "0")
    NEW_COUNT=$((CURRENT + 1))

    if grep -q "Tasks created:" "$BUDGET_FILE" 2>/dev/null; then
        sed -i "s/Tasks created: [0-9]*/Tasks created: $NEW_COUNT/" "$BUDGET_FILE"
    else
        # Add counter if not present
        echo "- Tasks created: $NEW_COUNT" >> "$BUDGET_FILE"
    fi
fi
