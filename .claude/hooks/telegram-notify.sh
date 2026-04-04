#!/bin/bash
# telegram-notify.sh — Send push notification to Telegram
# Usage: bash telegram-notify.sh "message text"
# Respects STOPA_VERBOSITY env var: brief (max 200 chars), standard (default), detailed
# Reads bot token from ~/.claude/channels/telegram/.env

# Skip for subagent Stop events (agent_type present = subagent)
HOOK_INPUT=$(cat 2>/dev/null || true)
echo "$HOOK_INPUT" | grep -q '"agent_type"' && exit 0

ENV_FILE="$HOME/.claude/channels/telegram/.env"
CHAT_ID="1328589040"
VERBOSITY="${STOPA_VERBOSITY:-standard}"

if [ ! -f "$ENV_FILE" ]; then
    exit 0
fi

TOKEN=$(grep -m1 'TELEGRAM_BOT_TOKEN=' "$ENV_FILE" | cut -d= -f2)
MESSAGE="${1:-Task completed}"

# Truncate based on verbosity mode
case "$VERBOSITY" in
    brief)
        MESSAGE=$(echo "$MESSAGE" | head -c 200)
        ;;
    detailed)
        # No truncation
        ;;
    *)
        # standard — max 500 chars
        MESSAGE=$(echo "$MESSAGE" | head -c 500)
        ;;
esac

if [ -n "$TOKEN" ]; then
    curl -s -X POST "https://api.telegram.org/bot${TOKEN}/sendMessage" \
        -d chat_id="$CHAT_ID" \
        -d text="$MESSAGE" \
        -d parse_mode="Markdown" \
        > /dev/null 2>&1
fi
