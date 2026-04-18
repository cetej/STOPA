#!/usr/bin/env bash
# PostToolUse hook: log significant tool events to activity-log.md
# Only captures Write/Edit/Agent/Skill/significant Bash — skips read-only tools for performance
# Parses tool name from stdin JSON (reliable) with env var fallback

# Anchor to project root via script location — prevents CWD-dependent writes
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
LOG="$PROJECT_ROOT/.claude/memory/activity-log.md"
TS=$(date +"%Y-%m-%d %H:%M")

# Parse tool name from stdin JSON (CC passes tool details via stdin)
# Format: {"tool_name": "Write", "tool_input": {...}, ...}
STDIN_DATA=""
if read -t 1 -r STDIN_DATA 2>/dev/null; then
  # Extract tool_name from JSON using lightweight parsing
  TOOL=$(echo "$STDIN_DATA" | sed -n 's/.*"tool_name"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)
  # Extract tool_input for Bash command detection
  INPUT=$(echo "$STDIN_DATA" | sed -n 's/.*"tool_input"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)
fi

# Fallback to env vars (may not be set in all CC versions)
TOOL="${TOOL:-${CLAUDE_TOOL_NAME:-unknown}}"
INPUT="${INPUT:-${CLAUDE_TOOL_INPUT:-}}"
EXIT="${CLAUDE_TOOL_EXIT_CODE:-0}"

# Skip unknown tools (means neither stdin nor env var worked)
if [ "$TOOL" = "unknown" ]; then
  exit 0
fi

# Create log file with header if missing
if [ ! -f "$LOG" ]; then
  echo "# Activity Log" > "$LOG"
  echo "" >> "$LOG"
  echo "Auto-captured by PostToolUse hook. Harvested by /scribe and /checkpoint." >> "$LOG"
  echo "Pruned to last 100 entries by memory-maintenance.sh." >> "$LOG"
  echo "" >> "$LOG"
fi

case "$TOOL" in
  Write|Edit|MultiEdit)
    # Extract file_path from stdin JSON for file-tracking
    FILE_PATH=$(echo "$STDIN_DATA" | sed -n 's/.*"file_path"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)
    if [ -n "$FILE_PATH" ]; then
      echo "- $TS | $TOOL | $(basename "$FILE_PATH") | exit=$EXIT" >> "$LOG"
    else
      echo "- $TS | $TOOL | exit=$EXIT" >> "$LOG"
    fi
    ;;
  Bash)
    # Only log significant Bash commands (git, package managers)
    if echo "$INPUT" | grep -qiE "git commit|git push|npm |pip |python "; then
      echo "- $TS | Bash (significant) | exit=$EXIT" >> "$LOG"
    fi
    ;;
  Agent)
    echo "- $TS | Agent spawn | exit=$EXIT" >> "$LOG"
    ;;
  Skill)
    # Try to extract skill name from input JSON
    SKILL_NAME=$(echo "$STDIN_DATA" | sed -n 's/.*"skill"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)
    if [ -n "$SKILL_NAME" ]; then
      echo "- $TS | Skill:$SKILL_NAME | exit=$EXIT" >> "$LOG"
    else
      echo "- $TS | Skill | exit=$EXIT" >> "$LOG"
    fi
    ;;
esac

exit 0
