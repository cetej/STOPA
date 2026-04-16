---
date: 2026-04-13
type: architecture
severity: high
component: orchestration
tags: [autoloop, autoresearch, self-evolve, outcomes, optstate, replay, compute-efficiency]
summary: "Skills čtou optstate momentum, ale ne konkrétní outcomes z minulých runů. Phase 0 by mělo glob outcomes/<skill>-* (last 5, desc) a číst Trajectory Summary — stejný mechanismus jako experience replay v RL snižuje 'inference cost' (agent spawns) bez ztráty kvality."
source: external_research
uses: 3
successful_uses: 0
harmful_uses: 0
confidence: 1.00
maturity: draft
skill_scope: [autoloop, autoresearch, self-evolve]
related: [2026-04-15-prm-step-verification-orchestrate.md]
verify_check: "Glob('.claude/memory/outcomes/autoloop-*') → 0+ files (can be empty)"
task_context:
  task_class: research
  complexity: medium
  tier: standard
---

## Detail

arXiv:2604.08706 (Meta FAIR): striktně on-policy RL = "generate-then-discard" je suboptimální. Replay buffer (reuse past trajectories) šetří 40% compute při stejné nebo lepší přesnosti.

STOPA analogie:
- "Generate new rollouts" = spawnovat nové agenty pro průzkum
- "Training on stored rollouts" = číst outcomes z minulých runů
- `outcomes/` = replay buffer (FIFO, max 100 files) — EXISTS ale UNDERUSED

**Gap:** Skills v Phase 0 čtou jen `optstate/<skill>.json` (momentum agregát), ale ne konkrétní trajectory summaries z `outcomes/<skill>-*.md`. To je jako kdybychom měli replay buffer, ale ignorovali ho.

**Fix pattern:**
```
Phase 0 enhanced:
1. Read optstate/<skill>.json (current)
2. NOVÉ: Glob outcomes/<skill>-*.md, sort desc, limit 5
3. Read last 5 outcomes → extract "What Worked" section
4. Use as positive context: "These approaches worked before: ..."
```

**Positive-bias:** čti `## What Worked` sekce outcomes s prioritou, `## What Failed` jako anticuriculum.

Ref: arXiv:2604.08706 Theorem 4.5 — optimal replay ratio B/R = √(μ/(ρ + 1/x*)), kde μ = cost inference/training

> Updated 2026-04-16: PRM step-verification (arXiv:2501.09686) can enrich outcome replay labels. Currently outcomes only record run-level "What Worked"/"What Failed". Future enhancement: annotate which step failed (step_results[] from PRM check) — enables step-level replay attribution instead of coarse run-level signal.
