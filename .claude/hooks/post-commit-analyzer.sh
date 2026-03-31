#!/bin/bash
# post-commit-analyzer.sh — Analyze last commit for risky changes
# Hook event: PostToolUse (matcher: Bash, command contains "git commit")
# Checks for: breaking changes, security risks, API surface changes

TOOL_INPUT="${CLAUDE_TOOL_INPUT:-}"

# Only trigger on git commit commands
if ! echo "$TOOL_INPUT" | grep -q "git commit"; then
    exit 0
fi

# Get the last commit diff
DIFF=$(git diff HEAD~1 HEAD --stat 2>/dev/null)
if [ -z "$DIFF" ]; then
    exit 0
fi

FULL_DIFF=$(git diff HEAD~1 HEAD 2>/dev/null)
WARNINGS=""

# Check 1: Deleted public functions/classes
DELETED_FUNCS=$(echo "$FULL_DIFF" | grep "^-" | grep -E "^-\s*(def |class |async def )" | grep -v "^---" | head -5)
if [ -n "$DELETED_FUNCS" ]; then
    WARNINGS="${WARNINGS}\n⚠️ BREAKING: Deleted/renamed functions or classes:\n${DELETED_FUNCS}\n"
fi

# Check 2: Changed function signatures
CHANGED_SIGS=$(echo "$FULL_DIFF" | grep -E "^\+\s*(def |async def )" | grep -v "^+++" | head -5)
OLD_SIGS=$(echo "$FULL_DIFF" | grep -E "^-\s*(def |async def )" | grep -v "^---" | head -5)
if [ -n "$CHANGED_SIGS" ] && [ -n "$OLD_SIGS" ]; then
    WARNINGS="${WARNINGS}\n⚠️ API CHANGE: Function signatures modified — check callers\n"
fi

# Check 3: Security patterns
SECURITY=$(echo "$FULL_DIFF" | grep "^+" | grep -iE "(password|secret|token|api_key|credential)" | grep -v "^+++" | grep -v "#" | head -3)
if [ -n "$SECURITY" ]; then
    WARNINGS="${WARNINGS}\n🔒 SECURITY: Possible sensitive data in commit:\n${SECURITY}\n"
fi

# Check 4: Large changes (>200 lines)
INSERTIONS=$(echo "$DIFF" | tail -1 | sed -n 's/.*\([0-9][0-9]*\) insertion.*/\1/p')
DELETIONS=$(echo "$DIFF" | tail -1 | sed -n 's/.*\([0-9][0-9]*\) deletion.*/\1/p')
TOTAL=$(( ${INSERTIONS:-0} + ${DELETIONS:-0} ))
if [ "$TOTAL" -gt 200 ]; then
    WARNINGS="${WARNINGS}\n📊 LARGE COMMIT: ${TOTAL} lines changed — consider splitting\n"
fi

# Check 5: Config file changes
CONFIG_CHANGES=$(echo "$DIFF" | grep -E "(settings\.json|\.env|config\.|CLAUDE\.md)" | head -3)
if [ -n "$CONFIG_CHANGES" ]; then
    WARNINGS="${WARNINGS}\n⚙️ CONFIG: Configuration files modified:\n${CONFIG_CHANGES}\n"
fi

if [ -n "$WARNINGS" ]; then
    echo -e "🔍 Post-commit analysis:\n${WARNINGS}"
fi
