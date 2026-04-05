---
date: 2026-04-05
type: best_practice
severity: high
component: skill
tags: [prompt-engineering, verification, orchestration, research]
summary: EgoAlpha repo analysis identified 5 gaps; 4 implemented (hypothesis annotation, self-consistency, VMAO completeness, FActScore atomic). Few-shot examples deferred.
source: external_research
uses: 0
harmful_uses: 0
confidence: 0.7
---

## EgoAlpha Prompt Engineering Patterns → STOPA Integration

Research brief: `outputs/egoalpha-stopa-research.md` (38 sources, 60 STOPA patterns mapped)

### Implemented (2026-04-05)

1. **Hypothesis-first annotation** (orchestrate, critic, verify) — "state your hypothesis before each Read/Grep"
   - Ref: FActScore arXiv:2305.14251, COT STEP arXiv:2501.13122
2. **Self-Consistency voting** (critic DEEP path) — re-run Verifier on borderline milestones, compare verdicts
   - Ref: Wang et al. arXiv:2203.11171 (+20% accuracy)
3. **Inter-wave completeness check** (orchestrate) — artifact presence, criterion coverage, downstream readiness before next wave
   - Ref: VMAO arXiv:2603.11445 (quality 3.1→4.2)
4. **Atomic claim decomposition** (verify Step 2.8) — decompose completion claims into atomic sub-claims, verify independently
   - Ref: FActScore arXiv:2305.14251

### Deferred

5. **Few-shot examples in skill bodies** — STOPA has 0 positive demonstrations, only negative rules. Min et al. arXiv:2202.12837 shows format/structure matters more than label correctness. TODO: create SKILL.examples.md for critic and orchestrate in dedicated session.

### Key validation findings

- STOPA implements 25/38 analyzed techniques, many before formal publication
- Unique patterns with no known academic equivalent: Amdahl parallelizability gate, calm steering hook, error classification before retry
- SKILL.compact.md validated by SKILL0 arXiv:2604.02268 (+9.7%)
- permission-tier validated by Agent Skills Survey arXiv:2602.12430 (26.1% vulnerability rate)
