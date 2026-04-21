#!/bin/bash
# telegram-notify.sh — NEUTRALIZED 2026-04-21 (user disabled Telegram notifications)
# Previous behavior: POST to Telegram Bot API.
# New behavior: append to .claude/memory/alerts.md (low-noise log).
# Usage: bash telegram-notify.sh "message text"
#
# To re-enable Telegram later: restore from git history (commit before 2026-04-21).

# Skip subagent Stop events (preserved from original)
HOOK_INPUT=$(cat 2>/dev/null || true)
echo "$HOOK_INPUT" | grep -q '"agent_type"' && exit 0

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
LOG="$PROJECT_ROOT/.claude/memory/alerts.md"
TS=$(date +"%Y-%m-%d %H:%M")
MESSAGE="${1:-Task completed}"

# Strip markdown/emoji safely for log
MSG_FLAT=$(echo "$MESSAGE" | tr '\n' ' ' | head -c 500)

if [ -f "$LOG" ]; then
    {
        echo ""
        echo "## $TS — [hook] $MSG_FLAT"
        echo "- **Severity:** low"
        echo "- **Source:** telegram-notify.sh (legacy caller)"
        echo "- **Status:** open"
    } >> "$LOG" 2>/dev/null || true
fi

exit 0
