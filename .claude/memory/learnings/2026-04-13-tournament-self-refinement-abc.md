---
date: 2026-04-13
type: best_practice
severity: high
component: orchestration
tags: [refinement, iteration, critic, review, anti-pattern]
summary: "Tournament self-refinement (A=incumbent, B=adversarial, AB=synthesis) with blind Borda panel prevents prompt bias and scope creep; removing either B or AB collapses performance."
source: external_research
uses: 2
successful_uses: 0
harmful_uses: 0
confidence: 0.9
verify_check: "manual"
skill_scope: [autoreason, critic, autoloop]
---

## Details

Standard critique-and-revise fails because: (1) prompt bias — asking for improvements causes hallucinated flaws; (2) scope creep — no mechanism to stop expansion; (3) lack of restraint — "do nothing" is never structurally valid.

Tournament architecture from NousResearch autoreason:
- A = unchanged incumbent (always competes — "do nothing" is first-class)
- B = adversarial revision by fresh agent
- AB = synthesis agent combining A and B
- Judge panel: 7 fresh agents, blind Borda count voting
- Convergence: incumbent wins k=2 consecutive rounds → stop

Ablation: removing B OR AB alone collapses performance. All three roles are necessary.

**Application to STOPA**: `/autoreason` currently uses 2-variant debate + single critic. Upgrading to A/B/AB + Borda panel would be a direct application of this pattern.
