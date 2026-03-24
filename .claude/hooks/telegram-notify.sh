#!/bin/bash
# telegram-notify.sh — Send push notification to Telegram
# Usage: bash telegram-notify.sh "message text"
# Reads bot token from ~/.claude/channels/telegram/.env

ENV_FILE="$HOME/.claude/channels/telegram/.env"
CHAT_ID="1328589040"

if [ ! -f "$ENV_FILE" ]; then
    exit 0
fi

TOKEN=$(grep -m1 'TELEGRAM_BOT_TOKEN=' "$ENV_FILE" | cut -d= -f2)
MESSAGE="${1:-Task completed}"

if [ -n "$TOKEN" ]; then
    curl -s -X POST "https://api.telegram.org/bot${TOKEN}/sendMessage" \
        -d chat_id="$CHAT_ID" \
        -d text="$MESSAGE" \
        -d parse_mode="Markdown" \
        > /dev/null 2>&1
fi
