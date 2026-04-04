#!/usr/bin/env bash
# PostToolUse hook (Skill matcher): Track which skill is currently active.
#
# When a Skill tool completes, extract skill name from stdin JSON and write
# to active-skill.json. Used by tool-gate.py for permission enforcement.
#
# stdin: {"tool_name": "Skill", "tool_input": {"skill": "orchestrate", ...}, ...}
# Also available: CLAUDE_TOOL_NAME, CLAUDE_TOOL_INPUT env vars

MARKER=".claude/memory/intermediate/active-skill.json"
TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Read stdin
STDIN_DATA=$(cat 2>/dev/null || true)

TOOL="${CLAUDE_TOOL_NAME:-}"

# Only process Skill tool events
if [ "$TOOL" != "Skill" ]; then
  # Check stdin JSON for tool_name
  TOOL=$(echo "$STDIN_DATA" | sed -n 's/.*"tool_name"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)
  [ "$TOOL" != "Skill" ] && exit 0
fi

# Extract skill name from tool_input
# Format: {"skill": "orchestrate", "args": "..."} or just {"skill": "orchestrate"}
SKILL_NAME=$(echo "$STDIN_DATA" | sed -n 's/.*"skill"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)

# Fallback: try CLAUDE_TOOL_INPUT env var
if [ -z "$SKILL_NAME" ]; then
  SKILL_NAME=$(echo "${CLAUDE_TOOL_INPUT:-}" | sed -n 's/.*"skill"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)
fi

if [ -z "$SKILL_NAME" ]; then
  exit 0
fi

# Strip namespace prefix if present (e.g., "stopa-orchestration:orchestrate" → "orchestrate")
SKILL_NAME=$(echo "$SKILL_NAME" | sed 's/.*://')

# Write marker
mkdir -p "$(dirname "$MARKER")" 2>/dev/null
cat > "$MARKER" << EOF
{"skill": "$SKILL_NAME", "started": "$TS"}
EOF

exit 0
