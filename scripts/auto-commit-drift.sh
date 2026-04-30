#!/usr/bin/env bash
# auto-commit-drift.sh — Commit auto-generated drift directly to main, no PR.
#
# Behavior:
#   1. Inspect uncommitted + untracked paths in the current repo.
#   2. Classify them via drift-classify.sh.
#   3. If ALL are drift: stage them, commit on main, push.
#      If ANY are non-drift: bail with exit 1 (caller should split commits or open PR).
#   4. Refuses to run on detached HEAD or while branch != main unless --force-branch.
#
# Usage:
#   scripts/auto-commit-drift.sh                       # auto-detect, commit, push
#   scripts/auto-commit-drift.sh --check               # classify only, no writes
#   scripts/auto-commit-drift.sh --message "msg"       # custom commit subject
#   scripts/auto-commit-drift.sh --no-push             # commit only, skip push
#   scripts/auto-commit-drift.sh --force-branch        # allow non-main branch
#
# Exit codes:
#   0 — committed (or --check passed) successfully
#   1 — non-drift paths detected; caller must split or open PR
#   2 — repo state unsafe (rebase in progress, detached HEAD, etc.)
#   3 — push failed (commit was made, but remote rejected)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || true)"
if [[ -z "$REPO_ROOT" ]]; then
  echo "auto-commit-drift: not in a git repo" >&2
  exit 2
fi
cd "$REPO_ROOT"

CHECK_ONLY=0
NO_PUSH=0
FORCE_BRANCH=0
COMMIT_MSG=""
TARGET_BRANCH="main"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --check)         CHECK_ONLY=1 ;;
    --no-push)       NO_PUSH=1 ;;
    --force-branch)  FORCE_BRANCH=1 ;;
    --message)       shift; COMMIT_MSG="${1:-}" ;;
    --branch)        shift; TARGET_BRANCH="${1:-main}" ;;
    -h|--help)
      sed -n '2,21p' "$0"; exit 0 ;;
    *)
      echo "auto-commit-drift: unknown arg: $1" >&2; exit 2 ;;
  esac
  shift
done

# ----------------------------------------------------------------------------
# Safety: refuse on detached HEAD, rebase/merge in progress
# ----------------------------------------------------------------------------
current_branch="$(git symbolic-ref --short HEAD 2>/dev/null || echo "DETACHED")"
if [[ "$current_branch" == "DETACHED" ]]; then
  echo "auto-commit-drift: HEAD is detached; refusing to commit" >&2
  exit 2
fi

if [[ -d .git/rebase-apply || -d .git/rebase-merge ]]; then
  echo "auto-commit-drift: rebase in progress; refusing" >&2
  exit 2
fi

if [[ -f .git/MERGE_HEAD ]]; then
  echo "auto-commit-drift: merge in progress; refusing" >&2
  exit 2
fi

if [[ "$current_branch" != "$TARGET_BRANCH" && "$FORCE_BRANCH" -ne 1 ]]; then
  echo "auto-commit-drift: not on $TARGET_BRANCH (current: $current_branch); use --force-branch to override" >&2
  echo "auto-commit-drift: rationale — drift commits should land on $TARGET_BRANCH directly, not in a feature branch" >&2
  exit 2
fi

# ----------------------------------------------------------------------------
# Collect changed paths (modified + staged + untracked)
# ----------------------------------------------------------------------------
mapfile -t changed_paths < <(
  {
    git diff --name-only
    git diff --name-only --cached
    git ls-files --others --exclude-standard
  } | sort -u | sed '/^$/d'
)

if [[ ${#changed_paths[@]} -eq 0 ]]; then
  echo "auto-commit-drift: working tree clean, nothing to commit"
  exit 0
fi

# ----------------------------------------------------------------------------
# Classify
# ----------------------------------------------------------------------------
if ! printf '%s\n' "${changed_paths[@]}" | python "$SCRIPT_DIR/drift_classify.py" -; then
  echo "auto-commit-drift: aborting — non-drift paths detected (above)" >&2
  echo "auto-commit-drift: action required:" >&2
  echo "  • commit non-drift changes manually with descriptive message and open PR" >&2
  echo "  • OR amend drift_classify.py DRIFT_PATTERNS if path was misclassified" >&2
  exit 1
fi

if [[ "$CHECK_ONLY" -eq 1 ]]; then
  exit 0
fi

# ----------------------------------------------------------------------------
# Stage + commit
# ----------------------------------------------------------------------------
# Stage explicitly by path — never `git add -A` (per behavioral-genome).
for p in "${changed_paths[@]}"; do
  git add -- "$p"
done

if [[ -z "$COMMIT_MSG" ]]; then
  COMMIT_MSG="chore: hook-generated memory drift ($(date +%Y-%m-%d))"
fi

# Pre-commit hooks may inject signers etc.; let them run.
if ! git commit -m "$COMMIT_MSG"; then
  echo "auto-commit-drift: commit failed (likely pre-commit hook); leaving working tree as-is" >&2
  exit 1
fi

new_sha="$(git rev-parse --short HEAD)"
echo "auto-commit-drift: committed $new_sha on $current_branch — \"$COMMIT_MSG\""

# ----------------------------------------------------------------------------
# Push
# ----------------------------------------------------------------------------
if [[ "$NO_PUSH" -eq 1 ]]; then
  echo "auto-commit-drift: --no-push set, skipping push"
  exit 0
fi

if ! git push origin "$current_branch"; then
  echo "auto-commit-drift: push to origin/$current_branch failed (commit kept locally as $new_sha)" >&2
  exit 3
fi

echo "auto-commit-drift: pushed $new_sha → origin/$current_branch"
exit 0
