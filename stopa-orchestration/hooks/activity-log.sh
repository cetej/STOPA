#!/usr/bin/env bash
# PostToolUse hook: log significant tool events to activity-log.md
# Only captures Write/Edit/Agent/Skill/significant Bash — skips read-only tools for performance
# Output: JSON with continue:true, suppressOutput:true (invisible to user)

LOG=".claude/memory/activity-log.md"
TOOL="${CLAUDE_TOOL_NAME:-unknown}"
EXIT="${CLAUDE_TOOL_EXIT_CODE:-0}"
TS=$(date +"%Y-%m-%d %H:%M")

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
    echo "- $TS | $TOOL | exit=$EXIT" >> "$LOG"
    ;;
  Bash)
    # Only log significant Bash commands (git, package managers)
    INPUT="${CLAUDE_TOOL_INPUT:-}"
    if echo "$INPUT" | grep -qiE "git commit|git push|npm |pip |python "; then
      echo "- $TS | Bash (significant) | exit=$EXIT" >> "$LOG"
    fi
    ;;
  Agent)
    echo "- $TS | Agent spawn | exit=$EXIT" >> "$LOG"
    ;;
  Skill)
    echo "- $TS | Skill | exit=$EXIT" >> "$LOG"
    ;;
esac

exit 0
