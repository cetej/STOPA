#!/usr/bin/env bash
# Shared profile gate for STOPA hooks
# Usage: source .claude/hooks/lib/profile-check.sh && require_profile standard
#
# Profiles (cumulative):
#   minimal  — only essential hooks (checkpoint, memory-brief, activity-log)
#   standard — + cost-tracker, suggest-compact, scribe-reminder (default)
#   strict   — + observe, ruff-lint, all quality gates
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
