---
generated: 2026-04-04
cluster: memory-architecture
sources: 18
last_updated: 2026-04-18
---

# Memory Architecture

> **TL;DR**: Write-time gating (filter before storing) structurally outperforms read-time filtering — at 8:1 distractor ratio, RAG collapses to 0% while gated store holds 100%. BM25-scored retrieval with metadata weights replaces raw grep and surfaces critical learnings over stale auto-patterns.

## Overview

STOPA's memory system evolved from simple file storage to a gated, scored, multi-layer architecture. The most impactful insight is that write-time gating — filtering information BEFORE storing it — is structurally superior to read-time filtering. At an 8:1 distractor ratio, RAG collapses to 0% accuracy while a gated store maintains 100%. The implementation uses a salience gate (source × novelty × reliability) with mandatory dedup and source reputation fields (ref: 2026-03-30-write-time-gating-salience.md).

BM25-inspired retrieval (`scripts/memory-search.py`) replaces raw grep for learnings lookup. IDF (rare terms like "pipeline" weight more than common ones like "harness"), term frequency saturation (k1=1.2), and length normalization (b=0.75) combine with STOPA metadata (severity × source × confidence × impact × time decay). A single query across learnings/, critical-patterns.md, decisions.md, and key-facts.md returns ranked results with zero GPU/embedding dependencies (ref: 2026-04-05-bm25-memory-search.md).

For multi-model environments (Haiku/Sonnet/Opus), agent-agnostic memory via contrastive trajectory distillation runs multiple agents on the same task, contrasts their reasoning paths, and distills shared constraints. The resulting memory improves all agents, not just the one that generated it (ref: 2026-03-29-memcollab-agent-agnostic-memory.md).

Cross-project memory transfer is now designed as a two-tier system: shared knowledge (critical-patterns.md + wiki articles = universal) syncs via the distribution script, while project-specific learnings stay local in auto-memory. This replaces the earlier open gap about cross-project mechanics (ref: 2026-04-07-cross-project-memory-design.md).

A counterintuitive finding from streaming video benchmarks: simple sliding-window recency (last N items) matches or beats complex memory accumulation in time-sensitive tasks. More history can actually hurt real-time perception even when it helps recall. This suggests STOPA should bias toward recency for context loading, using full history only when explicitly needed for longitudinal analysis (ref: 2026-04-08-recency-beats-complex-memory.md).

Checkpoint versioning is a foundational anti-pattern prevention: never overwrite checkpoints without archiving. Version frequently (especially before scope changes), include task list + technical findings + resume prompt, and archive rather than delete (ref: 2026-03-24-checkpoint-versioning.md). Living memory (MIA arXiv:2604.04503) beats static RAG by +31% avg across 11 benchmarks — a 7B model with living memory outperforms a 32B without it by 18%. The mechanism is bidirectional conversion between parametric and non-parametric memory plus test-time learning. This empirically validates STOPA's write-time gating approach (ref: 2026-04-08-living-memory-over-static-retrieval.md). The parametric ↔ non-parametric bridge maps to STOPA as: CLAUDE.md/behavioral-genome.md (parametric) ↔ learnings/*.md/critical-patterns.md (non-parametric). The gap is a reverse demote mechanism — stale rules in critical-patterns.md should move back to non-parametric for re-evaluation (ref: 2026-04-08-parametric-nonparametric-memory-bridge.md). Acemoglu Theorem 3 formalizes why local aggregators beat global: a global aggregator necessarily degrades ≥1 knowledge dimension. STOPA's implementation uses `skill_scope:` field for local graduation to `skills/<name>/learned-rules.md` and circular validation detection in learning-admission.py (ref: 2026-04-09-local-aggregator-beats-global.md).

