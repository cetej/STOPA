#!/bin/bash
# skill-usage-tracker.sh — Log skill invocations for self-evolution analysis
# Called as PostToolUse hook when Skill tool is used
# Appends to ~/.claude/memory/skill-usage.jsonl

# Profile: standard
source .claude/hooks/lib/profile-check.sh 2>/dev/null && require_profile standard

USAGE_FILE=".claude/memory/skill-usage.jsonl"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Read stdin (PostToolUse passes JSON via stdin in newer CC versions)
STDIN_DATA=$(cat 2>/dev/null || true)

# Extract skill name — try stdin JSON first, then CLAUDE_TOOL_INPUT env var
SKILL_NAME=""
if [ -n "$STDIN_DATA" ]; then
    SKILL_NAME=$(echo "$STDIN_DATA" | sed -n 's/.*"skill"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)
fi
if [ -z "$SKILL_NAME" ] && [ -n "$CLAUDE_TOOL_INPUT" ]; then
    SKILL_NAME=$(echo "$CLAUDE_TOOL_INPUT" | python3 -c "import json,sys; print(json.load(sys.stdin).get('skill',''))" 2>/dev/null)
fi

# Strip namespace prefix if present (e.g., "stopa-orchestration:orchestrate" → "orchestrate")
SKILL_NAME=$(echo "$SKILL_NAME" | sed 's/.*://')

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
