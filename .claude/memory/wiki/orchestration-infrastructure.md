---
generated: 2026-04-04
cluster: orchestration-infrastructure
sources: 5
last_updated: 2026-04-04
---

# Orchestration Infrastructure & Sessions

> **TL;DR**: Context management (autocompact at 70%), paged retrieval (manifest-first), and session persistence (channels, checkpoints) form the infrastructure layer that keeps long-running orchestration viable.

## Overview

Long sessions degrade without proactive context management. Setting `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=70` triggers compaction earlier than the default ~95%, preventing quality degradation before it becomes visible (ref: 2026-04-01-autocompact-threshold.md). The paged context protocol complements this: read block-manifest.json (metadata only) first, then fetch only top-scored blocks by budget — preventing irrelevant learnings from consuming precious context tokens (ref: 2026-03-29-paged-context-protocol.md).

Session persistence presents different challenges. Claude Channels has no message queue — messages are lost if no session is running. Cross-device sync via SyncThing and persistent session management via LaunchAgent/systemd are needed for 24/7 operation (ref: 2026-03-26-channels-24x7-architecture.md). The OpenClaw $12K burn postmortem identified five agent degradation patterns: identity collapse, memory bloat, budget blindness, browser loops, and session amnesia (ref: 2026-03-24-openclaw-postmortem-patterns.md). Structured handoffs and role separation from spec-kit partially address these (ref: spec-kit-adoption.md).

## Key Rules

1. **Autocompact at 70%**: set CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=70 (ref: 2026-04-01-autocompact-threshold.md)
2. **Manifest-first retrieval**: read metadata, score, then fetch only top blocks (ref: 2026-03-29-paged-context-protocol.md)
3. **No message queue in Channels**: messages lost without active session (ref: 2026-03-26-channels-24x7-architecture.md)
4. **Watch for 5 degradation patterns**: identity collapse, memory bloat, budget blindness, browser loops, session amnesia (ref: 2026-03-24-openclaw-postmortem-patterns.md)
5. **Structured handoffs**: constitution files + role separation (ref: spec-kit-adoption.md)

## Patterns

### Do
- Set autocompact threshold below default for long sessions (ref: 2026-04-01-autocompact-threshold.md)
- Use block-manifest.json as retrieval index, not raw file scanning (ref: 2026-03-29-paged-context-protocol.md)
- Implement scheduled maintenance for budget and memory hygiene (ref: 2026-03-24-openclaw-postmortem-patterns.md)

### Don't
- Assume context quality stays constant in 95%+ utilization (ref: 2026-04-01-autocompact-threshold.md)
- Load all learnings into context when only 3-5 are relevant (ref: 2026-03-29-paged-context-protocol.md)
- Run unattended agents without budget limits (ref: 2026-03-24-openclaw-postmortem-patterns.md)

## Open Questions

- GAP: No learnings about budget tracking accuracy and actual vs estimated cost calibration

## Related Articles

- See also: [memory-architecture](memory-architecture.md) — persistent memory patterns
- See also: [orchestration-resilience](orchestration-resilience.md) — error handling for long sessions

## Source Learnings

| File | Date | Severity | Summary |
|------|------|----------|---------|
| [2026-04-01-autocompact-threshold](../learnings/2026-04-01-autocompact-threshold.md) | 2026-04-01 | medium | Autocompact at 70% prevents quality degradation |
| [2026-03-29-paged-context-protocol](../learnings/2026-03-29-paged-context-protocol.md) | 2026-03-29 | medium | Paged retrieval via block-manifest.json |
| [2026-03-26-channels-24x7-architecture](../learnings/2026-03-26-channels-24x7-architecture.md) | 2026-03-26 | high | Channels has no queue, needs persistence layer |
| [2026-03-24-openclaw-postmortem-patterns](../learnings/2026-03-24-openclaw-postmortem-patterns.md) | 2026-03-24 | high | 5 degradation patterns from $12K burn |
| [spec-kit-adoption](../learnings/spec-kit-adoption.md) | 2026-03-23 | medium | Constitution files and structured handoffs |
