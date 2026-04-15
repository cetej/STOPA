---
date: 2026-04-07
type: architecture
severity: high
component: memory
tags: [cross-project, sync, distribution, memory-transfer]
summary: "Cross-project memory design: sync critical-patterns.md + wiki/ articles (universal knowledge), NOT learnings/ (project-specific). Two-tier: shared knowledge via sync script, project-specific via auto-memory."
source: auto_pattern
uses: 1
harmful_uses: 0
successful_uses: 0
confidence: 1.0
supersedes: 2026-04-04-gap-cross-project-memory.md
verify_check: "Grep('SYNC_MEMORY_FILES', path='scripts/sync-orchestration.sh') → 1+ matches"
---

## Cross-Project Memory Transfer Design

### Current State

`sync-orchestration.sh` copies these memory files to target projects:
- `learnings.md` (pointer file), `budget.md`, `decisions.md`, `decisions-archive.md`, `budget-archive.md`, `news.md`

**NOT copied**: `learnings/` directory (per-file YAML), `wiki/` articles, `critical-patterns.md`, `key-facts.md`

### Two-Tier Memory Model

| Tier | What | Where | Sync method |
|------|------|-------|-------------|
| **Universal** | Orchestration knowledge applicable to ALL projects | STOPA → targets via sync script | `sync-orchestration.sh --memory` |
| **Project-specific** | Project-local learnings, configs, key-facts | Auto-memory (`~/.claude/projects/<path>/memory/`) | Manual via `/handoff` |

### What SHOULD Be Synced (universal knowledge)

1. **critical-patterns.md** — top 10 always-read patterns (already validated, high confidence)
2. **wiki/ articles** — synthesized knowledge about orchestration, hooks, skills
3. **news.md** — ecosystem updates relevant to all projects

### What Should NOT Be Synced

1. **learnings/** — too granular, project-specific context. Would create noise in target projects
2. **key-facts.md** — project-specific (stack, endpoints, env vars differ per project)
3. **state.md, checkpoint.md** — session-specific
4. **budget.md** — STOPA budget != NG-ROBOT budget (different task histories)

### Proposed Changes to sync-orchestration.sh

```bash
# Add to SYNC_MEMORY_FILES:
SYNC_MEMORY_FILES=(
    "critical-patterns.md"   # ADD: universal validated patterns
    "news.md"                # KEEP: ecosystem updates
    "decisions.md"           # KEEP: decision index
    "decisions-archive.md"   # KEEP: decision history
)

# Add wiki sync (new section):
if [ "$SYNC_MEMORY" = true ] && [ -d "$SOURCE_DIR/memory/wiki" ]; then
    mkdir -p "$TARGET_CLAUDE/memory/wiki"
    for wiki_file in "$SOURCE_DIR/memory/wiki"/*.md; do
        # sync wiki articles
    done
fi

# REMOVE from sync (project-specific):
# - learnings.md (pointer file without learnings/ dir is useless)
# - budget.md (per-project budgets)
# - budget-archive.md (per-project)
```

### Cross-Project Handoff (project-specific transfers)

When work spans STOPA → NG-ROBOT:
1. Use `/handoff` to save findings to TARGET project's auto-memory
2. Target auto-memory path: `~/.claude/projects/C--Users-stock-Documents-000-NGM-NG-ROBOT/memory/`
3. Checkpoint references must include full path to target memory file
4. This is manual by design — project-specific context needs human judgment about what transfers

### Implementation Priority

Medium — implement during next sync script maintenance. Current workaround (manual `/handoff`) works.
