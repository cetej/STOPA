#!/usr/bin/env bash
# Stop hook: rebuild concept graph from learnings (Hebbian consolidation).
# Hippocampus-inspired: "sleep consolidation" — encode new connections at session end.
# Runs async, non-blocking. Max 10s.

cd "$(dirname "$0")/../.." 2>/dev/null || exit 0

# Skip for subagent Stop events (agent_type present = subagent)
HOOK_INPUT=$(cat 2>/dev/null || true)
echo "$HOOK_INPUT" | grep -q '"agent_type"' && exit 0

# Only rebuild if learnings dir is newer than graph
GRAPH=".claude/memory/concept-graph.json"
LEARNINGS=".claude/memory/learnings"

if [ ! -d "$LEARNINGS" ]; then
    exit 0
fi

# Check if any learning is newer than graph
NEEDS_REBUILD=false
if [ ! -f "$GRAPH" ]; then
    NEEDS_REBUILD=true
else
    for f in "$LEARNINGS"/*.md; do
        if [ "$f" -nt "$GRAPH" ] 2>/dev/null; then
            NEEDS_REBUILD=true
            break
        fi
    done
fi

if [ "$NEEDS_REBUILD" = "true" ]; then
    python .claude/hooks/lib/associative_engine.py build >/dev/null 2>&1
    # Phase 3e: optimize after rebuild (prune, normalize, compact)
    python .claude/hooks/lib/associative_engine.py optimize >/dev/null 2>&1
fi
