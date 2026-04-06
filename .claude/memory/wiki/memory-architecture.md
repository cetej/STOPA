---
generated: 2026-04-04
cluster: memory-architecture
sources: 7
last_updated: 2026-04-07
---

# Memory Architecture

> **TL;DR**: Write-time gating (filter before storing) structurally outperforms read-time filtering — at 8:1 distractor ratio, RAG collapses to 0% while gated store holds 100%. BM25-scored retrieval with metadata weights replaces raw grep and surfaces critical learnings over stale auto-patterns.

## Overview

STOPA's memory system evolved from simple file storage to a gated, scored, multi-layer architecture. The most impactful insight is that write-time gating — filtering information BEFORE storing it — is structurally superior to read-time filtering. At an 8:1 distractor ratio, RAG collapses to 0% accuracy while a gated store maintains 100%. The implementation uses a salience gate (source × novelty × reliability) with mandatory dedup and source reputation fields (ref: 2026-03-30-write-time-gating-salience.md).

BM25-inspired retrieval (`scripts/memory-search.py`) replaces raw grep for learnings lookup. IDF (rare terms like "pipeline" weight more than common ones like "harness"), term frequency saturation (k1=1.2), and length normalization (b=0.75) combine with STOPA metadata (severity × source × confidence × impact × time decay). A single query across learnings/, critical-patterns.md, decisions.md, and key-facts.md returns ranked results with zero GPU/embedding dependencies (ref: 2026-04-05-bm25-memory-search.md).

For multi-model environments (Haiku/Sonnet/Opus), agent-agnostic memory via contrastive trajectory distillation runs multiple agents on the same task, contrasts their reasoning paths, and distills shared constraints. The resulting memory improves all agents, not just the one that generated it (ref: 2026-03-29-memcollab-agent-agnostic-memory.md).

AutoDream (/dream) coexists with STOPA's structured memory: dream acts as janitor (cleanup, consolidation), while /scribe acts as architect (structured writes with YAML frontmatter). The key boundary is protecting YAML frontmatter from dream's modifications (ref: 2026-03-26-autodream-coexistence.md).

## Key Rules

1. **Write-time gating over read-time filtering**: filter before storing (ref: 2026-03-30-write-time-gating-salience.md)
2. **Mandatory source field**: tracks reputation for retrieval scoring (ref: 2026-03-30-write-time-gating-salience.md)
3. **BM25 retrieval over raw grep**: use memory-search.py for ranked, metadata-weighted results (ref: 2026-04-05-bm25-memory-search.md)
4. **Contrastive distillation for cross-model memory**: run multiple agents, distill shared constraints (ref: 2026-03-29-memcollab-agent-agnostic-memory.md)
5. **Dream = janitor, Scribe = architect**: protect YAML frontmatter (ref: 2026-03-26-autodream-coexistence.md)

## Patterns

### Do
- Apply salience gate (source × novelty × reliability) before writing learnings (ref: 2026-03-30-write-time-gating-salience.md)
- Use `scripts/memory-search.py "<query>"` for multi-source ranked retrieval (ref: 2026-04-05-bm25-memory-search.md)
- Dedup against existing learnings at write time (ref: 2026-03-30-write-time-gating-salience.md)

### Don't
- Rely on read-time filtering alone for noise resistance (ref: 2026-03-30-write-time-gating-salience.md)
- Let AutoDream modify YAML frontmatter fields (ref: 2026-03-26-autodream-coexistence.md)
- Use raw grep for multi-source learnings lookup — BM25 ranking matters at 70+ documents (ref: 2026-04-05-bm25-memory-search.md)

## Open Questions

- GAP: No documented mechanics for cross-project memory transfer between STOPA and target projects — which learnings are universal vs project-local? (ref: 2026-04-04-gap-cross-project-memory.md)

## Related Articles

- See also: [orchestration-infrastructure](orchestration-infrastructure.md) — context management and sessions
- See also: [skill-design](skill-design.md) — impact scoring for learning graduation

## Source Learnings

| File | Date | Severity | Summary |
|------|------|----------|---------|
| [2026-04-05-bm25-memory-search](../learnings/2026-04-05-bm25-memory-search.md) | 2026-04-05 | high | BM25 replaces grep: IDF + saturation + length norm + metadata weights |
| [2026-04-04-gap-cross-project-memory](../learnings/2026-04-04-gap-cross-project-memory.md) | 2026-04-04 | medium | GAP: no mechanics for cross-project memory transfer |
| [2026-03-30-write-time-gating-salience](../learnings/2026-03-30-write-time-gating-salience.md) | 2026-03-30 | high | Write-time gating holds 100% at 8:1 distractor ratio |
| [2026-03-30-calm-semantic-bandwidth](../learnings/2026-03-30-calm-semantic-bandwidth.md) | 2026-03-30 | medium | Semantic bandwidth limits for memory retrieval |
| [2026-03-29-memcollab-agent-agnostic-memory](../learnings/2026-03-29-memcollab-agent-agnostic-memory.md) | 2026-03-29 | high | Agent-agnostic memory via contrastive distillation |
| [2026-03-26-autodream-coexistence](../learnings/2026-03-26-autodream-coexistence.md) | 2026-03-26 | high | Dream=janitor, Scribe=architect coexistence |
| [2026-03-30-calm-semantic-bandwidth](../learnings/2026-03-30-calm-semantic-bandwidth.md) | 2026-03-30 | medium | Semantic bandwidth limits for memory retrieval |
