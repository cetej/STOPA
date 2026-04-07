---
date: 2026-04-07
type: best_practice
severity: high
component: orchestration
tags: [kaizen, improvement-loop, cron, meta, watch, evolve]
summary: Weekly kaizen loop (Friday cron research + Sunday human review) combines external community scan with internal friction detection. Produces measurable improvement on cadence rather than ad-hoc tinkering. STOPA has /watch + /evolve but no fused weekly rhythm that covers both.
source: external_research
uses: 0
successful_uses: 0
harmful_uses: 0
confidence: 0.6
verify_check: manual
---

# Kaizen Loop — Weekly Improvement Cadence

Production deployment ("Stella") with 800K-view post (2026-04-06) demonstrates that a formal weekly improvement cycle outperforms ad-hoc system maintenance.

**Pattern**: Friday cron scans community patterns, saves to `kaizen-research-YYYY-MM-DD.md`. Sunday human+AI review session surfaces top ideas, decides what to change.

**Internal feedback loop**: daily interaction friction (repeated corrections, noisy filters) captured in memory and surfaced as change proposals. Enables learning from own failures, not just external patterns.

**Key principle**: "Smaller system you trust > bigger system you route around." Kaizen enforces continuous pruning discipline.

**STOPA gap**: `/watch` scans ecosystem, `/evolve` graduates patterns — but no scheduled fusion of both into a weekly human review rhythm. Could be implemented as: cron `/watch` Friday → append to kaizen file → scheduled task Sunday morning → brief review session.

**Why:** Formal cadence prevents the anti-pattern of "I'll improve this when I remember" which produces stagnation. The weekly schedule creates accountability.
