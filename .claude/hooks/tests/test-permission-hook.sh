#!/usr/bin/env bash
# Test harness for permission-auto-approve hook
# Pipes sample PermissionRequest payloads and checks output decisions

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOK="${1:-$SCRIPT_DIR/../permission-auto-approve.sh}"
FAIL=0
PASS=0

check() {
  local name="$1"
  local payload="$2"
  local expected="$3"  # substring that must appear in output
  local out
  out=$(echo "$payload" | "$HOOK" 2>/dev/null)
  if echo "$out" | grep -q "$expected"; then
    echo "  PASS: $name"
    PASS=$((PASS+1))
  else
    echo "  FAIL: $name"
    echo "    payload: $payload"
    echo "    expected substring: $expected"
    echo "    got: $out"
    FAIL=$((FAIL+1))
  fi
}

echo "=== Testing $HOOK ==="
echo ""

echo "--- Read-only tools (always allow) ---"
check "Read tool" \
  '{"tool_name":"Read","tool_input":{"file_path":"/foo"}}' \
  'allow'
check "Glob tool" \
  '{"tool_name":"Glob","tool_input":{"pattern":"**/*.md"}}' \
  'allow'

echo ""
echo "--- Routine writes (L1 DSL should allow) ---"
check "Write to index.md" \
  '{"tool_name":"Write","tool_input":{"file_path":"/proj/brain/wiki/index.md","content":"# Index"}}' \
  'allow'
check "Write to brain/raw/processed" \
  '{"tool_name":"Write","tool_input":{"file_path":"/proj/.claude/memory/brain/raw/processed/foo.md","content":"# Doc"}}' \
  'allow'
check "Edit memory/learnings" \
  '{"tool_name":"Edit","tool_input":{"file_path":"/proj/.claude/memory/learnings/2026-04-21-foo.md"}}' \
  'allow'
check "Write to outputs/" \
  '{"tool_name":"Write","tool_input":{"file_path":"/proj/outputs/research.md","content":"data"}}' \
  'allow'

echo ""
echo "--- Critical invariant paths (must DENY) ---"
check "Write API key to settings.json" \
  '{"tool_name":"Write","tool_input":{"file_path":"/proj/.claude/settings.json","content":"{\"api_key\":\"sk-abc123\"}"}}' \
  'deny'
check "Write SECRET to any JSON" \
  '{"tool_name":"Write","tool_input":{"file_path":"/proj/config.json","content":"SECRET=\"foo\""}}' \
  'deny'
check "Edit .env with token" \
  '{"tool_name":"Write","tool_input":{"file_path":"/proj/.env","content":"TOKEN=abc"}}' \
  'allow'

echo ""
echo "--- Fallthrough (unclassified tools default allow) ---"
check "Unknown tool" \
  '{"tool_name":"SomeNewTool","tool_input":{}}' \
  'allow'

echo ""
echo "--- GitHub dangerous ops (must still ASK) ---"
check "GitHub merge PR" \
  '{"tool_name":"mcp__github__merge_pull_request","tool_input":{}}' \
  'ask\|deny'

echo ""
echo "--- Output format check (modern vs legacy) ---"
out=$(echo '{"tool_name":"Read"}' | "$HOOK" 2>/dev/null)
if echo "$out" | grep -q 'hookSpecificOutput'; then
  echo "  INFO: Uses modern hookSpecificOutput format"
elif echo "$out" | grep -q 'behavior'; then
  echo "  INFO: Uses legacy behavior format"
else
  echo "  WARN: Unknown output format"
fi

echo ""
echo "=== Results: $PASS passed, $FAIL failed ==="
exit $FAIL
