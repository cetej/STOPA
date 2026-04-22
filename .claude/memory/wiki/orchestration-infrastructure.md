---
generated: 2026-04-04
cluster: orchestration-infrastructure
sources: 29
last_updated: 2026-04-22
---

# Orchestration Infrastructure & Sessions

> **TL;DR**: Context management (autocompact at 70%), paged retrieval (manifest-first), and session persistence (channels, checkpoints) form the infrastructure layer that keeps long-running orchestration viable. Self-sharpening via decoupled model temperatures validates structured self-feedback without a reward model.

## Overview

Long sessions degrade without proactive context management. Setting `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=70` triggers compaction earlier than the default ~95%, preventing quality degradation before it becomes visible (ref: 2026-04-01-autocompact-threshold.md). Even better: manually compact at ~60% capacity, since autocompact at 70-95% already shows degradation from "lost in the middle" — models attend to conversation beginning and end, ignoring the middle. After 3-4 manual compacts in a row, quality degrades further; at that point, do `/clear` with a session summary and restart fresh (ref: 2026-04-14-compact-timing-60pct.md). The paged context protocol complements this: read block-manifest.json (metadata only) first, then fetch only top-scored blocks by budget — preventing irrelevant learnings from consuming precious context tokens (ref: 2026-03-29-paged-context-protocol.md).

Prompt caching has a 5-minute TTL — after a 5+ minute pause, the next message reprocesses the entire context at full cost, explaining "random usage spikes" after breaks. Before stepping away, compact or checkpoint+clear; when returning, start fresh with checkpoint resume rather than continuing a stale session (ref: 2026-04-14-prompt-cache-ttl-5min.md). Each connected MCP server loads all its tool definitions (~18K tokens per server per message) as invisible overhead. Audit MCP connections at session start and disconnect servers not needed for the current task. Where CLI equivalents exist (e.g., `gh` for GitHub, `gcal` CLI for Calendar), prefer CLI — outputs go through RTK filtering for 60-90% savings, while MCP tool definitions are uncompressible (ref: 2026-04-14-mcp-server-token-overhead.md).

Session persistence presents different challenges. Claude Channels has no message queue — messages are lost if no session is running. Cross-device sync via SyncThing and persistent session management via LaunchAgent/systemd are needed for 24/7 operation (ref: 2026-03-26-channels-24x7-architecture.md). The OpenClaw $12K burn postmortem identified five agent degradation patterns: identity collapse, memory bloat, budget blindness, browser loops, and session amnesia (ref: 2026-03-24-openclaw-postmortem-patterns.md).

OSFT (Online SFT, arXiv:2510.18814) demonstrates that self-sharpening — a model finetuning on its own outputs with decoupled sampling temperature (tau_s < tau_t, e.g. 0.6/1.0) — achieves RL-comparable reasoning improvement at 8x lower compute with no reward model. The latent knowledge insight maps to STOPA's learnings system: structured self-feedback unlocks existing capabilities rather than teaching new ones. The multi-tier model system (Haiku/Sonnet/Opus) is structurally analogous to temperature decoupling — different tiers for generation vs validation (ref: 2026-04-06-osft-self-sharpening.md).

Spec-kit competitive analysis (81k stars) yielded three adoptable patterns for STOPA: constitution check (project governance doc as non-negotiable authority in /orchestrate and /brainstorm), handoff metadata (`handoffs:` field in skill frontmatter), and requirements-level checklist with traceability tags [Spec]/[Gap]/[Ambiguity] in /critic --spec (ref: 2026-03-23-spec-kit-adoption.md). In-Place TTT (arXiv:2604.06169) demonstrates 3-12× improvement on long-context benchmarks by updating MLP weights chunk-by-chunk at inference time — when TTT-capable models become available, prefer them for deep-tier iterative tasks with >64k context (ref: 2026-04-08-in-place-ttt-long-context-multiplier.md). Test-time learning (MIA arXiv:2604.04503) validates that skills with repair loops (/tdd, /self-evolve) improve within-session without retraining — execution feedback alone suffices; capability-building (Executor) should precede strategy-building (Planner) in multi-agent orchestration (ref: 2026-04-08-test-time-learning-inference-evolution.md).

Operational rhythm transforms an AI tool into a persistent collaborator. A weekly kaizen loop — Friday cron research scan + Sunday human review — combines external community monitoring (/watch) with internal friction detection (/evolve), producing measurable improvement on cadence rather than ad-hoc tinkering (ref: 2026-04-07-kaizen-loop-weekly-improvement.md). Scheduled morning briefs and evening wraps, delivered via messaging channel with strict "silence when nothing to say" discipline, create a chief-of-staff dynamic. The silence rule is as important as the content — noise destroys trust faster than value builds it (ref: 2026-04-07-operational-rhythm-silence-discipline.md).

### 2026-04-18: Compaction, rewind, sidechains, Opus effort

