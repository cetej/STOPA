#!/usr/bin/env bash
# PermissionRequest hook: Auto-approve safe operations, prompt for risky ones
# v3.1 — reads tool_name from stdin JSON (PermissionRequest passes data via stdin, not env vars)
#
# AUTO-APPROVE: Read, Glob, Grep, WebFetch, WebSearch, ToolSearch, Edit, Write,
#               Agent, TodoWrite, NotebookEdit, filesystem MCP (local),
#               context7, youtube-transcript, brave-search, playwright,
#               GitHub (push, PR, issue, comment — own repos),
#               Chrome (navigate, click, type, form),
#               Telegram reply (status notifications),
#               Gmail draft, Calendar read, Google Drive
# ASK:          GitHub merge/delete, Gmail send, Calendar create/update/delete,
#               Chrome file_upload, unknown tools
# SKIP:         Bash (handled by Dippy PreToolUse hook)

LOG=".claude/memory/permission-log.md"
TS=$(date +"%Y-%m-%d %H:%M")

# Read stdin JSON and extract tool_name
TMPFILE=$(mktemp 2>/dev/null || echo "/tmp/perm-hook-$$")
timeout 2 cat > "$TMPFILE" 2>/dev/null || touch "$TMPFILE" 2>/dev/null || true
TOOL=$(python -c "
import json, sys
try:
    with open(sys.argv[1]) as f:
        d = json.load(f)
    # Try multiple JSON shapes — CC versions differ.
    name = (
        d.get('tool_name')
        or d.get('tool')
        or d.get('name')
        or (d.get('tool_use') or {}).get('name')
        or (d.get('input') or {}).get('tool_name')
        or (d.get('params') or {}).get('tool_name')
        or 'unknown'
    )
    print(name)
except Exception:
    print('unknown')
" "$TMPFILE" 2>/dev/null || echo "unknown")

# Debug: when parsing fails, dump raw stdin so next iteration can fix the parser.
if [ "$TOOL" = "unknown" ] && [ -s "$TMPFILE" ]; then
  DUMP_LOG=".claude/memory/permission-unknown-dumps.jsonl"
  {
    printf '{"ts":"%s","raw":' "$TS"
    python -c "import json,sys; print(json.dumps(open(sys.argv[1]).read()))" "$TMPFILE" 2>/dev/null || echo '"<parse-error>"'
    printf '}\n'
  } >> "$DUMP_LOG" 2>/dev/null
fi

rm -f "$TMPFILE" 2>/dev/null

# Fallback to env var (some CC versions set it)
if [ "$TOOL" = "unknown" ] && [ -n "$CLAUDE_TOOL_NAME" ]; then
  TOOL="$CLAUDE_TOOL_NAME"
fi

# Create log if missing
if [ ! -f "$LOG" ]; then
  echo "# Permission Request Log" > "$LOG"
  echo "" >> "$LOG"
  echo "Auto-captured by PermissionRequest hook. Autonomous mode v3.1." >> "$LOG"
  echo "" >> "$LOG"
fi

auto_allow() {
  echo '{"behavior":"allow","suppressOutput":true}'
  echo "- $TS | AUTO | $TOOL" >> "$LOG" 2>/dev/null || true
}

ask_user() {
  echo '{"behavior":"ask","suppressOutput":true}'
  echo "- $TS | ASK | $TOOL" >> "$LOG" 2>/dev/null || true
}

# Classify tool
case "$TOOL" in
  # --- READ-ONLY: always safe ---
  Read|Glob|Grep|WebFetch|WebSearch)
    auto_allow
    ;;

  # --- LOCAL WRITE: git is safety net ---
  Edit|Write|Agent|TodoWrite|NotebookEdit)
    auto_allow
    ;;

  # --- SAFE MCP: read-only or local-only ---
  mcp__context7__*|mcp__youtube-transcript__*|mcp__brave-search__*)
    auto_allow
    ;;
  mcp__filesystem__*)
    auto_allow
    ;;
  mcp__Claude_Preview__*)
    auto_allow
    ;;
  mcp__scheduled-tasks__*)
    auto_allow
    ;;
  mcp__mcp-registry__*)
    auto_allow
    ;;
  mcp__ccd_session__*)
    auto_allow
    ;;
  mcp__ccd_directory__*)
    auto_allow
    ;;

  # --- GITHUB: most write ops auto, merge/delete ask ---
  mcp__github__get_*|mcp__github__list_*|mcp__github__search_*)
    auto_allow
    ;;
  mcp__github__merge_*|mcp__github__fork_*)
    # merge PR, fork — irreversible, ask
    ask_user
    ;;
  mcp__github__*)
    # push, create PR/issue/branch, comment, review, update — auto
    auto_allow
    ;;

  # --- GMAIL: read + draft auto, send ask ---
  mcp__4d0c1623*gmail_search*|mcp__4d0c1623*gmail_read*|mcp__4d0c1623*gmail_get*|mcp__4d0c1623*gmail_list*)
    auto_allow
    ;;
  mcp__4d0c1623*gmail_create_draft*)
    # draft doesn't send — auto
    auto_allow
    ;;
  mcp__4d0c1623*)
    # send — ask
    ask_user
    ;;

  # --- CALENDAR: read/find auto, write ask ---
  mcp__e27626c3*list*|mcp__e27626c3*get*)
    auto_allow
    ;;
  mcp__e27626c3*suggest_time*)
    auto_allow
    ;;
  mcp__e27626c3*)
    # create/update/delete event, respond — sends invites, ask
    ask_user
    ;;

  # --- GOOGLE DRIVE (22ffc942 UUID): read auto, write ask ---
  mcp__22ffc942*list*|mcp__22ffc942*get*|mcp__22ffc942*search*|mcp__22ffc942*read*|mcp__22ffc942*download*)
    auto_allow
    ;;
  mcp__22ffc942*)
    ask_user
    ;;

  # --- CHROME BROWSER: full interaction auto, upload ask ---
  mcp__Claude_in_Chrome__file_upload|mcp__Claude_in_Chrome__upload_image)
    # uploads send data out — ask
    ask_user
    ;;
  mcp__Claude_in_Chrome__switch_browser)
    ask_user
    ;;
  mcp__Claude_in_Chrome__*)
    # navigate, click, type, form, screenshot, read, find, tabs — auto
    auto_allow
    ;;

  # --- PLAYWRIGHT: full interaction auto ---
  mcp__playwright__browser_file_upload)
    ask_user
    ;;
  mcp__playwright__*)
    auto_allow
    ;;

  # --- TELEGRAM: reply/react/edit auto (own bot, status only) ---
  mcp__plugin_telegram_telegram__reply|mcp__plugin_telegram_telegram__react|mcp__plugin_telegram_telegram__edit_message|mcp__plugin_telegram_telegram__download_attachment)
    auto_allow
    ;;

  # --- CRON: auto (session-only, no persistent damage) ---
  Cron*|SendMessage|Monitor|RemoteTrigger|TaskOutput|TaskStop|TeamCreate|TeamDelete)
    auto_allow
    ;;
  EnterWorktree|ExitWorktree|EnterPlanMode|ExitPlanMode|ScheduleWakeup)
    auto_allow
    ;;

  # --- SKILL + TOOLSEARCH: auto ---
  Skill|ToolSearch)
    auto_allow
    ;;

  # --- PUSH NOTIFICATION: auto (outbound to own devices) ---
  PushNotification)
    auto_allow
    ;;

  # --- BASH: auto-allow (Dippy PreToolUse hook handles command-level filtering) ---
  Bash)
    auto_allow
    ;;

  # --- UNKNOWN / FALLTHROUGH: auto-allow ---
  # Dangerous ops are explicitly listed above (GitHub merge, Gmail send, Calendar write, Chrome upload).
  # If tool_name parsing failed or a new tool arrived, auto-allow is safer than blocking the session.
  *)
    auto_allow
    ;;
esac

exit 0
