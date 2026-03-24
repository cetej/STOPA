#!/bin/bash
# skill-usage-tracker.sh — Log skill invocations for self-evolution analysis
# Called as PostToolUse hook when Skill tool is used
# Appends to ~/.claude/memory/skill-usage.jsonl

USAGE_FILE="$HOME/.claude/memory/skill-usage.jsonl"
SKILL_NAME="$1"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Only log if skill name is provided
if [ -z "$SKILL_NAME" ]; then
    exit 0
fi

# Ensure directory exists
mkdir -p "$(dirname "$USAGE_FILE")"

# Append JSONL entry
echo "{\"ts\":\"$TIMESTAMP\",\"skill\":\"$SKILL_NAME\"}" >> "$USAGE_FILE"

# Keep file under 1000 lines (rotate old entries)
if [ "$(wc -l < "$USAGE_FILE" 2>/dev/null)" -gt 1000 ]; then
    tail -500 "$USAGE_FILE" > "${USAGE_FILE}.tmp"
    mv "${USAGE_FILE}.tmp" "$USAGE_FILE"
fi
