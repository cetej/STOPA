#!/usr/bin/env bash
# PermissionRequest hook: Auto-approve read-only operations, log all requests
# Read-only tools: Read, Glob, Grep, WebFetch, WebSearch — approve silently
# Write tools: require normal user approval (pass through)

TOOL="${CLAUDE_TOOL_NAME:-unknown}"
LOG=".claude/memory/permission-log.md"
TS=$(date +"%Y-%m-%d %H:%M")

# Create log if missing
if [ ! -f "$LOG" ]; then
  echo "# Permission Request Log" > "$LOG"
  echo "" >> "$LOG"
  echo "Auto-captured by PermissionRequest hook. Read-only ops auto-approved." >> "$LOG"
  echo "" >> "$LOG"
fi

# Classify tool
case "$TOOL" in
  Read|Glob|Grep|WebFetch|WebSearch|mcp__context7__*)
    # Read-only — auto-approve silently
    echo "- $TS | AUTO-APPROVED | $TOOL" >> "$LOG"
    echo '{"behavior":"allow","suppressOutput":true}'
    ;;
  Bash)
    # Bash commands handled by Dippy (PreToolUse hook) — skip here
    exit 0
    ;;
  *)
    # All other tools — normal approval flow
    echo "- $TS | USER-PROMPTED | $TOOL" >> "$LOG"
    echo '{"behavior":"ask","suppressOutput":true}'
    ;;
esac

exit 0
