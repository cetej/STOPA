---
name: Parcae — looped transformer scaling laws
description: Exponential decay stopping model, training depth = inference ceiling, per-item variable depth, orthogonal scaling axes (iterations × data × model). arXiv:2604.12946
type: reference
originSessionId: b6b1952c-5999-4da1-89f8-0cac229cc826
---
**Paper:** Parcae: Scaling Laws For Stable Looped Language Models (arXiv:2604.12946, Apr 2026)
**Authors:** Prairie, Novack, Berg-Kirkpatrick, Fu (UCSD + Together AI)

**Why relevant:** Provides mathematical framework for iterative optimization stopping (autoloop, autoresearch, self-evolve) and variable-depth task distribution (farm tier).

**Key formulas:**
- Test-time decay: `L(T) = L∞ + Z·exp(-z·T)` — fittable after 4 points, 0.85% error
- Unified: `L(T|µ,D) = [E + X·N(µ)^{-x} + Y·D^{-y}] + Z·exp(-z·T/µ)`
- Training power laws: optimal iterations ~ C^0.40, optimal data ~ C^0.78

**STOPA learning:** `.claude/memory/learnings/2026-04-15-parcae-exponential-decay-stopping.md`
