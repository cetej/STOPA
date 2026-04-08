---
name: compile
variant: compact
description: Condensed compile for repeat invocations within session. Use full SKILL.md for first invocation.
---

# /compile — Compact (Session Re-invocation)

Synthesize learnings → thematic wiki articles. Read-optimized knowledge from write-optimized atoms.

## Pipeline

1. **Refresh manifest** → `python scripts/build-component-indexes.py` (or manual Glob)
2. **Load sources** → learnings/*.md + critical-patterns + decisions + key-facts + raw/*.md
3. **Incremental check** → compare .compile-state.json; >50% changed → fallback to --full
4. **Cluster** → group by component, sub-cluster by tag Jaccard (>0.2), merge <3 learnings into nearest
5. **Contradictions & gaps** → intra-cluster opposition scan + cross-component coverage check
6. **Generate articles** → 150-line cap, narrative synthesis (not bullet dump), every claim cites (ref:)
7. **Quality gate** → Haiku reviewer per article (fail-closed on accuracy_concerns). Skip on ≤2 incremental articles.
8. **INDEX.md** → 90-line cap, articles table, health score, Start Here section
9. **Compile state** → .compile-state.json with article→learnings mapping
10. **Briefings** → per-role filtered briefings (orchestration, research, code-quality, memory). 2000-word cap.
11. **News bridge** → scan news.md ACTION items, propose unmatched as learnings
12. **Research synthesis** → (opt-in --include-research) cluster research reports, generate cross-report synthesis

## Critical Rules

- Synthesize, don't list — narrative > bullet dump
- 100% coverage — every active learning in exactly one article
- Citation mandatory — `(ref: filename.md)` on every claim
- 150-line article cap, 90-line INDEX cap
- Incremental default — full only on first run or >50% changed
- Never modify source files (learnings, decisions, key-facts)
- Show clustering plan BEFORE generating articles