Harrison Chase (LangChain) frames memory as harness, not plugin: a closed harness means lost memory. STOPA is 80% open (git-backed files, markdown format), but three risk points remain: server-side compaction (invisible to git), auto-memory stored outside git tracking, and SKILL.md format lock-in. Six mitigations proposed: git-track auto-memory, export hooks for compaction events, format-neutral learning schema, memory portability tests, multi-harness sync protocol, and sovereignty audit in /evolve (ref: 2026-04-11-memory-sovereignty-open-harness.md).

AutoDream (/dream) coexists with STOPA's structured memory: dream acts as janitor (cleanup, consolidation), while /scribe acts as architect (structured writes with YAML frontmatter). The key boundary is protecting YAML frontmatter from dream's modifications (ref: 2026-03-26-autodream-coexistence.md).

Memory Caching (MC paper) formalizes a universal pattern STOPA already implements implicitly: segment long stream → compress state at boundary → cache checkpoint → gate retrieval by query. Session checkpoints and `hybrid-retrieve.py` are informal instances. The formal design calls for GRM-style query-dependent gating (query × cached-state similarity) when choosing which checkpoints to surface, rather than flat recency ordering (ref: 2026-04-18-mc-checkpoint-caching-retrieval-pattern.md). The same framework exposes STOPA retrieval as a complexity knob: grep = O(1), BM25 = O(log L), graph walk = O(L) — interpolated as O(NL) where N = cached segments. Practical rule: shallow tasks (tier=light) stay grep-only; deep tasks always use hybrid (BM25 + graph). Don't invoke graph walk when grep already returns 3+ matches — wasted quadratic expansion (ref: 2026-04-18-retrieval-depth-knob-complexity-interpolation.md).

## Key Rules

1. **Write-time gating over read-time filtering**: filter before storing (ref: 2026-03-30-write-time-gating-salience.md)
2. **Mandatory source field**: tracks reputation for retrieval scoring (ref: 2026-03-30-write-time-gating-salience.md)
3. **BM25 retrieval over raw grep**: use memory-search.py for ranked, metadata-weighted results (ref: 2026-04-05-bm25-memory-search.md)
4. **Contrastive distillation for cross-model memory**: run multiple agents, distill shared constraints (ref: 2026-03-29-memcollab-agent-agnostic-memory.md)
5. **Dream = janitor, Scribe = architect**: protect YAML frontmatter (ref: 2026-03-26-autodream-coexistence.md)
6. **Cross-project: sync universal, keep local local**: critical-patterns + wiki sync; learnings stay per-project (ref: 2026-04-07-cross-project-memory-design.md)
7. **Recency bias for context loading**: sliding-window recency ≥ complex accumulation in time-sensitive tasks (ref: 2026-04-08-recency-beats-complex-memory.md)
8. **Checkpoint versioning: archive, never overwrite**: version before scope changes, include resume prompt (ref: 2026-03-24-checkpoint-versioning.md)
9. **Living memory beats static RAG**: compressed trajectory storage + evolution hooks > append-only history (ref: 2026-04-08-living-memory-over-static-retrieval.md)
10. **Add reverse demote mechanism**: stale critical-patterns.md rules should return to non-parametric for re-evaluation (ref: 2026-04-08-parametric-nonparametric-memory-bridge.md)
11. **Local graduation over global**: skill_scope field routes learnings to local learned-rules.md (ref: 2026-04-09-local-aggregator-beats-global.md)
12. **Retrieval depth matches task tier**: grep for light, BM25 for standard, hybrid+graph for deep — don't over-retrieve when grep already hits 3+ (ref: 2026-04-18-retrieval-depth-knob-complexity-interpolation.md)
13. **Query-dependent checkpoint gating**: surface checkpoints by query × state similarity, not flat recency (ref: 2026-04-18-mc-checkpoint-caching-retrieval-pattern.md)

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

- GAP: Memory sovereignty mitigations (3 risk points identified, not yet implemented) (ref: 2026-04-11-memory-sovereignty-open-harness.md)
- ~~GAP: Cross-project memory transfer~~ — RESOLVED: two-tier design (universal sync + local learnings) (ref: 2026-04-07-cross-project-memory-design.md)

## Related Articles

