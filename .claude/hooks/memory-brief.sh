#!/usr/bin/env bash
# SessionStart hook: inject compact memory brief into context
# Provides task state, recent learnings, decisions count, news staleness, activity summary
# Runs after checkpoint-check.sh — complements checkpoint with broader memory context

# Anchor to project root via script location — prevents CWD-dependent reads
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
MEMORY_DIR="$PROJECT_ROOT/.claude/memory"
brief=""

# 1. TASK STATE — one-liner if active task exists
if [ -f "$MEMORY_DIR/state.md" ]; then
  task=$(grep -A1 "^## Active Task" "$MEMORY_DIR/state.md" 2>/dev/null | tail -1)
  if [ -n "$task" ] && ! echo "$task" | grep -qi "no active task"; then
    done=$(grep -ci "| done" "$MEMORY_DIR/state.md" 2>/dev/null || echo 0)
    total=$(grep -c "^| [0-9]" "$MEMORY_DIR/state.md" 2>/dev/null || echo 0)
    brief="${brief}Active task: $task ($done/$total subtasks done)\n"
  fi
fi

# 2. LEARNINGS — critical patterns count + recent learnings from L2 indexes
LEARNINGS_DIR="$MEMORY_DIR/learnings"
if [ -d "$LEARNINGS_DIR" ]; then
  # Count critical patterns (always-loaded)
  cp_count=0
  if [ -f "$LEARNINGS_DIR/critical-patterns.md" ]; then
    cp_count=$(grep -cE "^\*\*|^[0-9]+\." "$LEARNINGS_DIR/critical-patterns.md" 2>/dev/null || echo 0)
    cp_count=$(echo "$cp_count" | tr -cd '0-9')
    cp_count=${cp_count:-0}
  fi
  # Count total learnings files (excluding indexes and critical-patterns)
  total_learnings=$(find "$LEARNINGS_DIR" -maxdepth 1 -name "202*.md" 2>/dev/null | wc -l)
  total_learnings=$(echo "$total_learnings" | tr -cd '0-9')
  total_learnings=${total_learnings:-0}
  # Get 3 most recent learnings by filename (YYYY-MM-DD prefix sorts naturally)
  recent=$(ls -1 "$LEARNINGS_DIR"/202*.md 2>/dev/null | sort -r | head -3 | while read -r f; do
    # Extract summary from YAML frontmatter
    summary=$(grep "^summary:" "$f" 2>/dev/null | head -1 | sed "s/^summary:[[:space:]]*//" | sed "s/^['\"]//;s/['\"]$//" | head -c 80)
    if [ -n "$summary" ]; then
      echo "  - $summary"
    fi
  done)
  if [ "$cp_count" -gt 0 ] || [ "$total_learnings" -gt 0 ]; then
    brief="${brief}\nLearnings: $cp_count critical patterns, $total_learnings total"
    if [ -n "$recent" ]; then
      brief="${brief}\nRecent:\n$recent"
    fi
    brief="${brief}\n"
  fi
fi

# 3. DECISIONS — count only (not content)
if [ -f "$MEMORY_DIR/decisions.md" ]; then
  count=$(grep -c "^### " "$MEMORY_DIR/decisions.md" 2>/dev/null || echo 0)
  count=$(echo "$count" | tr -cd '0-9')
  count=${count:-0}
  if [ "$count" -gt 0 ]; then
    brief="${brief}\nActive decisions: $count (read .claude/memory/decisions.md if relevant)\n"
  fi
fi

# 4. NEWS STALENESS — warn if last scan > 7 days ago
if [ -f "$MEMORY_DIR/news.md" ]; then
  last_scan=$(grep -oP '\d{4}-\d{2}-\d{2}' "$MEMORY_DIR/news.md" 2>/dev/null | head -1)
  if [ -n "$last_scan" ]; then
    # GNU date (Git Bash on Windows) — compute days since last scan
    last_epoch=$(date -d "$last_scan" +%s 2>/dev/null)
    if [ -n "$last_epoch" ]; then
      now_epoch=$(date +%s)
      days_ago=$(( (now_epoch - last_epoch) / 86400 ))
      if [ "$days_ago" -gt 7 ]; then
        brief="${brief}\n[WARN] Last /watch scan: $last_scan ($days_ago days ago)\n"
      fi
    fi
  fi
fi

# 5. ACTIVITY LOG — summary from last session (if file exists)
if [ -f "$MEMORY_DIR/activity-log.md" ]; then
  writes=$(grep -cE "\| (Write|Edit|MultiEdit) \|" "$MEMORY_DIR/activity-log.md" 2>/dev/null)
  agents=$(grep -cE "\| Agent " "$MEMORY_DIR/activity-log.md" 2>/dev/null)
  skills=$(grep -cE "\| Skill \|" "$MEMORY_DIR/activity-log.md" 2>/dev/null)
  writes=${writes:-0}; agents=${agents:-0}; skills=${skills:-0}
  if [ "$writes" -gt 0 ] 2>/dev/null || [ "$agents" -gt 0 ] 2>/dev/null; then
    brief="${brief}\nLast session activity: $writes file edits, $agents agent spawns, $skills skill calls\n"
  fi
fi

# 6. PATTERNS — count of tracked session patterns
if [ -f "$MEMORY_DIR/patterns.md" ]; then
  pattern_count=$(grep -c "^### " "$MEMORY_DIR/patterns.md" 2>/dev/null | tr -d '[:space:]')
  pattern_count=${pattern_count:-0}
  if [ "$pattern_count" -gt 0 ] 2>/dev/null; then
    brief="${brief}\nSession patterns: $pattern_count tracked (see .claude/memory/patterns.md)\n"
  fi
fi

# 7. RELEVANCE PREFETCH — REMOVED
# Redundant with context-inject.py hybrid retrieval which does the same
# (keyword extraction from checkpoint → learning matching) but better
# (uses hybrid-retrieve.py with BM25+graph instead of simple grep).
# Removing saves ~200-400 chars per session and eliminates double-retrieval.

# Output brief to stdout → injected into Claude's context
if [ -n "$brief" ]; then
  echo "=== MEMORY BRIEF ==="
  echo -e "$brief"
fi

exit 0
