#!/usr/bin/env bash
# PostToolUse hook (matcher: Skill): After /critic PASS, suggest /verify
# Advisory only — injects context, does not force execution.

TOOL="${CLAUDE_TOOL_NAME:-}"
INPUT="${CLAUDE_TOOL_INPUT:-}"
OUTPUT="${CLAUDE_TOOL_OUTPUT:-}"

# Only react to Skill tool usage
[ "$TOOL" != "Skill" ] && exit 0

# Check if it was the critic skill
if ! echo "$INPUT" | grep -qi '"skill"[[:space:]]*:[[:space:]]*"critic"'; then
  exit 0
fi

# Check if critic output indicates PASS (various formats)
if echo "$OUTPUT" | grep -qiE '(PASS|passed|no.*(issues|problems)|clean|approved|all good)'; then
  cat <<'EOF'
{"additionalContext": "✅ Critic PASS detected. To prove the changes work end-to-end, run /verify on the last changes. This completes the quality chain: edit → critic → verify."}
EOF
fi
