#!/usr/bin/env bash
# Shared project boundary guard for STOPA hooks.
# Source this at the top of any hook that should only run on STOPA files.
#
# Usage in hooks:
#   INPUT=$(cat)
#   source "$(dirname "$0")/lib/project-guard.sh"
#   # If we get here, file is within STOPA (or no file path detected)
#
# For hooks that already read stdin before sourcing:
#   source "$(dirname "$0")/lib/project-guard.sh"
#   # Uses $INPUT variable if already set, otherwise reads stdin
#
# Behavior:
#   - Extracts file_path/path from tool input JSON
#   - If file is outside STOPA project root → exit 0 (silent pass)
#   - If file is within STOPA or no path detected → continue

# Detect STOPA project root (parent of .claude/)
STOPA_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
# Normalize to forward slashes
STOPA_ROOT=$(echo "$STOPA_ROOT" | sed 's|\\|/|g')

# Extract file path from tool input
_PG_FILE_PATH=$(echo "$INPUT" | sed -n 's/.*"file_path" *: *"\([^"]*\)".*/\1/p' | head -1)
if [ -z "$_PG_FILE_PATH" ]; then
  _PG_FILE_PATH=$(echo "$INPUT" | sed -n 's/.*"path" *: *"\([^"]*\)".*/\1/p' | head -1)
fi

# Normalize path
_PG_FILE_PATH=$(echo "$_PG_FILE_PATH" | sed 's|\\\\|/|g; s|\\|/|g')

# If we have a file path and it's outside STOPA → skip this hook
if [ -n "$_PG_FILE_PATH" ]; then
  case "$_PG_FILE_PATH" in
    "$STOPA_ROOT"/*|./*|.claude/*|scripts/*|stopa-orchestration/*)
      # Within STOPA — continue with hook
      ;;
    /*)
      # Absolute path not under STOPA — skip
      exit 0
      ;;
    *)
      # Relative path — check if it resolves under STOPA
      _PG_RESOLVED=$(cd "$STOPA_ROOT" && realpath -m "$_PG_FILE_PATH" 2>/dev/null || echo "$STOPA_ROOT/$_PG_FILE_PATH")
      _PG_RESOLVED=$(echo "$_PG_RESOLVED" | sed 's|\\|/|g')
      case "$_PG_RESOLVED" in
        "$STOPA_ROOT"/*)
          ;; # Within STOPA
        *)
          exit 0  # Outside STOPA
          ;;
      esac
      ;;
  esac
fi
