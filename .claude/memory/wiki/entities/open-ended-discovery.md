---
name: Open-Ended Discovery
type: concept
first_seen: 2026-04-08
last_updated: 2026-04-08
sources: [coral-autonomous-multi-agent-evolution]
tags: [self-evolution, autoresearch, exploration, multi-agent]
---

# Open-Ended Discovery

> A problem formulation where agents optimize without a fixed solution target — they explore, reflect, and accumulate knowledge indefinitely rather than solving a closed task.

## Key Facts

- Contrasts with fixed-task completion: no single correct answer, improvement is the only objective (ref: sources/coral-autonomous-multi-agent-evolution.md)
- Requires persistent memory to accumulate knowledge across exploration cycles — without it, each iteration starts from zero (ref: sources/coral-autonomous-multi-agent-evolution.md)
- CORAL achieves 3-10× improvement rates on 10 open-ended tasks vs evolutionary baselines (ref: sources/coral-autonomous-multi-agent-evolution.md)
- Tasks span: mathematical, algorithmic, systems optimization — not domain-specific (ref: sources/coral-autonomous-multi-agent-evolution.md)
- Related concept: GEA (group evolution) targets closed SWE-bench tasks; CORAL targets open-ended exploration

## Relevance to STOPA

STOPA's `autoloop` and `autoresearch` are closed-loop (fixed eval target); open-ended discovery mode is relevant when the eval function itself evolves — applicable to `self-evolve` with adaptive eval generation.

## Mentioned In

- [CORAL: Autonomous Multi-Agent Evolution for Open-Ended Discovery](../sources/coral-autonomous-multi-agent-evolution.md)
