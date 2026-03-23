# Shared Memory — Learnings

**MIGRATED**: Learnings are now stored as per-file YAML frontmatter in `.claude/memory/learnings/`.

## How to access

1. **Always-read**: `.claude/memory/learnings/critical-patterns.md` (top 8-10 patterns)
2. **Grep-first**: `grep -r "component: <X>" .claude/memory/learnings/` or `grep -r "tags:.*<keyword>" .claude/memory/learnings/`
3. **Read matched files** only

## How to write

Use `/scribe learning` — creates a new file in `learnings/` with YAML frontmatter (date, type, severity, component, tags).

See `/scribe` skill for full schema.
