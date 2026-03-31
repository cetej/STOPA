#!/bin/bash
# file-changed-critic.sh — Suggest /critic after code file edits
# Hook event: FileChanged
# Fires when a file is modified — suggests quality review for code files

# Profile: strict
source .claude/hooks/lib/profile-check.sh 2>/dev/null && require_profile strict

FILE_PATH="${CLAUDE_FILE_PATH:-}"

# Only trigger for code files (Python, JS, TS, shell)
if [[ "$FILE_PATH" =~ \.(py|js|ts|tsx|sh)$ ]]; then
    # Skip memory/config files
    if [[ "$FILE_PATH" =~ \.claude/memory/ ]] || [[ "$FILE_PATH" =~ \.claude/settings ]]; then
        exit 0
    fi

    # Count edits in this session (avoid spamming on every save)
    COUNTER_FILE="/tmp/stopa-edit-counter-$$"
    if [ -f "$COUNTER_FILE" ]; then
        COUNT=$(cat "$COUNTER_FILE")
    else
        COUNT=0
    fi
    COUNT=$((COUNT + 1))
    echo "$COUNT" > "$COUNTER_FILE"

    # Suggest critic every 5 edits
    if [ $((COUNT % 5)) -eq 0 ]; then
        echo "[$COUNT code edits this session] Consider running /critic to check quality."
    fi
fi