- See also: [orchestration-infrastructure](orchestration-infrastructure.md) — context management and sessions
- See also: [skill-design](skill-design.md) — impact scoring for learning graduation

## Source Learnings

| File | Date | Severity | Summary |
|------|------|----------|---------|
| [2026-04-05-bm25-memory-search](../learnings/2026-04-05-bm25-memory-search.md) | 2026-04-05 | high | BM25 replaces grep: IDF + saturation + length norm + metadata weights |
| [2026-04-07-cross-project-memory-design](../learnings/2026-04-07-cross-project-memory-design.md) | 2026-04-07 | high | Two-tier: universal sync + local learnings |
| [2026-04-08-recency-beats-complex-memory](../learnings/2026-04-08-recency-beats-complex-memory.md) | 2026-04-08 | medium | Sliding-window recency ≥ complex accumulation |
| [2026-03-30-write-time-gating-salience](../learnings/2026-03-30-write-time-gating-salience.md) | 2026-03-30 | high | Write-time gating holds 100% at 8:1 distractor ratio |
| [2026-03-30-calm-semantic-bandwidth](../learnings/2026-03-30-calm-semantic-bandwidth.md) | 2026-03-30 | medium | Semantic bandwidth limits for memory retrieval |
| [2026-03-29-memcollab-agent-agnostic-memory](../learnings/2026-03-29-memcollab-agent-agnostic-memory.md) | 2026-03-29 | high | Agent-agnostic memory via contrastive distillation |
| [2026-03-26-autodream-coexistence](../learnings/2026-03-26-autodream-coexistence.md) | 2026-03-26 | high | Dream=janitor, Scribe=architect coexistence |
| [2026-03-24-checkpoint-versioning](../learnings/2026-03-24-checkpoint-versioning.md) | 2026-03-24 | high | Never overwrite checkpoints; archive with task list + resume prompt |
| [2026-04-08-living-memory-over-static-retrieval](../learnings/2026-04-08-living-memory-over-static-retrieval.md) | 2026-04-08 | high | Living memory +31% over RAG; validates write-time gating |
| [2026-04-08-parametric-nonparametric-memory-bridge](../learnings/2026-04-08-parametric-nonparametric-memory-bridge.md) | 2026-04-08 | high | Bidirectional parametric↔non-parametric conversion; needs reverse demote |
| [2026-04-09-local-aggregator-beats-global](../learnings/2026-04-09-local-aggregator-beats-global.md) | 2026-04-09 | high | Acemoglu Theorem 3: local aggregators preserve knowledge better than global |
| [2026-04-11-memory-sovereignty-open-harness](../learnings/2026-04-11-memory-sovereignty-open-harness.md) | 2026-04-11 | high | Memory=harness, not plugin; 3 risk points, 6 mitigations |
| [2026-04-04-gap-cross-project-memory](../learnings/2026-04-04-gap-cross-project-memory.md) | 2026-04-04 | medium | GAP: cross-project memory sharing design |
| [2026-04-12-evolve-must-verify-current-state](../learnings/2026-04-12-evolve-must-verify-current-state.md) | 2026-04-12 | high | /evolve must verify filesystem before recommending |
| [2026-04-12-queries-back-to-wiki-compounding](../learnings/2026-04-12-queries-back-to-wiki-compounding.md) | 2026-04-12 | high | Wiki queries compound knowledge over time |
| [2026-04-18-mc-checkpoint-caching-retrieval-pattern](../learnings/2026-04-18-mc-checkpoint-caching-retrieval-pattern.md) | 2026-04-18 | medium | Memory Caching formalizes segment → compress → checkpoint → gate; use query-dependent gating not flat recency |
| [2026-04-18-retrieval-depth-knob-complexity-interpolation](../learnings/2026-04-18-retrieval-depth-knob-complexity-interpolation.md) | 2026-04-18 | medium | Retrieval complexity knob: grep O(1) → BM25 O(log L) → graph O(L); shallow tasks stay cheap |
