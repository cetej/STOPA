#!/usr/bin/env bash
# Test harness for permission-sentinel.py (Layer 2)
# Tests fail-safe behavior since no live API key is assumed in CI

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SENTINEL="$SCRIPT_DIR/../permission-sentinel.py"
FAIL=0
PASS=0

check() {
  local name="$1"
  local payload="$2"
  local expected="$3"
  local env_setup="$4"
  local out

  if [ -n "$env_setup" ]; then
    out=$(eval "$env_setup" python "$SENTINEL" <<< "$payload" 2>/dev/null)
  else
    out=$(echo "$payload" | python "$SENTINEL" 2>/dev/null)
  fi

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

echo "=== Testing $SENTINEL ==="
echo ""

echo "--- No API key (graceful passthrough) ---"
# Without ANTHROPIC_API_KEY, sentinel must emit empty {} so CC handles normally
unset ANTHROPIC_API_KEY
check "no api key -> passthrough" \
  '{"tool_name":"Write","tool_input":{"file_path":"/foo","content":"bar"}}' \
  '^{}$'

echo ""
echo "--- Dry-run mode (skip API, log only) ---"
check "dryrun mode -> passthrough" \
  '{"tool_name":"Write","tool_input":{"file_path":"/foo","content":"bar"}}' \
  '^{}$' \
  'STOPA_SENTINEL_DRYRUN=1'

echo ""
echo "--- Invalid JSON input (graceful passthrough) ---"
check "invalid json -> passthrough" \
  'not json at all' \
  '^{}$'

echo ""
echo "--- Empty stdin (graceful passthrough) ---"
out=$(echo '' | python "$SENTINEL" 2>/dev/null)
if echo "$out" | grep -q '^{}$'; then
  echo "  PASS: empty stdin -> passthrough"
  PASS=$((PASS+1))
else
  echo "  FAIL: empty stdin"
  echo "    got: $out"
  FAIL=$((FAIL+1))
fi

echo ""
echo "--- Output JSON validity ---"
out=$(echo '{"tool_name":"Read"}' | python "$SENTINEL" 2>/dev/null)
if echo "$out" | python -c "import json,sys; json.load(sys.stdin)" 2>/dev/null; then
  echo "  PASS: output is valid JSON"
  PASS=$((PASS+1))
else
  echo "  FAIL: output not valid JSON: $out"
  FAIL=$((FAIL+1))
fi

echo ""
echo "--- Sentinel log written ---"
LOG_BEFORE=$(wc -l < "$SCRIPT_DIR/../../memory/sentinel-log.jsonl" 2>/dev/null || echo 0)
echo '{"tool_name":"Write","tool_input":{"file_path":"/test"}}' | STOPA_SENTINEL_DRYRUN=1 python "$SENTINEL" >/dev/null 2>&1
LOG_AFTER=$(wc -l < "$SCRIPT_DIR/../../memory/sentinel-log.jsonl" 2>/dev/null || echo 0)
if [ "$LOG_AFTER" -gt "$LOG_BEFORE" ]; then
  echo "  PASS: sentinel-log.jsonl received entry"
  PASS=$((PASS+1))
else
  echo "  FAIL: log not written ($LOG_BEFORE -> $LOG_AFTER)"
  FAIL=$((FAIL+1))
fi

echo ""
echo "=== Results: $PASS passed, $FAIL failed ==="
exit $FAIL
