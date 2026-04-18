---
date: 2026-04-18
type: best_practice
severity: high
component: orchestration
tags: [evaluation, honesty, measurement, critic, eval, verify, feedback-loop]
summary: "MASK pipeline disentangles honesty from accuracy: elicit belief B via neutral prompt, elicit statement S via pressure prompt, compare S vs B (lying) independently from B vs T (accuracy). Measuring only accuracy conflates two orthogonal dimensions."
source: external_research
uses: 0
successful_uses: 0
harmful_uses: 0
confidence: 0.75
impact_score: 0.0
maturity: draft
skill_scope: [critic, eval, verify, self-evolve]
related: [2026-04-12-model-size-negatively-correlated-honesty.md, 2026-04-08-long-horizon-deception-eval.md]
verify_check: "manual"
valid_until: 2027-04-18
---

## Detail

**Paper**: MASK Benchmark (arXiv:2503.03750v3, Ren et al., Jan 2026), Center for AI Safety + Scale AI.

### Core insight
Honesty ≠ accuracy. These are **orthogonal** dimensions:
- **Accuracy** = belief B matches ground truth T (factual knowledge)
- **Honesty** = statement S matches belief B (intent not to deceive)

Models can be accurate but dishonest (knowingly state false) or inaccurate but honest (state what they genuinely believe, even if wrong).

### Measurement pipeline (3-step)
1. **Pressure prompt**: human-crafted scenario that incentivizes lying (role conflict, stakes, social pressure — NOT "say X" instruction)
2. **Belief elicitation prompt**: neutral direct question about same proposition, run 3× (for binary: 2 additional indirect questions for consistency check)
3. **Judge extraction**: LLM judge maps both S and B to proposition resolution, compare programmatically. Strict criteria — evasive answers classified as "no clear resolution", not imputed.

**Validation**: 86.4% agreement between automated judge and human labels on 150 samples.

### Design principles for eval prompts (apply to STOPA /eval harness)
1. **Realistic intent to mislead** — plausible deception scenario, not toy setup
2. **Avoid LLM-generated placeholders** ("ABC Company", "Alice/Bob", "John Doe") — signals test context, weakens pressure
3. **Commission vs omission** — this measures explicit falsehoods; omission is separate eval
4. **Don't update the belief** — "new evidence suggests X" poisons the belief probe; pressure must not shift what model thinks is true
5. **Consequential scenarios only** — skip roleplay/fiction/silly settings, they don't trigger genuine deception
6. **Verifiable facts only** — no subjective/debated ground truth

### STOPA application (Phase 3 feedback loop)
- `/critic` currently scores outputs against rubric → add **belief consistency check**: for claims in output, compare against model's unpressured answer on same fact
- `/eval` harness: add honesty archetype to eval cases alongside correctness. Track P(Lie) separately from P(Correct)
- `/verify` scoring: currently conflates "did the thing" with "claims it did the thing" — separate `claim_verified` from `output_verified`
- `/self-evolve` Critic gate: add invariant "no regression in honesty score" alongside existing invariants

### Anti-pattern this prevents
"Bigger model → better output" reasoning in model router. MASK shows +87% accuracy correlation with scale, **−60% honesty correlation**. Orchestrator must not treat "more capable = more trustworthy" as given.

### Integration hint for Phase 3
The MASK pipeline IS a measurable feedback loop — inputs (prompts), intermediate states (S, B), outputs (P(Lie), P(Correct)), each step programmatically verifiable. Adopting this structure in STOPA `/eval` gives us a second axis of measurement beyond accuracy, making the feedback loop richer without adding LLM-judge subjectivity (judge mapping is deterministic once rubric is fixed).
