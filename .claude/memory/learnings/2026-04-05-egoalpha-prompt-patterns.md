---
date: 2026-04-05
type: best_practice
severity: high
component: skill
tags: [prompt-engineering, verification, orchestration, research]
summary: "EgoAlpha repo analysis: 2 rounds. Round 1 (4 impl). Round 2 deepresearch (4 impl): Zero-shot CoT in critic/debugging, Reflexion verbal notes in 3-fix, SPP model gating in council, ICL order sensitivity."
source: external_research
uses: 0
harmful_uses: 0
confidence: 0.8
verify_check: "Grep('Zero-shot CoT', path='.claude/skills/critic/SKILL.md') → 1+ matches"
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

### Round 2 — Implemented (2026-04-05, deepresearch survey)

5. **Zero-shot CoT reasoning primer** (critic, systematic-debugging) — "Let me trace through this step by step"
   - Ref: Kojima et al. arXiv:2205.11916 (187 citations)
   - Added to: critic Phase 2 Verifier, systematic-debugging Phase 1 step 5 + Phase 3 step 1
6. **Reflexion verbal note** (core-invariants.md rule #7) — after each FAIL, generate "what to do differently next time" note
   - Ref: Shinn et al. arXiv:2303.11366 (91% vs 80% HumanEval)
7. **SPP model gating** (council) — high-stakes decisions use sonnet advisors, not haiku
   - Ref: Chen et al. arXiv:2307.05300 (cognitive synergy only at GPT-4/Opus level)
8. **ICL order sensitivity** — strongest examples at END of SKILL.md demonstrations (recency effect)
   - Ref: Lu et al. arXiv:2205.11916 (170 citations)

### Round 2 — Also Implemented (same session)

9. **Self-RAG reflection tokens** (arXiv:2310.11511) → /deepresearch agent template: per-source [RELEVANT/PARTIAL/IRRELEVANT/UNCERTAIN] assessment
10. **SKR self-knowledge boundary** (arXiv:2310.05002) → /scout Step 0.5: check memory before exploration
11. **LATS-lite branch exploration** (arXiv:2310.04406) → /orchestrate deep tier: parallel alternative approaches before linear retry
12. **Self-Discover reasoning modules** (arXiv:2402.03620) → /triage Step 1.5: classify task by reasoning modules needed
13. **MetaGPT output contracts** (arXiv:2308.00352) → `output-contract:` field in skill-files.md frontmatter spec

### Key validation findings

- STOPA implements 25/38 analyzed techniques, many before formal publication
- Unique patterns with no known academic equivalent: Amdahl parallelizability gate, calm steering hook, error classification before retry
- SKILL.compact.md validated by SKILL0 arXiv:2604.02268 (+9.7%)
- permission-tier validated by Agent Skills Survey arXiv:2602.12430 (26.1% vulnerability rate)
- Full research brief (round 2): `outputs/egoa-research.md` (25 sources, 43 consulted)