Anthropic confirms context rot begins at 300-400k tokens on the 1M context model (30-40% of window), NOT at 60-95% where prior guidance placed it. Proactive compact should trigger earlier than assumed; the 60% manual-compact rule is now closer to the hard edge of safety, not conservative (ref: 2026-04-18-context-rot-absolute-threshold.md). Bad compacts happen when the model can't predict the next task direction — content outside the session's dominant theme gets dropped silently. Fix: trigger `/compact` proactively with an explicit direction hint BEFORE the topic changes, not after context is already confused (ref: 2026-04-18-bad-compact-direction-unpredictability.md).

Claude Code implements 5 graduated compression layers (Budget Reduction → Snip → Microcompact → Context Collapse → Auto-Compact), each targeting a different pressure type. Apply lightest first, heaviest last. STOPA's `/compact` jumps straight to aggressive summarization — adopt a progressive strategy with lighter interventions first to preserve more recoverable signal (ref: 2026-04-18-cc-graduated-compaction-5layer.md). A related CC feature: `/rewind` (Esc×2) jumps back to before a failed approach and re-prompts with learnings, cleaner than appending "that didn't work, try X" which adds noise without removing the failed reasoning from context (ref: 2026-04-18-rewind-beats-correction.md).

Sidechain isolation: CC subagent sidechains never return full history to parent — only final response text. STOPA `Agent()` already works this way, but agent instructions often don't explicitly mandate concise response summarization before return, causing context bloat at the orchestrator level. Fix: every Agent() prompt should end with "return a <200-word summary — do not dump raw tool output" (ref: 2026-04-18-cc-sidechain-transcript-isolation.md).

Opus 4.7 in Claude Code: default effort=xhigh is the recommended setting; max effort shows diminishing returns plus overthinking. Adaptive thinking is per-step (not a fixed budget). Every user turn adds reasoning overhead — specify the whole task in the first turn rather than incrementally. Treat the model like a delegated engineer (full spec upfront), not a pair-programmer (back-and-forth) (ref: 2026-04-18-opus-4-7-effort-calibration.md).

## Key Rules

