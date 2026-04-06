#!/bin/bash
# learnings-sync.sh — Sync critical learnings to global memory + rebuild indexes
# Hook event: PostToolUse (matcher: Write|Edit, path contains learnings/)
# 1. Copies critical/high severity learnings to ~/.claude/memory/cross-project-learnings.md
# 2. Auto-rebuilds component indexes and block manifest when stale

# Profile: standard
source .claude/hooks/lib/profile-check.sh 2>/dev/null && require_profile standard

TOOL_INPUT="${CLAUDE_TOOL_INPUT:-}"
GLOBAL_FILE="$HOME/.claude/memory/cross-project-learnings.md"
MANIFEST=".claude/memory/learnings/block-manifest.json"
INDEX_SCRIPT="scripts/build-component-indexes.py"

# Only trigger on writes to learnings/ directory
if ! echo "$TOOL_INPUT" | grep -q "learnings/"; then
    exit 0
fi

# Find the file that was just written
FILE=$(echo "$TOOL_INPUT" | grep -oP '"file_path"\s*:\s*"([^"]*learnings/[^"]*)"' | head -1 | sed 's/.*"file_path"\s*:\s*"//;s/"//')
if [ -z "$FILE" ]; then
    exit 0
fi

# --- Part 1: Global sync for critical/high learnings ---
if [ -f "$FILE" ] && grep -q "severity: \(critical\|high\)" "$FILE" 2>/dev/null; then
    PROJECT=$(basename "$(git -C "$(dirname "$FILE")" rev-parse --show-toplevel 2>/dev/null)" 2>/dev/null || echo "unknown")
    DATE=$(date +%Y-%m-%d)
    TITLE=$(grep -m1 "^#" "$FILE" 2>/dev/null | sed 's/^#* *//')

    if [ -f "$GLOBAL_FILE" ] && ! grep -q "$TITLE" "$GLOBAL_FILE" 2>/dev/null; then
        echo "" >> "$GLOBAL_FILE"
        echo "### [$DATE] $PROJECT — $TITLE" >> "$GLOBAL_FILE"
        grep -A2 "severity:" "$FILE" 2>/dev/null >> "$GLOBAL_FILE"
        echo "→ sync z lokálních learnings" >> "$GLOBAL_FILE"
        echo "[LEARNINGS-SYNC] Synced critical learning to global memory: $TITLE"
    fi
fi

# --- Part 2: Auto-rebuild indexes if manifest is stale ---
# Skip for index files and non-learning files
BASENAME=$(basename "$FILE")
if echo "$BASENAME" | grep -qE "^(index-|block-manifest|critical-patterns|ecosystem-scan)"; then
    exit 0
fi

if [ -f "$INDEX_SCRIPT" ]; then
    NEEDS_REBUILD=false
    if [ ! -f "$MANIFEST" ]; then
        NEEDS_REBUILD=true
    elif [ "$FILE" -nt "$MANIFEST" ] 2>/dev/null; then
        NEEDS_REBUILD=true
    fi

    if [ "$NEEDS_REBUILD" = true ]; then
        python "$INDEX_SCRIPT" > /dev/null 2>&1
        # Also rebuild concept graph for hybrid retrieval (LLM Wiki v2 integration)
        python .claude/hooks/lib/associative_engine.py build > /dev/null 2>&1
        echo "[LEARNINGS-SYNC] Rebuilt component indexes, block manifest, and concept graph"
    fi
fi
