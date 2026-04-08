---
name: Program.md Research Org
type: concept
first_seen: 2026-04-08
last_updated: 2026-04-08
sources: [karpathy-nopriors-autoagent-loopy-era]
tags: [orchestration, research, memory, ai-tools]
---

# Program.md Research Org

> A research organization described entirely as a set of markdown files (roles, workflows, policies) — enabling meta-optimization: run auto-research on the org itself to find better research methodologies.

## Key Facts

- Karpathy's insight: "a research organization is a set of markdown files that describe all the roles and how the whole thing connects" (ref: sources/karpathy-nopriors-autoagent-loopy-era.md)
- Different program.mds produce different research velocities — one org has fewer standups, one is more risk-taking, all expressible as code (ref: sources/karpathy-nopriors-autoagent-loopy-era.md)
- Contest idea: same hardware, different program.mds → leaderboard of improvement rate → feed to model → generate better program.md (ref: sources/karpathy-nopriors-autoagent-loopy-era.md)
- Layers of the onion: LLM → agent → claw → multi-claw → instructions-to-claws → optimization-over-instructions → infinite (ref: sources/karpathy-nopriors-autoagent-loopy-era.md)
- STOPA is already this: SKILL.md files + hooks.json + CLAUDE.md = program.md for the orchestration org (ref: sources/karpathy-nopriors-autoagent-loopy-era.md)

## Relevance to STOPA

STOPA is literally a program.md implementation. `/evolve` runs meta-optimization on STOPA's own SKILL.md files. The contest idea (same hardware, different configs → leaderboard) is the direction for `/self-evolve` at the system level. This framing validates the entire STOPA architecture.

## Mentioned In

- [No Priors: Code Agents, AutoResearch, and the Loopy Era](../sources/karpathy-nopriors-autoagent-loopy-era.md)
