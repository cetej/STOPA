#!/usr/bin/env bash
# SessionStart hook: show pending improvement tips for the current project
# Checks GitHub issues with "improvement" label in the current repo

set -euo pipefail

# Detect current project repo from git remote
REPO=$(git remote get-url origin 2>/dev/null | sed 's/.*github.com[:/]\(.*\)\.git/\1/' | sed 's/.*github.com[:/]\(.*\)/\1/' || echo "")

if [ -z "$REPO" ]; then
    exit 0
fi

# Count open improvement issues
COUNT=$(gh issue list --repo "$REPO" --label "improvement" --state open --json number 2>/dev/null | python3 -c "import sys,json; print(len(json.load(sys.stdin)))" 2>/dev/null || echo "0")

if [ "$COUNT" -gt 0 ]; then
    echo "=== Cross-Project Improvements ==="
    echo "  $COUNT open improvement tip(s) for $REPO"
    echo "  Run: gh issue list --repo $REPO --label improvement --state open"
    echo ""
fi
