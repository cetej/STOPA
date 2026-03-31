#!/usr/bin/env bash
# Stop hook: auto-track session costs to budget.md
# Reads activity-log.md, counts operations, appends summary
# Profile: standard+

source .claude/hooks/lib/profile-check.sh 2>/dev/null && require_profile standard

BUDGET=".claude/memory/budget.md"
LOG=".claude/memory/activity-log.md"
TS=$(date +"%Y-%m-%d %H:%M")

if [ ! -f "$LOG" ]; then
  exit 0
fi

# Count operations from activity log (current session = all entries, pruned by maintenance)
writes=$(grep -cE "\| (Write|Edit|MultiEdit) \|" "$LOG" 2>/dev/null || echo 0)
agents=$(grep -cE "\| Agent " "$LOG" 2>/dev/null || echo 0)
skills=$(grep -cE "\| Skill \|" "$LOG" 2>/dev/null || echo 0)
bash_sig=$(grep -cE "\| Bash \(significant\)" "$LOG" 2>/dev/null || echo 0)
total=$((writes + agents + skills + bash_sig))

# Skip if nothing happened
if [ "$total" -eq 0 ]; then
  exit 0
fi

# Ensure budget file exists
if [ ! -f "$BUDGET" ]; then
  exit 0
fi

# Update counters in budget.md
# Parse current values and add
current_agents=$(grep "Agent spawns" "$BUDGET" 2>/dev/null | grep -oP '\| \K\d+' | head -1 || echo 0)
current_agents=${current_agents:-0}
new_agents=$((current_agents + agents))

# Append to event log section
if grep -q "^| Time | Event" "$BUDGET" 2>/dev/null; then
  # Find the event log table and append
  # Sanitize variables for sed replacement (escape &, /, \)
  SAFE_ENTRY="| ${TS//\//\\/} | auto-track: ${writes}w ${agents}a ${skills}s ${bash_sig}b | — | total=$total |"
  SAFE_ENTRY="${SAFE_ENTRY//&/\\&}"
  sed -i "/^| Time | Event | Cost | Running Total |$/a\\${SAFE_ENTRY}" "$BUDGET" 2>/dev/null
fi

# Update agent spawn counter
if [ "$agents" -gt 0 ]; then
  sed -i "s/| Agent spawns | [0-9]*/| Agent spawns | $new_agents/" "$BUDGET" 2>/dev/null
fi

exit 0
