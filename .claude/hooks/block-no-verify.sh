#!/usr/bin/env bash
# PreToolUse:Bash hook: Block --no-verify and --no-gpg-sign flags
# These flags bypass safety checks and should never be used by AI agents
# Profile: minimal (always active — safety hook)

INPUT=$(cat)

# Check for dangerous git flags
if echo "$INPUT" | grep -qE '\-\-no-verify|\-\-no-gpg-sign'; then
  echo "BLOCK: --no-verify and --no-gpg-sign are prohibited. Fix the underlying issue instead of skipping checks." >&2
  exit 2
fi

exit 0
