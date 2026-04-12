---
name: systematicls Harness Design Patterns
description: @systematicls articles on long-running agent failures — taxonomy of agent stupidity + why fine-tuning beats prompt engineering for specialization
type: reference
---

**Source:** @systematicls on Twitter/X (2026-04, two articles)

## Article 1: Long-Running Agentic Workflows

Taxonomy of agent failures in autonomous sessions:

| Phase | Problem | Solution Pattern |
|-------|---------|-----------------|
| Pre-task | Incomplete/contradictory context | Systematic context check before starting |
| Planning | Wrong attack vector (misalignment) | N-plan generation + independent selection agent |
| Planning | Short-term thinking (tech debt) | Remind to think as founder, not contractor |
| Task | Context anxiety (premature ending) | Smart session handoffs, custom compaction |
| Task | Planning deviation (A→A') | Early & frequent verification against plan |
| Task | Complexity fear (stubs, "out of scope") | Break into bite-sized sub-tasks (<100 lines each) |
| Post-task | Verification laziness (weak tests) | Dedicated verification agent, fresh context, real assertions |
| Post-task | Entropy maximization (stale docs) | Fresh-context cleanup agent after every long session |

Key insight: "Algorithmic contract" per session — formalize what must be true before session can end, enforce with independent auditor.

## Article 2: Specialization vs Prompt Engineering

- Current LLMs optimize for "preference fitness" (sycophancy), not task fitness
- Prompt engineering / skills / rules have a hard ceiling — they can't rewire model weights
- For specialized domains (trading, autonomous survival), fine-tuning on domain data is necessary
- Alpha Arena confirmed: vanilla LLM trading bots converge to random walk minus costs
- OpenForager Foundation: open-source project to train survival-specialized agents with telemetry

**How to apply:** STOPA skills/harness add real value for coding tasks (where frontier models are already strong). For specialized prediction tasks (POLYBOT, ORAKULUM), consider fine-tuning open models rather than relying on prompt-level specialization alone.