1. **Manual compact at 60%, max 3-4 per session**: after 3-4 compacts, /clear + summary + restart (ref: 2026-04-14-compact-timing-60pct.md)
2. **Manifest-first retrieval**: read metadata, score, then fetch only top blocks (ref: 2026-03-29-paged-context-protocol.md)
3. **No message queue in Channels**: messages lost without active session (ref: 2026-03-26-channels-24x7-architecture.md)
4. **Watch for 5 degradation patterns**: identity collapse, memory bloat, budget blindness, browser loops, session amnesia (ref: 2026-03-24-openclaw-postmortem-patterns.md)
5. **Stronger model for iterative loops, not one-shot**: OSFT validates tier escalation for iterative tasks (ref: 2026-04-06-osft-self-sharpening.md)
6. **Latent knowledge over new learning**: structured self-feedback retrieval unlocks capabilities; same principle as learnings system (ref: 2026-04-06-osft-self-sharpening.md)
7. **Weekly kaizen cadence**: research scan + friction review on fixed schedule, not ad-hoc (ref: 2026-04-07-kaizen-loop-weekly-improvement.md)
8. **Silence when nothing to say**: scheduled notifications must skip empty reports — noise destroys trust (ref: 2026-04-07-operational-rhythm-silence-discipline.md)
9. **Constitution check in /orchestrate**: project governance doc as non-negotiable authority before decomposition (ref: 2026-03-23-spec-kit-adoption.md)
10. **TTT-capable models for deep long-context**: 3-12× improvement at >64k context — watch model release notes for "fast weights" (ref: 2026-04-08-in-place-ttt-long-context-multiplier.md)
11. **Capability before strategy in multi-agent**: build Executor competence before Planner strategy-building (ref: 2026-04-08-test-time-learning-inference-evolution.md)
12. **Compact or clear before breaks**: prompt cache TTL is 5 min; >5min pause = full reprocessing at full cost (ref: 2026-04-14-prompt-cache-ttl-5min.md)
13. **Audit MCP connections per session**: each server = ~18K tokens/message invisible overhead; prefer CLI where equivalent (ref: 2026-04-14-mcp-server-token-overhead.md)
14. **Context rot at 30-40%, not 60-95%**: 300-400k tokens on 1M model is the actual safety edge — compact earlier than historical thresholds (ref: 2026-04-18-context-rot-absolute-threshold.md)
15. **Compact with direction hint, not reactively**: trigger `/compact` proactively with next-task direction before topic changes (ref: 2026-04-18-bad-compact-direction-unpredictability.md)
16. **Progressive compaction**: apply lightest intervention first (Snip/Micro) before aggressive summarization — preserves more recoverable signal (ref: 2026-04-18-cc-graduated-compaction-5layer.md)
17. **`/rewind` over corrective re-prompt**: after a failed approach, Esc×2 back to pre-failure state — appending "that didn't work" leaves failed reasoning in context (ref: 2026-04-18-rewind-beats-correction.md)
18. **Mandate <200-word summaries on Agent() returns**: prevents orchestrator context bloat from subagent tool-output dumps (ref: 2026-04-18-cc-sidechain-transcript-isolation.md)
19. **Opus 4.7: default xhigh, full spec upfront**: max effort diminishes + overthinks; specify whole task in first turn, no incremental pair-programming (ref: 2026-04-18-opus-4-7-effort-calibration.md)

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
- Leave MCP servers connected "just in case" — each one costs ~18K tokens per message (ref: 2026-04-14-mcp-server-token-overhead.md)
- Step away for >5min without compacting or clearing — cache miss reprocesses everything (ref: 2026-04-14-prompt-cache-ttl-5min.md)

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
| [2026-04-07-kaizen-loop-weekly-improvement](../learnings/2026-04-07-kaizen-loop-weekly-improvement.md) | 2026-04-07 | high | Weekly kaizen: research + friction review on cadence |
| [2026-04-07-operational-rhythm-silence-discipline](../learnings/2026-04-07-operational-rhythm-silence-discipline.md) | 2026-04-07 | medium | Silence discipline: skip empty reports |
| [2026-03-25-batch-edit-pattern](../learnings/2026-03-25-batch-edit-pattern.md) | 2026-03-25 | high | Batch scripts for bulk file edits |
| [2026-03-23-spec-kit-adoption](../learnings/2026-03-23-spec-kit-adoption.md) | 2026-03-23 | medium | Spec-kit: constitution check, handoff metadata, requirements checklist |
| [2026-04-08-in-place-ttt-long-context-multiplier](../learnings/2026-04-08-in-place-ttt-long-context-multiplier.md) | 2026-04-08 | medium | In-Place TTT: 3-12× at >64k context; prefer TTT-capable models for deep tier |
| [2026-04-08-test-time-learning-inference-evolution](../learnings/2026-04-08-test-time-learning-inference-evolution.md) | 2026-04-08 | medium | TTL: repair loops improve within-session; Executor before Planner |
| [2026-04-12-model-size-negatively-correlated-honesty](../learnings/2026-04-12-model-size-negatively-correlated-honesty.md) | 2026-04-12 | high | Larger models less honest under pressure |
| [2026-04-12-pretraining-vs-posttraining-dissociation](../learnings/2026-04-12-pretraining-vs-posttraining-dissociation.md) | 2026-04-12 | medium | Pretraining != posttraining capabilities |
| [2026-04-12-ib-optimality-predicts-benchmarks](../learnings/2026-04-12-ib-optimality-predicts-benchmarks.md) | 2026-04-12 | high | IB optimality predicts benchmark performance |
| [2026-04-12-small-model-compression-threshold](../learnings/2026-04-12-small-model-compression-threshold.md) | 2026-04-12 | high | Small models have compression capacity limits |
| [2026-04-13-pretraining-loss-insufficient-generalization-proxy](../learnings/2026-04-13-pretraining-loss-insufficient-generalization-proxy.md) | 2026-04-13 | high | Pretraining loss insufficient for generalization |
| [2026-04-04-gap-budget-calibration](../learnings/2026-04-04-gap-budget-calibration.md) | 2026-04-04 | medium | GAP: budget calibration methodology |
| [2026-04-04-gap-compact-variant-measurement](../learnings/2026-04-04-gap-compact-variant-measurement.md) | 2026-04-04 | medium | GAP: compact variant effectiveness measurement |
| [2026-04-14-compact-timing-60pct](../learnings/2026-04-14-compact-timing-60pct.md) | 2026-04-14 | medium | Compact at 60%, max 3-4 per session, then /clear |
| [2026-04-14-prompt-cache-ttl-5min](../learnings/2026-04-14-prompt-cache-ttl-5min.md) | 2026-04-14 | medium | Cache TTL 5min; pause = full reprocessing |
| [2026-04-14-mcp-server-token-overhead](../learnings/2026-04-14-mcp-server-token-overhead.md) | 2026-04-14 | high | MCP servers ~18K tokens/message invisible overhead |
| [2026-04-18-context-rot-absolute-threshold](../learnings/2026-04-18-context-rot-absolute-threshold.md) | 2026-04-18 | medium | Context rot at 30-40% (300-400k on 1M), not 60-95% |
| [2026-04-18-bad-compact-direction-unpredictability](../learnings/2026-04-18-bad-compact-direction-unpredictability.md) | 2026-04-18 | high | Compact proactively with direction hint before topic change |
| [2026-04-18-cc-graduated-compaction-5layer](../learnings/2026-04-18-cc-graduated-compaction-5layer.md) | 2026-04-18 | medium | CC's 5-layer progressive compaction; apply lightest first |
| [2026-04-18-rewind-beats-correction](../learnings/2026-04-18-rewind-beats-correction.md) | 2026-04-18 | high | `/rewind` (Esc×2) cleaner than corrective re-prompt after failure |
| [2026-04-18-cc-sidechain-transcript-isolation](../learnings/2026-04-18-cc-sidechain-transcript-isolation.md) | 2026-04-18 | medium | Mandate <200-word summaries on Agent() returns |
| [2026-04-18-opus-4-7-effort-calibration](../learnings/2026-04-18-opus-4-7-effort-calibration.md) | 2026-04-18 | high | Opus 4.7: default xhigh, full spec upfront, adaptive per-step thinking |
