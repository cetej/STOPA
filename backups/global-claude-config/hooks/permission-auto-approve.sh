#!/usr/bin/env bash
# PermissionRequest hook: Auto-approve safe operations, prompt for risky ones
# v2.0 — expanded auto-approve: read + local write + agents
#
# AUTO-APPROVE: Read, Glob, Grep, WebFetch, WebSearch, Edit, Write,
#               Agent, TodoWrite, NotebookEdit, filesystem MCP (local),
#               context7, youtube-transcript, brave-search, playwright (read)
# ASK:          GitHub push/merge/PR, Gmail send, Calendar create,
#               Chrome actions, unknown tools
# SKIP:         Bash (handled by Dippy PreToolUse hook)

TOOL="${CLAUDE_TOOL_NAME:-unknown}"
# Log to project .claude/memory if exists, else to ~/.claude/permission-log.md
if [ -d ".claude/memory" ]; then
  LOG=".claude/memory/permission-log.md"
else
  LOG="$HOME/.claude/permission-log.md"
fi
TS=$(date +"%Y-%m-%d %H:%M")

# Create log if missing
if [ ! -f "$LOG" ]; then
  echo "# Permission Request Log" > "$LOG"
  echo "" >> "$LOG"
  echo "Auto-captured by PermissionRequest hook. Safe ops auto-approved (v2.0)." >> "$LOG"
  echo "" >> "$LOG"
fi

# Classify tool
case "$TOOL" in
  # --- READ-ONLY: always safe ---
  Read|Glob|Grep|WebFetch|WebSearch)
    echo "- $TS | AUTO | $TOOL" >> "$LOG"
    echo '{"behavior":"allow","suppressOutput":true}'
    ;;

  # --- LOCAL WRITE: git is safety net ---
  Edit|Write|Agent|TodoWrite|NotebookEdit)
    echo "- $TS | AUTO | $TOOL" >> "$LOG"
    echo '{"behavior":"allow","suppressOutput":true}'
    ;;

  # --- SAFE MCP: read-only or local-only ---
  mcp__context7__*|mcp__youtube-transcript__*|mcp__brave-search__*)
    echo "- $TS | AUTO | $TOOL" >> "$LOG"
    echo '{"behavior":"allow","suppressOutput":true}'
    ;;
  mcp__filesystem__read_*|mcp__filesystem__list_*|mcp__filesystem__get_*|mcp__filesystem__search_*|mcp__filesystem__directory_tree)
    echo "- $TS | AUTO | $TOOL" >> "$LOG"
    echo '{"behavior":"allow","suppressOutput":true}'
    ;;
  mcp__filesystem__write_file|mcp__filesystem__edit_file|mcp__filesystem__create_directory|mcp__filesystem__move_file)
    echo "- $TS | AUTO | $TOOL" >> "$LOG"
    echo '{"behavior":"allow","suppressOutput":true}'
    ;;
  mcp__playwright__browser_snapshot|mcp__playwright__browser_console_messages|mcp__playwright__browser_network_requests)
    echo "- $TS | AUTO | $TOOL" >> "$LOG"
    echo '{"behavior":"allow","suppressOutput":true}'
    ;;
  mcp__Claude_Preview__*)
    echo "- $TS | AUTO | $TOOL" >> "$LOG"
    echo '{"behavior":"allow","suppressOutput":true}'
    ;;
  mcp__scheduled-tasks__*)
    echo "- $TS | AUTO | $TOOL" >> "$LOG"
    echo '{"behavior":"allow","suppressOutput":true}'
    ;;

  # --- GITHUB: read = auto, write = ask ---
  mcp__github__get_*|mcp__github__list_*|mcp__github__search_*)
    echo "- $TS | AUTO | $TOOL" >> "$LOG"
    echo '{"behavior":"allow","suppressOutput":true}'
    ;;
  mcp__github__*)
    # push, merge, create PR/issue, comment — ask user
    echo "- $TS | ASK | $TOOL" >> "$LOG"
    echo '{"behavior":"ask","suppressOutput":true}'
    ;;

  # --- GMAIL/CALENDAR: always ask (sends on your behalf) ---
  mcp__4d0c1623*gmail_search*|mcp__4d0c1623*gmail_read*|mcp__4d0c1623*gmail_get*|mcp__4d0c1623*gmail_list*)
    echo "- $TS | AUTO | $TOOL" >> "$LOG"
    echo '{"behavior":"allow","suppressOutput":true}'
    ;;
  mcp__4d0c1623*)
    # send, create draft — ask
    echo "- $TS | ASK | $TOOL" >> "$LOG"
    echo '{"behavior":"ask","suppressOutput":true}'
    ;;
  mcp__e27626c3*gcal_list*|mcp__e27626c3*gcal_get*|mcp__e27626c3*gcal_find*)
    echo "- $TS | AUTO | $TOOL" >> "$LOG"
    echo '{"behavior":"allow","suppressOutput":true}'
    ;;
  mcp__e27626c3*)
    # create/update/delete event, respond — ask
    echo "- $TS | ASK | $TOOL" >> "$LOG"
    echo '{"behavior":"ask","suppressOutput":true}'
    ;;

  # --- CHROME BROWSER: read = auto, interact = ask ---
  mcp__Claude_in_Chrome__tabs_context*|mcp__Claude_in_Chrome__read_*|mcp__Claude_in_Chrome__get_*|mcp__Claude_in_Chrome__find|mcp__Claude_in_Chrome__shortcuts_list)
    echo "- $TS | AUTO | $TOOL" >> "$LOG"
    echo '{"behavior":"allow","suppressOutput":true}'
    ;;
  mcp__Claude_in_Chrome__*)
    # click, type, navigate, form — ask
    echo "- $TS | ASK | $TOOL" >> "$LOG"
    echo '{"behavior":"ask","suppressOutput":true}'
    ;;

  # --- BASH: handled by Dippy ---
  Bash)
    exit 0
    ;;

  # --- EVERYTHING ELSE: ask ---
  *)
    echo "- $TS | ASK | $TOOL" >> "$LOG"
    echo '{"behavior":"ask","suppressOutput":true}'
    ;;
esac

exit 0
