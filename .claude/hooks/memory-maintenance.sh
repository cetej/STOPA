#!/usr/bin/env bash
# SessionStart hook: check memory file sizes and warn if maintenance needed
# Threshold: 100 lines (warn), 500 lines (circuit breaker per CLAUDE.md)

MEMORY_DIR=".claude/memory"
WARN_THRESHOLD=100
CRITICAL_THRESHOLD=500
warnings=""

if [ ! -d "$MEMORY_DIR" ]; then
  exit 0
fi

for file in "$MEMORY_DIR"/decisions.md "$MEMORY_DIR"/learnings.md "$MEMORY_DIR"/budget.md "$MEMORY_DIR"/state.md "$MEMORY_DIR"/news.md; do
  [ -f "$file" ] || continue
  lines=$(wc -l < "$file" 2>/dev/null | tr -d ' ')
  name=$(basename "$file")

  if [ "$lines" -ge "$CRITICAL_THRESHOLD" ]; then
    warnings="${warnings}[CRITICAL] $name has $lines lines (limit: $CRITICAL_THRESHOLD). Run /scribe maintenance before continuing.\n"
  elif [ "$lines" -ge "$WARN_THRESHOLD" ]; then
    warnings="${warnings}[WARN] $name has $lines lines. Consider running /scribe maintenance soon.\n"
  fi
done

# Activity log pruning: keep last 100 entries when over 200 lines
if [ -f "$MEMORY_DIR/activity-log.md" ]; then
  al_lines=$(wc -l < "$MEMORY_DIR/activity-log.md" 2>/dev/null | tr -d ' ')
  if [ "$al_lines" -gt 200 ]; then
    header=$(head -5 "$MEMORY_DIR/activity-log.md")
    tail_entries=$(tail -100 "$MEMORY_DIR/activity-log.md")
    printf "%s\n%s\n" "$header" "$tail_entries" > "$MEMORY_DIR/activity-log.md"
  fi
fi

if [ -n "$warnings" ]; then
  echo "=== MEMORY MAINTENANCE NEEDED ==="
  echo -e "$warnings"
fi

exit 0
