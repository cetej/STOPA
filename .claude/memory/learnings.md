# Shared Memory — Learnings

**MIGRATED**: Learnings are now stored as per-file YAML frontmatter in `.claude/memory/learnings/`.

## How to access

1. **Always-read**: `.claude/memory/learnings/critical-patterns.md` (top 8-10 patterns)
2. **Grep-first**: `grep -r "component: <X>" .claude/memory/learnings/` or `grep -r "tags:.*<keyword>" .claude/memory/learnings/`
3. **Read matched files** only
4. **When a learning is retrieved and applied**: increment its `uses:` counter in YAML frontmatter

## How to write

Use `/scribe learning` — creates a new file in `learnings/` with YAML frontmatter (date, type, severity, component, tags, summary, uses, harmful_uses).

## Counter tracking (ACE-inspired)

- `uses: N` — how many times this learning was retrieved and applied
- `harmful_uses: N` — how many times applying this learning led to a bad outcome (tagged by /critic)
- High-performing: `uses > 5` AND `harmful_uses < 2`
- Problematic: `harmful_uses >= uses` AND `harmful_uses > 0` → flag for removal during maintenance
- Old learnings without counters remain valid (backward compatible)

See `/scribe` skill for full schema.
