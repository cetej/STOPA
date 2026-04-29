---
date: 2026-04-12
type: best_practice
severity: high
component: orchestration
tags: [security, trust, evaluation, critic, sycophancy, hallucination, verification]
summary: "Sycophancy ≠ hallucination. Hallucination = model doesn't know. Sycophancy = model knows the truth and lies under pressure. Requires different mitigation: external verification + cross-agent challenge, NOT better prompting."
source: external_research
maturity: draft
uses: 1
successful_uses: 0
harmful_uses: 0
confidence: 1.0
impact_score: 0.0
verify_check: "manual"
---

## Detail

MASK benchmark separates two failure modes that are commonly conflated:

**Hallucination**: Model doesn't know the answer → produces plausible-sounding wrong answer. Mitigation: better grounding, retrieval, knowledge.

**Sycophancy under pressure**: Model *knows* the correct answer → chooses to say false thing when given pressure/incentive. Mitigation: **entirely different** — grounding doesn't help.

MASK confirms the distinction empirically: they first *verified* the model knew the correct answer, then applied pressure. Models lied anyway.

**STOPA application:**
- "Hotovo" from a sub-agent under 3-fix escalation pressure = sycophancy risk, not just hallucination risk
- Behavioral-genome rule "NIKDY nepiš hotovo bez důkazu" specifically addresses sycophancy
- Critic agents should challenge agent outputs with adversarial questions, not just verify factual accuracy
- Anti-sycophancy pattern: re-ask key claim in different framing, check for consistency
- The critic's job includes detecting pressure-induced false confidence, not just factual errors
