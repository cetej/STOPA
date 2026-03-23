#!/usr/bin/env bash
# PostToolUse hook: Run ruff linter on Python files after Write/Edit
# Returns additionalContext on errors (Claude sees and auto-fixes)
# Returns suppressOutput:true on success (silent)

TOOL="${CLAUDE_TOOL_NAME:-unknown}"

# Only trigger on Write/Edit
case "$TOOL" in
  Write|Edit|MultiEdit) ;;
  *) echo '{"continue":true,"suppressOutput":true}'; exit 0 ;;
esac

# Extract file path from tool input
INPUT="${CLAUDE_TOOL_INPUT:-}"
FILE_PATH=$(echo "$INPUT" | grep -oP '"file_path"\s*:\s*"([^"]+)"' | head -1 | sed 's/.*"file_path"\s*:\s*"\([^"]*\)".*/\1/')

# Only check .py files
if [[ ! "$FILE_PATH" =~ \.py$ ]]; then
  echo '{"continue":true,"suppressOutput":true}'
  exit 0
fi

# Check if ruff is available
if ! command -v ruff &> /dev/null; then
  echo '{"continue":true,"suppressOutput":true}'
  exit 0
fi

# Run ruff check
LINT_OUTPUT=$(ruff check "$FILE_PATH" 2>&1)
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
