#!/usr/bin/env bash
# SessionStart hook: inject checkpoint resume prompt into context
# Only emits the Resume Prompt section — full checkpoint is redundant
# because context-inject.py already extracts SESSION CONTINUITY narrative
# from the same file with better filtering.

# Anchor to project root via script location — prevents CWD-dependent reads
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
CHECKPOINT="$PROJECT_ROOT/.claude/memory/checkpoint.md"

if [ ! -f "$CHECKPOINT" ]; then
  exit 0
fi

content=$(cat "$CHECKPOINT" 2>/dev/null)

# Skip if empty or placeholder
if [ -z "$content" ] || echo "$content" | grep -q "No active checkpoint"; then
  exit 0
fi

# Extract just the Resume Prompt section (after "## Resume Prompt" heading)
# This is the actionable part — task + context + what to do next
resume=$(sed -n '/^## Resume Prompt/,/^## /{ /^## Resume Prompt/d; /^## [^R]/q; p; }' "$CHECKPOINT" 2>/dev/null)

if [ -z "$resume" ]; then
  # Fallback: extract Task + Last commit + Branch (minimal context)
  resume=$(grep -E '^\*\*(Task|Branch|Last commit)\*\*' "$CHECKPOINT" 2>/dev/null)
fi

if [ -n "$resume" ]; then
  echo "=== ACTIVE CHECKPOINT ==="
  echo "$resume"
  echo "=== Nabídni uživateli pokračování z checkpointu ==="
fi

# Slack notify — fire-and-forget
BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
TASK=$(grep -m1 '^\*\*Task\*\*:' "$CHECKPOINT" 2>/dev/null | sed 's/\*\*Task\*\*: *//' || echo "unknown")
python "$SCRIPT_DIR/slack-notify.py" session_start branch="$BRANCH" task="$TASK" &
