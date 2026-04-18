#!/bin/bash
# eval-trigger.sh — Detect SKILL.md edits and remind agent to run evals
# Hook event: PostToolUse (matcher: Write|Edit)
# Outputs a system reminder when a SKILL.md file is modified

# Anchor to project root via script location — prevents CWD-dependent reads
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Profile: standard
source "$SCRIPT_DIR/lib/profile-check.sh" 2>/dev/null && require_profile standard

TOOL_INPUT="${CLAUDE_TOOL_INPUT:-}"

# Only trigger on SKILL.md files
if ! echo "$TOOL_INPUT" | grep -qi "SKILL\.md\|skills/"; then
    exit 0
fi

# Extract skill name from path
SKILL_NAME=$(echo "$TOOL_INPUT" | grep -oP 'skills/\K[^/]+' | head -1)
if [ -z "$SKILL_NAME" ]; then
    exit 0
fi

# Check if eval cases exist for this skill
EVAL_DIR="$PROJECT_ROOT/.claude/evals/$SKILL_NAME"
if [ -d "$EVAL_DIR" ]; then
    CASE_COUNT=$(find "$EVAL_DIR" -name "case-*.md" 2>/dev/null | wc -l)
    if [ "$CASE_COUNT" -gt 0 ]; then
        echo "[EVAL-TRIGGER] Skill '$SKILL_NAME' was modified. $CASE_COUNT behavioral eval cases exist in $EVAL_DIR. Run them to verify the change didn't break behavior. Use: /harness eval-runner --skill $SKILL_NAME"
    fi
else
    echo "[EVAL-TRIGGER] Skill '$SKILL_NAME' was modified but has no eval cases yet. Consider adding cases to .claude/evals/$SKILL_NAME/ for regression coverage."
fi
