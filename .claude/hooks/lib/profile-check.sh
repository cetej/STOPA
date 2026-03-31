#!/usr/bin/env bash
# Shared profile gate for STOPA hooks
# Usage: source .claude/hooks/lib/profile-check.sh && require_profile standard
#
# Profiles (cumulative):
#   minimal  — 12 hooks: checkpoint, memory-*, activity-log, block-no-verify,
#              config-protection, completion-guard, permission-auto-approve,
#              post-compact, session-summary, stop-failure, telegram-notify
#   standard — +13 hooks: cost-tracker, suggest-compact, scribe-reminder,
#              learnings-sync, skill-*, task-*, teammate-idle, post-commit-analyzer,
#              eval-trigger, evolve-trigger, improvement-funnel (default)
#   strict   — +4 hooks: observe, ruff-lint, file-changed-critic, auto-verify-after-critic
#
# Set via: export STOPA_HOOK_PROFILE=minimal|standard|strict

STOPA_HOOK_PROFILE="${STOPA_HOOK_PROFILE:-standard}"

profile_level() {
  case "$1" in
    minimal)  echo 1 ;;
    standard) echo 2 ;;
    strict)   echo 3 ;;
    *)        echo 2 ;;  # default to standard
  esac
}

# require_profile <min_profile>
# Exits 0 (skip hook silently) if current profile is below required level
require_profile() {
  local required=$(profile_level "$1")
  local current=$(profile_level "$STOPA_HOOK_PROFILE")
  if [ "$current" -lt "$required" ]; then
    exit 0
  fi
}
