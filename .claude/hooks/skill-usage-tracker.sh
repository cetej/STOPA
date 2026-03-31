#!/bin/bash
# skill-usage-tracker.sh — Log skill invocations for self-evolution analysis
# Called as PostToolUse hook when Skill tool is used
# Appends to ~/.claude/memory/skill-usage.jsonl

# Profile: standard
source .claude/hooks/lib/profile-check.sh 2>/dev/null && require_profile standard

USAGE_FILE=".claude/memory/skill-usage.jsonl"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Extract skill name from CLAUDE_TOOL_INPUT JSON (PostToolUse env var)
SKILL_NAME=""
if [ -n "$CLAUDE_TOOL_INPUT" ]; then
    SKILL_NAME=$(echo "$CLAUDE_TOOL_INPUT" | python3 -c "import json,sys; print(json.load(sys.stdin).get('skill',''))" 2>/dev/null)
fi

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
