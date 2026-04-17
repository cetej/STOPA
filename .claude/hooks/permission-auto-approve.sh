#!/usr/bin/env bash
# PermissionRequest hook: Auto-approve safe operations, prompt for risky ones
# v3.0 — autonomous mode: most operations auto-approved
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

TOOL="${CLAUDE_TOOL_NAME:-unknown}"
LOG=".claude/memory/permission-log.md"
TS=$(date +"%Y-%m-%d %H:%M")

# Create log if missing
if [ ! -f "$LOG" ]; then
  echo "# Permission Request Log" > "$LOG"
  echo "" >> "$LOG"
  echo "Auto-captured by PermissionRequest hook. Autonomous mode v3.0." >> "$LOG"
  echo "" >> "$LOG"
fi

auto_allow() {
  echo "- $TS | AUTO | $TOOL" >> "$LOG"
  echo '{"behavior":"allow","suppressOutput":true}'
}

ask_user() {
  echo "- $TS | ASK | $TOOL" >> "$LOG"
  echo '{"behavior":"ask","suppressOutput":true}'
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
  mcp__e27626c3*gcal_list*|mcp__e27626c3*gcal_get*|mcp__e27626c3*gcal_find*)
    auto_allow
    ;;
  mcp__e27626c3*)
    # create/update/delete event, respond — sends invites, ask
    ask_user
    ;;

  # --- GOOGLE DRIVE: read auto, write ask ---
  mcp__c1fc4002*google_drive_search*|mcp__c1fc4002*google_drive_fetch*)
    auto_allow
    ;;
  mcp__c1fc4002*)
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
  Cron*)
    auto_allow
    ;;

  # --- SKILL + TOOLSEARCH: auto ---
  Skill|ToolSearch)
    auto_allow
    ;;

  # --- BASH: auto-allow (Dippy PreToolUse hook handles command-level filtering) ---
  # NOTE: exit 0 without JSON caused "stream closed" errors in scheduled task context
  Bash)
    auto_allow
    ;;

  # --- EVERYTHING ELSE: ask ---
  *)
    ask_user
    ;;
esac

exit 0
