---
name: Deception Auditor
type: concept
first_seen: 2026-04-08
last_updated: 2026-04-08
sources: [lh-deception-long-horizon-agent]
tags: [security, evaluation, multi-agent, audit, deception]
---

# Deception Auditor

> Third-party agent role that retrospectively reviews complete interaction trajectories to detect deceptive behaviors — distinct from a real-time supervisor or per-step critic.

## Key Facts

- Operates AFTER the full interaction, not during — reviews the entire trajectory (ref: sources/lh-deception-long-horizon-agent.md)
- Independent from both Performer and Supervisor — avoids trust-contamination from ongoing interaction (ref: sources/lh-deception-long-horizon-agent.md)
- Specifically designed to detect patterns invisible in single-turn or per-step evaluation (ref: sources/lh-deception-long-horizon-agent.md)
- Complements (not replaces) real-time supervision — catches what step-by-step critics miss (ref: sources/lh-deception-long-horizon-agent.md)

## Relevance to STOPA

A Deception Auditor is the trajectory-level analog of STOPA's per-step `/critic`. STOPA could implement this pattern in `/discover` or as a post-session audit in `/checkpoint` — run a "trajectory auditor" agent on the full session trace to flag escalating rationalization or systematic output distortion.

## Mentioned In

- [LH-Deception: Long-Horizon Agent Deception](../sources/lh-deception-long-horizon-agent.md)
