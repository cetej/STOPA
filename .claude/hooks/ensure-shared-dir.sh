#!/usr/bin/env bash
# SessionStart hook: ensure shared directories exist for multi-agent coordination.
#
# CORAL pattern (arXiv:2604.01658): agents share knowledge via filesystem,
# not message passing. This hook creates the shared directories so skills
# don't need to mkdir -p at runtime.
#
# Directories:
#   intermediate/           — per-skill temporary state (post-it pattern)
#   intermediate/shared/    — cross-agent shared notes (CORAL public dir equivalent)
#   optstate/               — per-skill optimizer state (RCL-inspired)
#   outcomes/               — per-run outcome records (RCL-inspired)
#   failures/               — per-failure HERA records
#
# Profile: minimal+ (always runs, <5ms)

# Anchor to project root via script location — prevents CWD-dependent writes
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
MEMORY_DIR="$PROJECT_ROOT/.claude/memory"

# Core directories (always needed)
mkdir -p "$MEMORY_DIR/intermediate"
mkdir -p "$MEMORY_DIR/intermediate/shared"
mkdir -p "$MEMORY_DIR/optstate"
mkdir -p "$MEMORY_DIR/outcomes"
mkdir -p "$MEMORY_DIR/failures"
mkdir -p "$MEMORY_DIR/wiki/entities"
mkdir -p "$MEMORY_DIR/wiki/sources"

# Touch shared notes file if it doesn't exist (append-only by convention)
if [ ! -f "$MEMORY_DIR/intermediate/shared/notes.md" ]; then
  cat > "$MEMORY_DIR/intermediate/shared/notes.md" << 'EOF'
# Shared Agent Notes (CORAL-inspired)

Append-only file for cross-agent knowledge sharing.
Format: `## Agent <name> — <timestamp>` followed by bullet points.
Read by orchestrator between sweeps/rounds to inject discovered patterns.

---
EOF
fi

# Cleanup stale post-it files (>24h old, per memory-files.md rules)
if [ -d "$MEMORY_DIR/intermediate" ]; then
  find "$MEMORY_DIR/intermediate" -maxdepth 1 -name "*-state.md" -mmin +1440 -delete 2>/dev/null || true
fi

# Report nothing — silent hook
