#!/bin/bash
# sync-orchestration.sh — Sync .claude/ orchestration system to target projects
#
# Usage:
#   ./scripts/sync-orchestration.sh <target1> [target2] [target3] [options]
#   ./scripts/sync-orchestration.sh ~/ng-robot ~/adobe-automat --dry-run
#   ./scripts/sync-orchestration.sh ~/ng-robot --commit --skills-only
#   ./scripts/sync-orchestration.sh --all --dry-run
#
# Syncs: .claude/skills/, .claude/hooks/, settings.json, and selected .claude/memory/ files
# Skips: CLAUDE.md (project-specific), state/checkpoint (session-specific), settings.local.json (local permissions)
# Preserves: Target-specific skills not present in STOPA are left untouched

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SOURCE_DIR="$SCRIPT_DIR/.claude"

# Known target projects (for --all)
KNOWN_TARGETS=(
    "$HOME/Documents/000_NGM/NG-ROBOT"
    "$HOME/Documents/000_NGM/test1"
    "$HOME/Documents/000_NGM/ADOBE-AUTOMAT"
)

# Memory files to sync (shared knowledge, not session state)
SYNC_MEMORY_FILES=(
    "learnings.md"
    "budget.md"
    "decisions.md"
    "decisions-archive.md"
    "budget-archive.md"
    "news.md"
)

# --- Parse args ---
TARGETS=()
DRY_RUN=false
AUTO_COMMIT=false
SYNC_SKILLS=true
SYNC_MEMORY=true
SYNC_HOOKS=true
SYNC_SETTINGS=true
SYNC_ALL=false

for arg in "$@"; do
    case "$arg" in
        --dry-run) DRY_RUN=true ;;
        --commit) AUTO_COMMIT=true ;;
        --skills-only) SYNC_MEMORY=false; SYNC_HOOKS=false; SYNC_SETTINGS=false ;;
        --memory-only) SYNC_SKILLS=false; SYNC_HOOKS=false; SYNC_SETTINGS=false ;;
        --hooks-only) SYNC_SKILLS=false; SYNC_MEMORY=false; SYNC_SETTINGS=false ;;
        --all) SYNC_ALL=true ;;
        -*) echo "Unknown option: $arg"; exit 1 ;;
        *) TARGETS+=("$arg") ;;
    esac
done

# Expand --all to known targets
if [ "$SYNC_ALL" = true ]; then
    for t in "${KNOWN_TARGETS[@]}"; do
        if [ -d "$t" ]; then
            TARGETS+=("$t")
        else
            echo "Warning: $t does not exist, skipping"
        fi
    done
fi

if [ ${#TARGETS[@]} -eq 0 ]; then
    echo "Usage: $0 <target-repo-path> [target2] [...] [options]"
    echo ""
    echo "Options:"
    echo "  --dry-run       Show what would be copied without making changes"
    echo "  --commit        Auto-commit changes in target repo after sync"
    echo "  --skills-only   Only sync skills (no memory, hooks, settings)"
    echo "  --memory-only   Only sync memory files"
    echo "  --hooks-only    Only sync hooks"
    echo "  --all           Sync to all known target projects"
    echo ""
    echo "Known targets (for --all):"
    for t in "${KNOWN_TARGETS[@]}"; do
        echo "  $t"
    done
    echo ""
    echo "Examples:"
    echo "  $0 ~/ng-robot"
    echo "  $0 ~/ng-robot ~/adobe-automat --commit"
    echo "  $0 --all --dry-run"
    exit 1
fi

# --- Helper: sync one file ---
sync_file() {
    local source_file="$1"
    local target_file="$2"
    local label="$3"
    local make_exec="${4:-false}"

    [ -f "$source_file" ] || return 0

    if [ -f "$target_file" ]; then
        if diff -q "$source_file" "$target_file" > /dev/null 2>&1; then
            echo "  [=] $label (unchanged)"
            return 0
        fi
        echo "  [U] $label (updated)"
    else
        echo "  [+] $label (new)"
    fi

    if [ "$DRY_RUN" = false ]; then
        mkdir -p "$(dirname "$target_file")"
        cp "$source_file" "$target_file"
        [ "$make_exec" = true ] && chmod +x "$target_file"
    fi
    return 1  # signal: file was changed
}

# --- Sync to each target ---
total_changed=0

for TARGET_REPO in "${TARGETS[@]}"; do
    TARGET_REPO="$(cd "$TARGET_REPO" 2>/dev/null && pwd)" || {
        echo "Error: Target '$TARGET_REPO' does not exist, skipping"
        continue
    }
    TARGET_CLAUDE="$TARGET_REPO/.claude"
    changed=0

    echo ""
    echo "=========================================="
    echo "Target: $TARGET_REPO"
    [ "$DRY_RUN" = true ] && echo "Mode:   DRY RUN"
    echo "=========================================="

    # --- Skills ---
    if [ "$SYNC_SKILLS" = true ]; then
        echo ""
        echo "--- Skills ---"
        mkdir -p "$TARGET_CLAUDE/skills"

        for skill_dir in "$SOURCE_DIR/skills"/*/; do
            [ -d "$skill_dir" ] || continue
            skill_name="$(basename "$skill_dir")"

            for source_file in "$skill_dir"*; do
                [ -f "$source_file" ] || continue
                filename="$(basename "$source_file")"
                target_file="$TARGET_CLAUDE/skills/$skill_name/$filename"

                sync_file "$source_file" "$target_file" "$skill_name/$filename" || ((changed++))
            done
        done
    fi

    # --- Memory ---
    if [ "$SYNC_MEMORY" = true ]; then
        echo ""
        echo "--- Memory ---"
        mkdir -p "$TARGET_CLAUDE/memory"

        for mem_file in "${SYNC_MEMORY_FILES[@]}"; do
            sync_file "$SOURCE_DIR/memory/$mem_file" "$TARGET_CLAUDE/memory/$mem_file" "$mem_file" || ((changed++))
        done
    fi

    # --- Hooks ---
    if [ "$SYNC_HOOKS" = true ] && [ -d "$SOURCE_DIR/hooks" ]; then
        echo ""
        echo "--- Hooks ---"
        mkdir -p "$TARGET_CLAUDE/hooks"

        for hook_file in "$SOURCE_DIR/hooks"/*; do
            [ -f "$hook_file" ] || continue
            filename="$(basename "$hook_file")"
            sync_file "$hook_file" "$TARGET_CLAUDE/hooks/$filename" "$filename" "true" || ((changed++))
        done
    fi

    # --- Settings ---
    if [ "$SYNC_SETTINGS" = true ]; then
        echo ""
        echo "--- Settings ---"
        sync_file "$SOURCE_DIR/settings.json" "$TARGET_CLAUDE/settings.json" "settings.json" || ((changed++))
    fi

    # --- Summary for this target ---
    echo ""
    if [ "$changed" -eq 0 ]; then
        echo "=> Everything is up to date."
    else
        if [ "$DRY_RUN" = true ]; then
            echo "=> $changed file(s) would be updated."
        else
            echo "=> $changed file(s) synced."

            if [ "$AUTO_COMMIT" = true ]; then
                echo "--- Committing ---"
                cd "$TARGET_REPO"
                git add .claude/
                git commit -m "Sync orchestration system from STOPA" || echo "Nothing to commit."
            fi
        fi
    fi

    ((total_changed += changed))
done

# --- Grand total ---
echo ""
echo "=========================================="
echo "Total: ${#TARGETS[@]} target(s), $total_changed file(s) changed"
[ "$DRY_RUN" = true ] && echo "(dry run — no changes made)"
echo "=========================================="
