#!/usr/bin/env bash
# PermissionRequest hook v4 — Guardian Layer 1 (static DSL + tool classification)
#
# Inspired by AgentSpec (arXiv:2503.18666) — pre-action synchronous DSL enforcement.
# Three-layer permission gate:
#   L1 DSL: pattern-match on tool_name + tool_input (file_path, content) — this file
#   L2 Sentinel: LLM-based decision for escalated cases (future, prompt hook)
#   L3 Fallback: deny-with-reason for destructive patterns
#
# v4 changes:
#   - Modern output format: {"hookSpecificOutput":{"permissionDecision":"allow|deny|ask"}}
#   - Tool input parsing (file_path, content) for DSL evaluation
#   - Critical invariant deny-list (API keys/secrets in JSON configs)
#   - Routine-path allow-list (index.md, brain/, memory/learnings/, outputs/)
#   - Decision log with layer tag (L1-dsl / L0-classifier) for future tuning

# Anchor to project root via script location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

LOG="$PROJECT_ROOT/.claude/memory/permission-log.md"
SENTINEL_LOG="$PROJECT_ROOT/.claude/memory/sentinel-log.jsonl"
TS=$(date +"%Y-%m-%d %H:%M")

# Read stdin JSON once
TMPFILE=$(mktemp 2>/dev/null || echo "/tmp/perm-hook-$$")
timeout 2 cat > "$TMPFILE" 2>/dev/null || touch "$TMPFILE" 2>/dev/null || true

# Extract tool_name, tool_input.file_path, tool_input.content in one Python call
PARSED=$(python -c "
import json, sys
try:
    with open(sys.argv[1]) as f:
        d = json.load(f)
    name = (
        d.get('tool_name')
        or d.get('tool')
        or d.get('name')
        or (d.get('tool_use') or {}).get('name')
        or (d.get('input') or {}).get('tool_name')
        or (d.get('params') or {}).get('tool_name')
        or 'unknown'
    )
    ti = d.get('tool_input') or {}
    fp = (ti.get('file_path') or ti.get('path') or '').replace(chr(92), '/')
    # content may be under 'content' (Write), 'new_string' (Edit), or 'command' (Bash)
    content = ti.get('content') or ti.get('new_string') or ti.get('command') or ''
    # Truncate content to 2000 chars for pattern matching (secrets usually in first few hundred)
    content = content[:2000]
    # Tab-separated output: name<TAB>file_path<TAB>content (content newlines stripped)
    content_flat = content.replace('\t', ' ').replace('\n', ' ')
    print(f'{name}\t{fp}\t{content_flat}')
except Exception as e:
    print(f'unknown\t\t')
" "$TMPFILE" 2>/dev/null || echo "unknown")

TOOL=$(echo "$PARSED" | cut -f1)
FILE_PATH=$(echo "$PARSED" | cut -f2)
CONTENT=$(echo "$PARSED" | cut -f3)

# Debug dump for unparseable payloads
if [ "$TOOL" = "unknown" ] && [ -s "$TMPFILE" ]; then
  DUMP_LOG="$PROJECT_ROOT/.claude/memory/permission-unknown-dumps.jsonl"
  {
    printf '{"ts":"%s","raw":' "$TS"
    python -c "import json,sys; print(json.dumps(open(sys.argv[1]).read()))" "$TMPFILE" 2>/dev/null || echo '"<parse-error>"'
    printf '}\n'
  } >> "$DUMP_LOG" 2>/dev/null
fi

rm -f "$TMPFILE" 2>/dev/null

# Fallback to env var
if [ "$TOOL" = "unknown" ] && [ -n "$CLAUDE_TOOL_NAME" ]; then
  TOOL="$CLAUDE_TOOL_NAME"
fi

# Ensure log file exists
if [ ! -f "$LOG" ]; then
  echo "# Permission Request Log" > "$LOG"
  echo "" >> "$LOG"
  echo "Auto-captured by PermissionRequest hook. Autonomous mode v4 (Guardian L1)." >> "$LOG"
  echo "" >> "$LOG"
fi

# Output helpers — modern hookSpecificOutput format
auto_allow() {
  local layer="${1:-L0}"
  local reason="${2:-classifier allow}"
  echo '{"hookSpecificOutput":{"hookEventName":"PermissionRequest","permissionDecision":"allow"},"suppressOutput":true}'
  echo "- $TS | AUTO-$layer | $TOOL | $reason" >> "$LOG" 2>/dev/null || true
  log_jsonl "$layer" "allow" "$reason"
}

deny_with_reason() {
  local layer="${1:-L1}"
  local reason="${2:-critical invariant violation}"
  # Escape quotes in reason for JSON
  local reason_esc="${reason//\"/\\\"}"
  printf '{"hookSpecificOutput":{"hookEventName":"PermissionRequest","permissionDecision":"deny","permissionDecisionReason":"%s"},"suppressOutput":false}\n' "$reason_esc"
  echo "- $TS | DENY-$layer | $TOOL | $reason" >> "$LOG" 2>/dev/null || true
  log_jsonl "$layer" "deny" "$reason"
}

ask_user() {
  local layer="${1:-L0}"
  local reason="${2:-unclassified risk}"
  # If L2 sentinel is enabled (env var or settings.json hook chain), prefer escalation.
  # Otherwise emit ask for live user.
  if [ "${STOPA_L2_SENTINEL:-0}" = "1" ]; then
    passthrough "$layer" "$reason -> L2"
    return
  fi
  echo '{"hookSpecificOutput":{"hookEventName":"PermissionRequest","permissionDecision":"ask"},"suppressOutput":true}'
  echo "- $TS | ASK-$layer | $TOOL | $reason" >> "$LOG" 2>/dev/null || true
  log_jsonl "$layer" "ask" "$reason"
}

# Passthrough — empty {} response. Lets next hook in chain (L2 sentinel) decide.
# Used when STOPA_L2_SENTINEL=1 for previously-ASK cases.
# If no L2 hook is configured, CC falls back to default (asks user).
passthrough() {
  local layer="${1:-L0}"
  local reason="${2:-escalate to L2}"
  echo '{}'
  echo "- $TS | ESCALATE-$layer | $TOOL | $reason" >> "$LOG" 2>/dev/null || true
  log_jsonl "$layer" "escalate" "$reason"
}

# Structured JSONL log for metrics and L1->L2 promotion analysis
log_jsonl() {
  local layer="$1"
  local decision="$2"
  local reason="$3"
  python -c "
import json, sys, time
entry = {
    'ts': '$TS',
    'layer': '$layer',
    'decision': '$decision',
    'tool': '''$TOOL''',
    'file_path': '''$FILE_PATH''',
    'reason': '''$reason''',
}
print(json.dumps(entry))
" 2>/dev/null >> "$SENTINEL_LOG" 2>/dev/null || true
}

# ============================================================================
# LAYER 1: DSL Rules (pre-action synchronous enforcement, AgentSpec-style)
# Evaluated BEFORE the classic tool classifier.
# Returns early on match; falls through to L0 classifier on no match.
# ============================================================================

# --- Critical invariant denies (hard stop) ---
# Writing secrets to JSON configs = core-invariants.md #4 violation
if [ "$TOOL" = "Write" ] || [ "$TOOL" = "Edit" ]; then
  case "$FILE_PATH" in
    *.json|*settings*|*config*|*mcp*)
      # Check content for API key / secret patterns
      case "$CONTENT" in
        *api_key*|*API_KEY*|*sk-*|*SECRET*|*bearer*|*Bearer*|*password*)
          # Only deny if it looks like an actual value assignment, not just a key mention
          case "$CONTENT" in
            *'"api_key"'*:*\"*|*API_KEY=*|*sk-*|*SECRET=*|*'"SECRET"'*:*\"*)
              deny_with_reason "L1" "critical invariant: secret value in JSON/config file - use env var"
              exit 0
              ;;
          esac
          ;;
      esac
      ;;
  esac
