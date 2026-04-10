#!/bin/bash
# sync-orchestration.sh — Sync .claude/ orchestration system to target projects
#
# Usage:
#   ./scripts/sync-orchestration.sh <target1> [target2] [target3] [options]
#   ./scripts/sync-orchestration.sh ~/ng-robot ~/adobe-automat --dry-run
#   ./scripts/sync-orchestration.sh ~/ng-robot --commit --skills-only
#   ./scripts/sync-orchestration.sh --all --dry-run
#   ./scripts/sync-orchestration.sh --all --dry-run --json
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
JSON_OUTPUT=false

for arg in "$@"; do
    case "$arg" in
        --dry-run) DRY_RUN=true ;;
        --commit) AUTO_COMMIT=true ;;
        --json) JSON_OUTPUT=true ;;
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
            echo "Warning: $t does not exist, skipping" >&2
        fi
    done
fi

if [ ${#TARGETS[@]} -eq 0 ]; then
    echo "Usage: $0 <target-repo-path> [target2] [...] [options]"
    echo ""
    echo "Options:"
    echo "  --dry-run       Show what would be copied without making changes"
    echo "  --commit        Auto-commit changes in target repo after sync"
    echo "  --json          Output results as JSON (for agent consumption)"
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

# --- JSON collection ---
JSON_TARGETS=""  # accumulated JSON target objects

# --- Helper: sync one file ---
# Sets CURRENT_TARGET_CHANGES as side-effect when file changes
CURRENT_TARGET_CHANGES=""

sync_file() {
    local source_file="$1"
    local target_file="$2"
    local label="$3"
    local make_exec="${4:-false}"

    [ -f "$source_file" ] || return 0

    local status=""
    if [ -f "$target_file" ]; then
        if diff -q "$source_file" "$target_file" > /dev/null 2>&1; then
            [ "$JSON_OUTPUT" = false ] && echo "  [=] $label (unchanged)"
            return 0
        fi
        status="updated"
        [ "$JSON_OUTPUT" = false ] && echo "  [U] $label (updated)"
    else
        status="new"
        [ "$JSON_OUTPUT" = false ] && echo "  [+] $label (new)"
    fi

    # Collect for JSON output
    [ -n "$CURRENT_TARGET_CHANGES" ] && CURRENT_TARGET_CHANGES="$CURRENT_TARGET_CHANGES,"
    CURRENT_TARGET_CHANGES="${CURRENT_TARGET_CHANGES}{\"status\":\"$status\",\"file\":\"$label\"}"

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
        echo "Error: Target '$TARGET_REPO' does not exist, skipping" >&2
        continue
    }
    TARGET_CLAUDE="$TARGET_REPO/.claude"
    changed=0
    CURRENT_TARGET_CHANGES=""

    if [ "$JSON_OUTPUT" = false ]; then
        echo ""
        echo "=========================================="
        echo "Target: $TARGET_REPO"
        [ "$DRY_RUN" = true ] && echo "Mode:   DRY RUN"
        echo "=========================================="
    fi

    # --- Skills ---
    if [ "$SYNC_SKILLS" = true ]; then
        [ "$JSON_OUTPUT" = false ] && echo "" && echo "--- Skills ---"
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
        [ "$JSON_OUTPUT" = false ] && echo "" && echo "--- Memory ---"
        mkdir -p "$TARGET_CLAUDE/memory"

        for mem_file in "${SYNC_MEMORY_FILES[@]}"; do
            sync_file "$SOURCE_DIR/memory/$mem_file" "$TARGET_CLAUDE/memory/$mem_file" "$mem_file" || ((changed++))
        done

        # --- Learnings (individual YAML files) ---
        # Only sync general learnings (no skill_scope or skill_scope covers 3+ skills)
        # Project-specific learnings stay in STOPA
        if [ -d "$SOURCE_DIR/memory/learnings" ]; then
            [ "$JSON_OUTPUT" = false ] && echo "" && echo "--- Learnings ---"
            mkdir -p "$TARGET_CLAUDE/memory/learnings"

            for learning_file in "$SOURCE_DIR/memory/learnings"/*.md; do
                [ -f "$learning_file" ] || continue
                filename="$(basename "$learning_file")"

                # Skip project-specific learnings (those with narrow skill_scope)
                # Sync only: no skill_scope (global) OR skill_scope with 3+ entries (cross-cutting)
                if grep -q "^skill_scope:" "$learning_file" 2>/dev/null; then
                    # Count skills in scope — skip if 1-2 (too specific)
                    scope_count=$(grep "^skill_scope:" "$learning_file" | grep -o "," | wc -l)
                    scope_count=$((scope_count + 1))
                    if [ "$scope_count" -lt 3 ]; then
                        [ "$JSON_OUTPUT" = false ] && echo "  [-] learnings/$filename (skill-specific, skipped)"
                        continue
                    fi
                fi

                sync_file "$learning_file" "$TARGET_CLAUDE/memory/learnings/$filename" "learnings/$filename" || ((changed++))
            done

            # Also sync critical-patterns.md (always-read, max 10 entries)
            sync_file "$SOURCE_DIR/memory/critical-patterns.md" "$TARGET_CLAUDE/memory/critical-patterns.md" "critical-patterns.md" || ((changed++))
        fi
    fi

    # --- Hooks ---
    if [ "$SYNC_HOOKS" = true ] && [ -d "$SOURCE_DIR/hooks" ]; then
        [ "$JSON_OUTPUT" = false ] && echo "" && echo "--- Hooks ---"
        mkdir -p "$TARGET_CLAUDE/hooks"

        for hook_file in "$SOURCE_DIR/hooks"/*; do
            [ -f "$hook_file" ] || continue
            filename="$(basename "$hook_file")"
            sync_file "$hook_file" "$TARGET_CLAUDE/hooks/$filename" "$filename" "true" || ((changed++))
        done
    fi

    # --- Settings ---
    if [ "$SYNC_SETTINGS" = true ]; then
        [ "$JSON_OUTPUT" = false ] && echo "" && echo "--- Settings ---"
        sync_file "$SOURCE_DIR/settings.json" "$TARGET_CLAUDE/settings.json" "settings.json" || ((changed++))
    fi

    # --- Collect JSON for this target ---
    [ -n "$JSON_TARGETS" ] && JSON_TARGETS="$JSON_TARGETS,"
    JSON_TARGETS="${JSON_TARGETS}{\"path\":\"$TARGET_REPO\",\"files_changed\":$changed,\"changes\":[$CURRENT_TARGET_CHANGES]}"

    # --- Summary for this target ---
    if [ "$JSON_OUTPUT" = false ]; then
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
    fi

    ((total_changed += changed))
done

# --- Output ---
if [ "$JSON_OUTPUT" = true ]; then
    echo "{\"targets\":[$JSON_TARGETS],\"total_targets\":${#TARGETS[@]},\"total_changed\":$total_changed,\"dry_run\":$DRY_RUN}"
else
    echo ""
    echo "=========================================="
    echo "Total: ${#TARGETS[@]} target(s), $total_changed file(s) changed"
    [ "$DRY_RUN" = true ] && echo "(dry run — no changes made)"
    echo "=========================================="
fi
