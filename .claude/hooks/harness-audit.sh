#!/usr/bin/env bash
# SessionStart hook: run stopa-audit.py and write JSON to intermediate/
# Lightweight — Python script is fast (no network, no LLM)
# Output: none (writes to intermediate/audit-report.json)

SCRIPT="scripts/stopa-audit.py"
OUTPUT=".claude/memory/intermediate/audit-report.json"

if [ ! -f "$SCRIPT" ]; then
  exit 0
fi

mkdir -p ".claude/memory/intermediate" 2>/dev/null

python "$SCRIPT" --json > "$OUTPUT" 2>/dev/null

# Extract overall score for status message
if [ -f "$OUTPUT" ]; then
  # Simple extraction without jq (Windows compatibility)
  score=$(python -c "import json,sys; d=json.load(open('$OUTPUT')); print(d['overall_score'])" 2>/dev/null)
  grade=$(python -c "import json,sys; d=json.load(open('$OUTPUT')); print(d['summary'])" 2>/dev/null)
  if [ -n "$score" ]; then
    echo "Harness audit: ${score}/10 (${grade})"
  fi
fi
