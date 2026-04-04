#!/usr/bin/env bash
# skill-sync.sh — Auto-sync commands/ ↔ skills/ ↔ plugin after SKILL.md edits
# Triggered by PostToolUse on Write|Edit of SKILL.md or commands/*.md
# Maintains Core Invariant #2: commands/ and skills/ MUST stay identical

set -euo pipefail

STOPA_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
COMMANDS_DIR="$STOPA_ROOT/.claude/commands"
SKILLS_DIR="$STOPA_ROOT/.claude/skills"
PLUGIN_SKILLS_DIR="$STOPA_ROOT/stopa-orchestration/skills"
PLUGIN_COMMANDS_DIR="$STOPA_ROOT/stopa-orchestration/commands"

# Get the edited file path from CC hook env
TOOL_INPUT="${TOOL_INPUT:-}"
FILE_PATH=""

# Extract file_path from JSON tool input
if [ -n "$TOOL_INPUT" ]; then
  FILE_PATH=$(echo "$TOOL_INPUT" | python -c "import sys,json; d=json.load(sys.stdin); print(d.get('file_path',''))" 2>/dev/null || true)
fi

# Nothing to do if no file path
[ -z "$FILE_PATH" ] && exit 0

# Normalize path separators
FILE_PATH="${FILE_PATH//\\//}"

synced=0

# Case 1: Edited .claude/commands/<name>.md → sync to skills/ and plugin
if [[ "$FILE_PATH" == */.claude/commands/*.md ]]; then
  NAME=$(basename "$FILE_PATH" .md)
  # → skills/
  if [ -d "$SKILLS_DIR/$NAME" ]; then
    cp "$FILE_PATH" "$SKILLS_DIR/$NAME/SKILL.md"
    synced=$((synced+1))
  fi
  # → plugin skills/
  if [ -d "$PLUGIN_SKILLS_DIR/$NAME" ]; then
    cp "$FILE_PATH" "$PLUGIN_SKILLS_DIR/$NAME/SKILL.md"
    synced=$((synced+1))
  fi
  # → plugin commands/
  if [ -d "$PLUGIN_COMMANDS_DIR" ]; then
    cp "$FILE_PATH" "$PLUGIN_COMMANDS_DIR/$NAME.md"
    synced=$((synced+1))
  fi
fi

# Case 2: Edited .claude/skills/<name>/SKILL.md → sync to commands/ and plugin
if [[ "$FILE_PATH" == */.claude/skills/*/SKILL.md ]]; then
  SKILL_DIR=$(dirname "$FILE_PATH")
  NAME=$(basename "$SKILL_DIR")
  # → commands/
  cp "$FILE_PATH" "$COMMANDS_DIR/$NAME.md"
  synced=$((synced+1))
  # → plugin skills/
  if [ -d "$PLUGIN_SKILLS_DIR/$NAME" ]; then
    cp "$FILE_PATH" "$PLUGIN_SKILLS_DIR/$NAME/SKILL.md"
    synced=$((synced+1))
  fi
  # → plugin commands/
  if [ -d "$PLUGIN_COMMANDS_DIR" ]; then
    cp "$FILE_PATH" "$PLUGIN_COMMANDS_DIR/$NAME.md"
    synced=$((synced+1))
  fi
fi

# Case 3: Edited plugin skill → sync back to source (less common)
if [[ "$FILE_PATH" == */stopa-orchestration/skills/*/SKILL.md ]]; then
  SKILL_DIR=$(dirname "$FILE_PATH")
  NAME=$(basename "$SKILL_DIR")
  cp "$FILE_PATH" "$COMMANDS_DIR/$NAME.md"
  cp "$FILE_PATH" "$SKILLS_DIR/$NAME/SKILL.md"
  synced=$((synced+1))
fi

if [ "$synced" -gt 0 ]; then
  echo "[skill-sync] Synced $synced copies for $(basename "$FILE_PATH" .md)"
fi
