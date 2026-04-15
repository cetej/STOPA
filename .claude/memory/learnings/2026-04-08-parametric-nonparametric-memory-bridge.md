---
date: 2026-04-08
type: architecture
severity: high
component: memory
tags: [memory, parametric, non-parametric, hybrid-memory, agent-memory, retrieval]
summary: "Bidirectional conversion between parametric (model weights) and non-parametric (explicit files) memory enables agents to leverage both: fast internalized knowledge + updateable external store. Key to living memory systems."
source: external_research
uses: 1
successful_uses: 0
harmful_uses: 0
confidence: 0.95
related: [2026-04-08-living-memory-over-static-retrieval.md, 2026-03-29-memcollab-agent-agnostic-memory.md]
verify_check: "manual"
---

## Detail

MIA's core structural innovation (arXiv:2604.04503): non-parametric Memory Manager stores compressed trajectories explicitly (fast, updatable, no retraining); parametric Planner internalizes patterns (fast at inference, but fixed per-training). Bidirectional conversion lets the system move knowledge between tiers depending on access patterns and reliability.

**STOPA mapping**: STOPA already implements a version of this:
- Non-parametric: learnings/*.md + critical-patterns.md (explicit, updatable files)
- Parametric: CLAUDE.md + behavioral-genome.md (always-loaded, effectively "internalized")

The gap is the **conversion mechanism**: STOPA's /evolve + /compile are one-directional (non-parametric → effectively-parametric via graduation). MIA suggests reverse flow is valuable: when parametric knowledge becomes stale or wrong, it should demote back to non-parametric for re-evaluation.

**Practical implication**: Rules in critical-patterns.md and behavioral-genome.md should have expiration or challenge mechanisms, not just promotion gates.
