# ADR 0013: Wiki Synthesis Layer

**Date**: 2026-04-04
**Status**: IMPLEMENTING
**Component**: memory
**Tags**: memory, synthesis, retrieval, wiki

## Context

STOPA memory system accumulates atomic learnings (52+ files) but retrieval effectiveness is ~30%:
- 21 learnings not indexed (invisible to grep-first retrieval)
- 70% have `uses: 0` (never retrieved in practice)
- Keyword mismatch causes ~30-40% retrieval misses (synonym problem)
- No synthesis layer between atomic learnings and the 10-slot `critical-patterns.md`
- Session onboarding requires 5-10 tool calls to build context from scattered files

Inspired by Karpathy "Second Brain" pattern (raw → wiki → outputs) and Spisak's implementation guide.

## Decision

Add a wiki compilation layer at `.claude/memory/wiki/` via new `/compile` skill:

1. **Cluster** learnings by component + tag Jaccard similarity
2. **Synthesize** each cluster into a narrative wiki article with citations
3. **Maintain** `wiki/INDEX.md` as always-readable onboarding entry point
4. **Track** incremental state via `.compile-state.json` for efficient rebuilds
5. **Integrate** with `/evolve` (wiki freshness check), `/status` (wiki_health), `/checkpoint` (INDEX.md reference)

### Architecture: 3-Layer Knowledge Pyramid

```
Layer 3: critical-patterns.md    (10 entries, always-loaded, ~100 tokens)
Layer 2: wiki/ articles          (5-8 articles, read on-demand, ~200 tokens each)
Layer 1: learnings/ files        (52+ files, source of truth, grep-first)
```

Each layer compresses the previous ~10x. Sessions choose appropriate detail level.

## Alternatives Considered

1. **Integrate into `/evolve`** — Rejected: evolve is audit/prune (destructive), compile is synthesis (constructive). Different responsibilities, different frequencies.
2. **Vector-based retrieval (hippocampus)** — Complementary, not competing. ADR 0012 hippocampus handles associative activation; wiki handles human-readable synthesis. Both can coexist.
3. **Just fix indexes** — Insufficient. Indexes list but don't synthesize. The keyword mismatch problem needs narrative that naturally contains synonyms.

## Consequences

- **Positive**: Better retrieval coverage, faster onboarding, contradiction detection, knowledge gap identification
- **Negative**: Additional maintenance artifact (wiki can go stale), ~8K tokens for full compile run
- **Mitigated**: Incremental builds, staleness detection in `/evolve`, compile-state tracking
