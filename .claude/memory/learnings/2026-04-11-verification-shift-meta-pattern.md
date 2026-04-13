---
date: 2026-04-11
type: best_practice
severity: high
component: skill
tags: [verification, testing, evaluation, critic, meta-pattern]
summary: "Verification Shift: generování kódu není bottleneck — verifikace ano. LLM judges slabé na faktičnost, cascade failures zesilují, schema compliance != utility. Kombinuj: LLM scoring + grep/search verifikaci + cascade-order checking + regression gates."
source: auto_pattern
uses: 2
successful_uses: 0
harmful_uses: 0
confidence: 1.00
skill_scope: [critic, verify, harness, eval]
related: [2026-04-03-testing-bottleneck.md, 2026-04-08-llm-judge-factuality-weak.md, 2026-04-04-toolgenesis-cascade-evaluation.md, 2026-04-05-regression-gate-pattern.md]
verify_check: "manual"
---

## Meta-pattern: Verification Shift

Consolidated from /dreams 2026-04-11 — 4 learnings from independent sources converging on same conclusion.

### The Shift

Code generation is cheap and fast. Verification that it's correct is now the expensive part.

### Evidence

1. **Testing bottleneck** (2026-04-03): "Code generation is no longer the bottleneck — verification and testing are."
2. **LLM judge weakness** (2026-04-08): LLM judges prioritize structural formatting over factual correctness.
3. **Cascade failure** (Tool-Genesis 2026-04-04): Small L1 compliance errors amplify to catastrophic L4 utility failures. Schema-F1 0.964 but SR only 0.472.
4. **Regression gate** (NeoSigma 2026-04-05): Without additive regression suite, optimization goes in circles.

### Multi-Layer Verification Protocol

| Layer | What | How | When |
|-------|------|-----|------|
| L1 | Syntax/format | Linter, schema check | Always (cheap) |
| L2 | Semantic correctness | LLM judge + grep/search cross-check | After L1 pass |
| L3 | Downstream utility | Execute on real data, check output | After L2 pass |
| L4 | Regression | Run accumulated regression suite | Before accepting any change |

### When to Apply

Every /critic run, every /verify, every /harness eval step, every iterative skill's KEEP decision.
