---
generated: 2026-04-04
cluster: memory-architecture
sources: 5
last_updated: 2026-04-04
---

# Memory Architecture

> **TL;DR**: Write-time gating (filter before storing) structurally outperforms read-time filtering — at 8:1 distractor ratio, RAG collapses to 0% while gated store holds 100%. Agent-agnostic memory via contrastive distillation improves all model tiers.

## Overview

STOPA's memory system evolved from simple file storage to a gated, scored, multi-layer architecture. The most impactful insight is that write-time gating — filtering information BEFORE storing it — is structurally superior to read-time filtering. At an 8:1 distractor ratio, RAG collapses to 0% accuracy while a gated store maintains 100%. The implementation uses a salience gate (source × novelty × reliability) with mandatory dedup and source reputation fields (ref: 2026-03-30-write-time-gating-salience.md).

For multi-model environments (Haiku/Sonnet/Opus), agent-agnostic memory via contrastive trajectory distillation runs multiple agents on the same task, contrasts their reasoning paths, and distills shared constraints. The resulting memory improves all agents, not just the one that generated it (ref: 2026-03-29-memcollab-agent-agnostic-memory.md).

AutoDream (/dream) coexists with STOPA's structured memory: dream acts as janitor (cleanup, consolidation), while /scribe acts as architect (structured writes with YAML frontmatter). The key boundary is protecting YAML frontmatter from dream's modifications (ref: 2026-03-26-autodream-coexistence.md). Checkpoint versioning prevents data loss: never overwrite without archiving, version frequently, especially before scope changes (ref: checkpoint-versioning.md). Semantic bandwidth research suggests that memory retrieval efficiency has natural limits tied to how much structured knowledge can be transmitted per context token (ref: 2026-03-30-calm-semantic-bandwidth.md).

## Key Rules

1. **Write-time gating over read-time filtering**: filter before storing (ref: 2026-03-30-write-time-gating-salience.md)
2. **Mandatory source field**: tracks reputation for retrieval scoring (ref: 2026-03-30-write-time-gating-salience.md)
3. **Contrastive distillation for cross-model memory**: run multiple agents, distill shared constraints (ref: 2026-03-29-memcollab-agent-agnostic-memory.md)
4. **Dream = janitor, Scribe = architect**: protect YAML frontmatter (ref: 2026-03-26-autodream-coexistence.md)
5. **Never overwrite checkpoints**: archive before overwriting (ref: checkpoint-versioning.md)

## Patterns

### Do
- Apply salience gate (source × novelty × reliability) before writing learnings (ref: 2026-03-30-write-time-gating-salience.md)
- Dedup against existing learnings at write time (ref: 2026-03-30-write-time-gating-salience.md)
- Version checkpoints frequently, especially before scope changes (ref: checkpoint-versioning.md)

### Don't
- Rely on read-time filtering alone for noise resistance (ref: 2026-03-30-write-time-gating-salience.md)
- Let AutoDream modify YAML frontmatter fields (ref: 2026-03-26-autodream-coexistence.md)
- Overwrite checkpoints without archiving the previous version (ref: checkpoint-versioning.md)

## Open Questions

- GAP: No learnings about cross-project memory sharing mechanics — how should memory transfer between STOPA and target projects?

## Related Articles

- See also: [orchestration-infrastructure](orchestration-infrastructure.md) — context management and sessions
- See also: [skill-design](skill-design.md) — impact scoring for learning graduation

## Source Learnings

| File | Date | Severity | Summary |
|------|------|----------|---------|
| [2026-03-30-write-time-gating-salience](../learnings/2026-03-30-write-time-gating-salience.md) | 2026-03-30 | high | Write-time gating holds 100% at 8:1 distractor ratio |
| [2026-03-30-calm-semantic-bandwidth](../learnings/2026-03-30-calm-semantic-bandwidth.md) | 2026-03-30 | medium | Semantic bandwidth limits for memory retrieval |
| [2026-03-29-memcollab-agent-agnostic-memory](../learnings/2026-03-29-memcollab-agent-agnostic-memory.md) | 2026-03-29 | high | Agent-agnostic memory via contrastive distillation |
| [2026-03-26-autodream-coexistence](../learnings/2026-03-26-autodream-coexistence.md) | 2026-03-26 | high | Dream=janitor, Scribe=architect coexistence |
| [checkpoint-versioning](../learnings/checkpoint-versioning.md) | 2026-03-18 | high | Never overwrite, always version checkpoints |
