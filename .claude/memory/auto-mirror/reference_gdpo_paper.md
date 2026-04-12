---
name: GDPO Paper Reference
description: GDPO multi-reward RL optimization pattern — decoupled normalization fixes GRPO advantage collapse
type: reference
---

# GDPO (arXiv:2601.05242)

Liu et al. 2026. Fixes GRPO's multi-reward collapse.

**Core insight:** Normalizing the *sum* of multiple rewards erases signal — (0,1) and (0,2) reward pairs get identical normalized advantages. Fix: normalize each reward independently → sum → batch-normalize for stability.

**Conditional reward gating:** When objectives have different difficulty levels, gate easier reward on harder: `R_secondary = R_secondary if R_primary == 1 else 0`. Weight tuning alone fails when difficulty gap is large.

**Benchmarks:** +2–7% across tool calling (Qwen2.5), AIME (DeepSeek-R1), coding (Codecontests/Codeforces).

**STOPA relevance:** /autoloop and /autoresearch multi-metric optimization should apply decoupled normalization; gate style/format metrics on correctness in critic scoring loops.

**Wiki:** `.claude/memory/wiki/sources/gdpo-multi-reward-rl-optimization.md`
**Learning:** `learnings/2026-04-07-multi-reward-normalization-collapse.md`
