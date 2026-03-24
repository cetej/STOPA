#!/usr/bin/env bash
# Pre/PostToolUse hook: passive observation for pattern extraction
# Captures tool name + input snippet → .claude/memory/observations.jsonl
# Profile: strict only (verbose, slight overhead)

source .claude/hooks/lib/profile-check.sh 2>/dev/null && require_profile strict

OBS=".claude/memory/observations.jsonl"
TOOL="${CLAUDE_TOOL_NAME:-unknown}"
INPUT="${CLAUDE_TOOL_INPUT:-}"
EXIT="${CLAUDE_TOOL_EXIT_CODE:-}"
TS=$(date +"%Y-%m-%dT%H:%M:%S")

# Truncate input to 200 chars for storage efficiency
INPUT_SHORT=$(echo "$INPUT" | head -c 200 | tr '\n' ' ' | tr '"' "'")

# Determine phase (pre vs post) by checking exit code presence
if [ -n "$EXIT" ]; then
  PHASE="post"
else
  PHASE="pre"
  EXIT="n/a"
fi

# Skip read-only tools in pre phase (too noisy)
if [ "$PHASE" = "pre" ]; then
  case "$TOOL" in
    Read|Glob|Grep|TodoRead) exit 0 ;;
  esac
fi

# Append JSONL entry
echo "{\"ts\":\"$TS\",\"phase\":\"$PHASE\",\"tool\":\"$TOOL\",\"exit\":\"$EXIT\",\"input\":\"$INPUT_SHORT\"}" >> "$OBS"

# Prune to last 500 entries (avoid unbounded growth)
if [ -f "$OBS" ]; then
  lines=$(wc -l < "$OBS")
  if [ "$lines" -gt 500 ]; then
    tail -300 "$OBS" > "${OBS}.tmp" && mv "${OBS}.tmp" "$OBS"
  fi
fi

exit 0
