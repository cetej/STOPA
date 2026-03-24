#!/bin/bash
# Post-commit hook: warn when branch is ahead of origin
# Reads stdin JSON from PostToolUse, checks if command was git commit

INPUT=$(cat)

# Only trigger on git commit commands (parse without jq)
if ! echo "$INPUT" | grep -qE '"command"\s*:\s*"[^"]*git\s+commit'; then
  exit 0
fi

# Check how far ahead we are
AHEAD=$(git rev-list --count @{upstream}..HEAD 2>/dev/null || echo 0)

if [ "$AHEAD" -gt 2 ]; then
  echo "{\"systemMessage\": \"⚠️ ${AHEAD} commitů ahead of origin — nezapomeň pushnout (git push)!\"}"
fi