fi

# --- Routine-path allow-list (fast auto-approve) ---
if [ "$TOOL" = "Write" ] || [ "$TOOL" = "Edit" ] || [ "$TOOL" = "NotebookEdit" ]; then
  case "$FILE_PATH" in
    # Wiki indices and content pages — safe, high-frequency writes (case-insensitive INDEX)
    */brain/wiki/index.md|*/brain/wiki/INDEX.md|*/brain/wiki/log.md|*/brain/wiki/concepts/*.md|*/brain/wiki/entities/*.md|*/brain/wiki/sources/*.md)
      auto_allow "L1" "routine wiki write"
      exit 0
      ;;
    # Brain raw/processed pipeline + knowledge/concept graphs
    */brain/raw/processed/*.md|*/brain/inbox.md|*/brain/watchlist.md|*/brain/knowledge-graph.json|*/brain/**/*.md|*/brain/**/*.json)
      auto_allow "L1" "routine brain pipeline write"
      exit 0
      ;;
    # Memory concept graph (ingest target) + daily reports, news streams
    */memory/concept-graph.json|*/memory/daily-reports.md|*/memory/news.md|*/memory/watchlist.md|*/memory/inbox.md)
      auto_allow "L1" "routine memory graph/feed write"
      exit 0
      ;;
    # Wiki INDEX at memory root (ingest writes here too)
    */memory/wiki/INDEX.md|*/memory/wiki/index.md|*/memory/wiki/entities/*.md|*/memory/wiki/sources/*.md|*/memory/wiki/concepts/*.md|*/memory/wiki/log.md)
      auto_allow "L1" "routine wiki (memory root)"
      exit 0
      ;;
    # Memory learnings, outcomes, failures, dreams — append-mostly
    */memory/learnings/*.md|*/memory/outcomes/*.md|*/memory/failures/*.md|*/memory/dreams/*.md)
      auto_allow "L1" "routine memory artifact write"
      exit 0
      ;;
    # Optstate, replay queue — counter updates
    */memory/optstate/*.json|*/memory/replay-queue.md)
      auto_allow "L1" "routine state counter update"
      exit 0
      ;;
    # Research outputs
    */outputs/*.md|*/outputs/.research/*.md)
      auto_allow "L1" "routine research output"
      exit 0
      ;;
    # News, radar, improvement log — monitoring outputs
    */memory/news.md|*/memory/radar.md|*/memory/improvement-log.md|*/memory/sentinel-log.jsonl)
      auto_allow "L1" "routine monitoring log"
      exit 0
      ;;
    # Permission log archives (self-referential, safe)
    */memory/permission-log-*-archive.md)
      auto_allow "L1" "permission log archive"
      exit 0
      ;;
  esac
