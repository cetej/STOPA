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

# --- Learning confidence audit (Dream consolidation detection) ---
# Check for learnings with confidence < 0.3 (pruning candidates)
LEARNINGS_DIR="$MEMORY_DIR/learnings"
low_confidence_count=0
if [ -d "$LEARNINGS_DIR" ]; then
  for lfile in "$LEARNINGS_DIR"/*.md; do
    [ -f "$lfile" ] || continue
    # Extract confidence from YAML frontmatter
    conf=$(sed -n '/^---$/,/^---$/{ s/^confidence: *//p; }' "$lfile" 2>/dev/null | head -1)
    if [ -n "$conf" ]; then
      # Compare as integer (multiply by 10 to avoid float comparison in bash)
      conf_int=$(echo "$conf" | awk '{printf "%d", $1 * 10}')
      if [ "$conf_int" -lt 3 ]; then
        low_confidence_count=$((low_confidence_count + 1))
      fi
    fi
  done

  if [ "$low_confidence_count" -gt 0 ]; then
    warnings="${warnings}[DREAM] $low_confidence_count learning(s) below confidence 0.3 — run /evolve to review pruning candidates.\n"
  fi
fi

if [ -n "$warnings" ]; then
  echo "=== MEMORY MAINTENANCE NEEDED ==="
  echo -e "$warnings"
fi

exit 0
