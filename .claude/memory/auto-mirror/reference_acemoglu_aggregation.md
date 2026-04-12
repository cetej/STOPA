---
name: Acemoglu AI Aggregation
description: arXiv:2604.04906 — global aggregator necessarily hurts ≥1 dimension; local aggregators preserve specialization; implemented in STOPA as skill_scope field + circular validation detection + inverse frequency graduation
type: reference
---

Acemoglu et al. (MIT, arXiv:2604.04906): extended DeGroot model with AI aggregator node.

Three theorems implemented in STOPA:
1. **Theorem 3** (global < local) → `skill_scope:` field in learnings YAML, local graduation to `skills/<name>/learned-rules.md`
2. **Proposition 2** (majority-weighting bias) → inverse frequency graduation threshold in `/evolve`
3. **Theorem 2** (feedback loop) → circular validation detection in `learning-admission.py` (`check_circular_validation()`)

Implementation files:
- `.claude/hooks/learning-admission.py` — `check_circular_validation()` function, title-keyword matching
- `.claude/skills/evolve/SKILL.md` — graduation routing + inverse frequency threshold
- `.claude/rules/memory-files.md` — `skill_scope:` field documentation