fi

# ============================================================================
# LAYER 0: Classic tool classifier (fallthrough)
# Original logic preserved for non-DSL-matched cases.
# ============================================================================

case "$TOOL" in
  # --- READ-ONLY: always safe ---
  Read|Glob|Grep|WebFetch|WebSearch)
    auto_allow "L0" "read-only"
    ;;

  # --- LOCAL WRITE: git is safety net ---
  Edit|Write|Agent|TodoWrite|NotebookEdit)
    auto_allow "L0" "local-write (git protected)"
    ;;

  # --- SAFE MCP: read-only or local-only ---
  mcp__context7__*|mcp__youtube-transcript__*|mcp__brave-search__*)
    auto_allow "L0" "safe-mcp"
    ;;
  mcp__filesystem__*)
    auto_allow "L0" "fs-mcp"
    ;;
  mcp__Claude_Preview__*|mcp__scheduled-tasks__*|mcp__mcp-registry__*|mcp__ccd_session__*|mcp__ccd_directory__*)
    auto_allow "L0" "internal-mcp"
    ;;

  # --- GITHUB ---
  mcp__github__get_*|mcp__github__list_*|mcp__github__search_*)
    auto_allow "L0" "github-read"
    ;;
  mcp__github__merge_*|mcp__github__fork_*)
    ask_user "L0" "github irreversible op"
    ;;
  mcp__github__*)
    auto_allow "L0" "github-write (own repos)"
    ;;

  # --- GMAIL ---
  mcp__4d0c1623*gmail_search*|mcp__4d0c1623*gmail_read*|mcp__4d0c1623*gmail_get*|mcp__4d0c1623*gmail_list*)
    auto_allow "L0" "gmail-read"
    ;;
  mcp__4d0c1623*gmail_create_draft*)
    auto_allow "L0" "gmail-draft"
    ;;
  mcp__4d0c1623*)
    ask_user "L0" "gmail send"
    ;;

  # --- CALENDAR ---
  mcp__e27626c3*list*|mcp__e27626c3*get*|mcp__e27626c3*suggest_time*)
    auto_allow "L0" "calendar-read"
    ;;
  mcp__e27626c3*)
    ask_user "L0" "calendar write (sends invites)"
    ;;

  # --- GOOGLE DRIVE ---
  mcp__22ffc942*list*|mcp__22ffc942*get*|mcp__22ffc942*search*|mcp__22ffc942*read*|mcp__22ffc942*download*)
    auto_allow "L0" "drive-read"
    ;;
  mcp__22ffc942*)
    ask_user "L0" "drive-write"
    ;;

  # --- CHROME ---
  mcp__Claude_in_Chrome__file_upload|mcp__Claude_in_Chrome__upload_image)
    ask_user "L0" "chrome upload (outbound data)"
    ;;
  mcp__Claude_in_Chrome__switch_browser)
    ask_user "L0" "chrome switch browser"
    ;;
  mcp__Claude_in_Chrome__*)
    auto_allow "L0" "chrome interactive"
    ;;

  # --- PLAYWRIGHT ---
  mcp__playwright__browser_file_upload)
    ask_user "L0" "playwright upload"
    ;;
  mcp__playwright__*)
    auto_allow "L0" "playwright"
    ;;

  # --- TELEGRAM ---
  mcp__plugin_telegram_telegram__reply|mcp__plugin_telegram_telegram__react|mcp__plugin_telegram_telegram__edit_message|mcp__plugin_telegram_telegram__download_attachment)
    auto_allow "L0" "telegram-reply"
    ;;

  # --- CRON / SESSION MGMT ---
  Cron*|SendMessage|Monitor|RemoteTrigger|TaskOutput|TaskStop|TeamCreate|TeamDelete)
    auto_allow "L0" "cron/session-mgmt"
    ;;
  EnterWorktree|ExitWorktree|EnterPlanMode|ExitPlanMode|ScheduleWakeup)
    auto_allow "L0" "worktree/plan-mode"
    ;;

  # --- SKILL / TOOLSEARCH ---
  Skill|ToolSearch)
    auto_allow "L0" "skill/toolsearch"
    ;;

  # --- PUSH NOTIFICATION ---
  PushNotification)
    auto_allow "L0" "push-notify"
    ;;

  # --- BASH: PreToolUse filter handles command-level ---
  Bash)
    auto_allow "L0" "bash (PreToolUse filter)"
    ;;

  # --- UNKNOWN / FALLTHROUGH ---
  *)
    auto_allow "L0" "unknown tool fallthrough"
    ;;
esac

exit 0
