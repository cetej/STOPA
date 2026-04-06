---
generated: 2026-04-04
cluster: orchestration-infrastructure
sources: 6
last_updated: 2026-04-07
---

# Orchestration Infrastructure & Sessions

> **TL;DR**: Context management (autocompact at 70%), paged retrieval (manifest-first), and session persistence (channels, checkpoints) form the infrastructure layer that keeps long-running orchestration viable. Self-sharpening via decoupled model temperatures validates structured self-feedback without a reward model.

## Overview

Long sessions degrade without proactive context management. Setting `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=70` triggers compaction earlier than the default ~95%, preventing quality degradation before it becomes visible (ref: 2026-04-01-autocompact-threshold.md). The paged context protocol complements this: read block-manifest.json (metadata only) first, then fetch only top-scored blocks by budget — preventing irrelevant learnings from consuming precious context tokens (ref: 2026-03-29-paged-context-protocol.md).

Session persistence presents different challenges. Claude Channels has no message queue — messages are lost if no session is running. Cross-device sync via SyncThing and persistent session management via LaunchAgent/systemd are needed for 24/7 operation (ref: 2026-03-26-channels-24x7-architecture.md). The OpenClaw $12K burn postmortem identified five agent degradation patterns: identity collapse, memory bloat, budget blindness, browser loops, and session amnesia (ref: 2026-03-24-openclaw-postmortem-patterns.md).

OSFT (Online SFT, arXiv:2510.18814) demonstrates that self-sharpening — a model finetuning on its own outputs with decoupled sampling temperature (tau_s < tau_t, e.g. 0.6/1.0) — achieves RL-comparable reasoning improvement at 8x lower compute with no reward model. The latent knowledge insight maps to STOPA's learnings system: structured self-feedback unlocks existing capabilities rather than teaching new ones. The multi-tier model system (Haiku/Sonnet/Opus) is structurally analogous to temperature decoupling — different tiers for generation vs validation (ref: 2026-04-06-osft-self-sharpening.md).

## Key Rules

1. **Autocompact at 70%**: set CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=70 (ref: 2026-04-01-autocompact-threshold.md)
2. **Manifest-first retrieval**: read metadata, score, then fetch only top blocks (ref: 2026-03-29-paged-context-protocol.md)
3. **No message queue in Channels**: messages lost without active session (ref: 2026-03-26-channels-24x7-architecture.md)
4. **Watch for 5 degradation patterns**: identity collapse, memory bloat, budget blindness, browser loops, session amnesia (ref: 2026-03-24-openclaw-postmortem-patterns.md)
5. **Stronger model for iterative loops, not one-shot**: OSFT validates tier escalation for iterative tasks (ref: 2026-04-06-osft-self-sharpening.md)
6. **Latent knowledge over new learning**: structured self-feedback retrieval unlocks capabilities; same principle as learnings system (ref: 2026-04-06-osft-self-sharpening.md)

## Patterns

### Do
- Set autocompact threshold below default for long sessions (ref: 2026-04-01-autocompact-threshold.md)
- Use block-manifest.json as retrieval index, not raw file scanning (ref: 2026-03-29-paged-context-protocol.md)
- Implement scheduled maintenance for budget and memory hygiene (ref: 2026-03-24-openclaw-postmortem-patterns.md)

### Don't
- Assume context quality stays constant in 95%+ utilization (ref: 2026-04-01-autocompact-threshold.md)
- Load all learnings into context when only 3-5 are relevant (ref: 2026-03-29-paged-context-protocol.md)
- Run unattended agents without budget limits (ref: 2026-03-24-openclaw-postmortem-patterns.md)
- Use same model tier for one-shot generation and iterative repair — decouple them (ref: 2026-04-06-osft-self-sharpening.md)

## Open Questions

- GAP: Budget tracking accuracy — no actual vs estimated cost comparison (ref: 2026-04-04-gap-budget-calibration.md; owned by orchestration-resilience.md)
- OSFT limited to verifiable tasks (math, code) — open-ended skill improvement unclear

## Related Articles

- See also: [memory-architecture](memory-architecture.md) — persistent memory patterns
- See also: [orchestration-resilience](orchestration-resilience.md) — error handling for long sessions

## Source Learnings

| File | Date | Severity | Summary |
|------|------|----------|---------|
| [2026-04-06-osft-self-sharpening](../learnings/2026-04-06-osft-self-sharpening.md) | 2026-04-06 | medium | Self-sharpening via decoupled temps, no reward model, 8x cheaper than GRPO |
| [2026-04-01-autocompact-threshold](../learnings/2026-04-01-autocompact-threshold.md) | 2026-04-01 | medium | Autocompact at 70% prevents quality degradation |
| [2026-03-29-paged-context-protocol](../learnings/2026-03-29-paged-context-protocol.md) | 2026-03-29 | medium | Paged retrieval via block-manifest.json |
| [2026-03-26-channels-24x7-architecture](../learnings/2026-03-26-channels-24x7-architecture.md) | 2026-03-26 | high | Channels has no queue, needs persistence layer |
| [2026-03-24-openclaw-postmortem-patterns](../learnings/2026-03-24-openclaw-postmortem-patterns.md) | 2026-03-24 | high | 5 degradation patterns from $12K burn |
| [2026-03-25-batch-edit-pattern](../learnings/2026-03-25-batch-edit-pattern.md) | 2026-03-25 | high | Batch scripts for bulk file edits |
