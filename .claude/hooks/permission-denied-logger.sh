#!/usr/bin/env bash
# PermissionDenied hook: Log auto-mode classifier denials for analysis
# Hook event: PermissionDenied
# CC v2.1.89+: fires after auto mode classifier denies a tool call
#
# Returns: {"retry": true} if the denial is for a known-safe pattern
#          nothing otherwise (let the denial stand)
#
# Profile: minimal (always active — security telemetry)

LOG=".claude/memory/intermediate/permission-denials.json"
TS=$(date +"%Y-%m-%dT%H:%M:%S")

# Read tool details from stdin
INPUT=$(cat)

TOOL_NAME=$(echo "$INPUT" | sed -n 's/.*"tool_name" *: *"\([^"]*\)".*/\1/p' | head -1)
REASON=$(echo "$INPUT" | sed -n 's/.*"reason" *: *"\([^"]*\)".*/\1/p' | head -1)

# Log every denial for pattern analysis
mkdir -p "$(dirname "$LOG")"
if [ ! -f "$LOG" ]; then
    echo '[]' > "$LOG"
fi

# Append denial record (use Python for safe JSON append)
python3 -c "
import json, sys
try:
    with open('$LOG', 'r') as f:
        data = json.load(f)
except (json.JSONDecodeError, FileNotFoundError):
    data = []
data.append({
    'ts': '$TS',
    'tool': '$TOOL_NAME',
    'reason': '$REASON'
})
# Keep last 50 entries
data = data[-50:]
with open('$LOG', 'w') as f:
    json.dump(data, f, indent=2)
" 2>/dev/null

# Known-safe retry patterns:
# - Read/Glob/Grep are always safe to retry (read-only)
case "$TOOL_NAME" in
    Read|Glob|Grep|WebSearch|WebFetch)
        echo '{"retry": true}'
        ;;
    *)
        # Let denial stand — human must approve
        ;;
esac
