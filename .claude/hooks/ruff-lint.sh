#!/usr/bin/env bash
# PostToolUse hook: Run ruff linter on Python files after Write/Edit
# Returns additionalContext on errors (Claude sees and auto-fixes)
# Returns suppressOutput:true on success (silent)
# Profile: strict+

# Anchor to project root via script location — prevents CWD-dependent source
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

source "$SCRIPT_DIR/lib/profile-check.sh" 2>/dev/null && require_profile strict

TOOL="${CLAUDE_TOOL_NAME:-unknown}"

# Only trigger on Write/Edit
case "$TOOL" in
  Write|Edit|MultiEdit) ;;
  *) echo '{"continue":true,"suppressOutput":true}'; exit 0 ;;
esac

# Extract file path from tool input (POSIX-compatible, no grep -P)
INPUT="${CLAUDE_TOOL_INPUT:-}"
FILE_PATH=$(echo "$INPUT" | sed -n 's/.*"file_path"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)

# Only check .py files
if [[ ! "$FILE_PATH" =~ \.py$ ]]; then
  echo '{"continue":true,"suppressOutput":true}'
  exit 0
fi

# Find ruff command (direct or via python -m)
if command -v ruff &> /dev/null; then
  RUFF_CMD="ruff"
elif python -m ruff --version &> /dev/null; then
  RUFF_CMD="python -m ruff"
else
  echo '{"continue":true,"suppressOutput":true}'
  exit 0
fi

# Run ruff check
LINT_OUTPUT=$($RUFF_CMD check "$FILE_PATH" 2>&1)
LINT_EXIT=$?

if [ $LINT_EXIT -ne 0 ]; then
  # Errors found — feed back to Claude via additionalContext
  cat <<EOF
{"continue":true,"additionalContext":"Ruff lint errors in $FILE_PATH:\n$LINT_OUTPUT\n\nFix these lint issues before proceeding."}
EOF
else
  # Clean — silent
  echo '{"continue":true,"suppressOutput":true}'
fi

exit 0
