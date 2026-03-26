#!/usr/bin/env bash
# PreToolUse hook: Protect critical config files from accidental overwrites
# Inspired by ECC Tools config protection pattern
#
# BLOCK: settings.json, settings.local.json, hooks.json overwrites
# WARN:  CLAUDE.md changes (allowed but flagged)
# PASS:  everything else

# Read tool input from stdin
INPUT=$(cat)

TOOL="${CLAUDE_TOOL_NAME:-unknown}"

# Only care about write operations
case "$TOOL" in
  Write|Edit|mcp__filesystem__write_file|mcp__filesystem__edit_file)
    ;;
  *)
    exit 0
    ;;
esac

# Extract file path from tool input (sed-based — avoids JSON/PCRE issues on Windows)
FILE_PATH=$(echo "$INPUT" | sed -n 's/.*"file_path" *: *"\([^"]*\)".*/\1/p' | head -1)
if [ -z "$FILE_PATH" ]; then
  FILE_PATH=$(echo "$INPUT" | sed -n 's/.*"path" *: *"\([^"]*\)".*/\1/p' | head -1)
fi

# Normalize backslashes to forward slashes
FILE_PATH=$(echo "$FILE_PATH" | sed 's|\\\\|/|g; s|\\|/|g')

# Extract just the filename for matching
BASENAME=$(basename "$FILE_PATH")

case "$BASENAME" in
  settings.json|settings.local.json)
    echo '{"decision":"block","reason":"⛔ Config protection: settings.json cannot be edited directly by tools. Use /update-config skill or edit manually."}'
    exit 0
    ;;
  hooks.json)
    echo '{"decision":"block","reason":"⛔ Config protection: hooks.json is managed by settings.json hooks config. Edit settings.json manually if needed."}'
    exit 0
    ;;
  CLAUDE.md)
    # Allow but warn — CLAUDE.md edits are intentional but worth flagging
    echo "⚠️ Editing CLAUDE.md — make sure this is intentional" >&2
    exit 0
    ;;
  *)
    exit 0
    ;;
esac
