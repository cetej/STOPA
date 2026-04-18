#!/bin/bash
# PreCompact hook — save critical state BEFORE context compaction
# Exit code 0 = allow compaction, 2 = block compaction
# Runs BEFORE PostCompact, so state is captured while full context is still available

# Anchor to project root via script location — prevents CWD-dependent writes
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
MEMORY_DIR="$PROJECT_ROOT/.claude/memory"

STATE="$MEMORY_DIR/state.md"
INTERMEDIATE="$MEMORY_DIR/intermediate"
TS=$(date +"%Y-%m-%d %H:%M")
TODAY=$(date +"%Y-%m-%d")

mkdir -p "$INTERMEDIATE"

# Capture pre-compaction snapshot with richer context
# (PostCompact only gets the post-compaction degraded context)
SNAPSHOT="$INTERMEDIATE/pre-compact-snapshot.md"

{
  echo "# Pre-Compaction Snapshot — $TS"
  echo ""

  # Current task from state.md
  if [ -f "$STATE" ]; then
    echo "## Task State"
    head -30 "$STATE"
    echo ""
  fi

  # Git working state
  echo "## Git State"
  echo "Branch: $(git branch --show-current 2>/dev/null || echo 'unknown')"
  echo "Uncommitted files: $(git status --porcelain 2>/dev/null | wc -l)"
  echo ""

  # Pending learnings in intermediate
  PENDING=$(find "$INTERMEDIATE" -name "*.md" -newer "$STATE" 2>/dev/null | wc -l)
  if [ "$PENDING" -gt 0 ]; then
    echo "## Pending Intermediate Files: $PENDING"
    find "$INTERMEDIATE" -name "*.md" -newer "$STATE" -printf "%f\n" 2>/dev/null
    echo ""
  fi
} > "$SNAPSHOT"

echo "Pre-compaction snapshot saved to $SNAPSHOT"

# Always allow compaction (exit 0)
# Use exit 2 to block if we ever need to prevent compaction
exit 0
