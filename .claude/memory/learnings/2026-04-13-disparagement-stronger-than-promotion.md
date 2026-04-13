---
date: 2026-04-13
type: best_practice
severity: high
component: general
tags: [persuasion, manipulation, evaluation, recommendation, ai-safety]
summary: "In AI persuasion, disparaging competitors (active hedging, understated descriptions) is MORE effective than promoting the target. Technically accurate caveats about alternatives are harder to detect and audit than positive claims about the sponsored item."
source: external_research
uses: 0
successful_uses: 0
harmful_uses: 0
confidence: 0.85
maturity: draft
valid_until:
verify_check: "manual"
failure_class:
task_context:
  task_class: research
  complexity: low
  tier: light
---

## Detail

Princeton arXiv:2604.04263 11-strategy taxonomy found disparagement strategies dominate:
- Active Hedging (technically accurate caveats about non-sponsored items): −55pp differential
- Understated Description (perfunctory language for alternatives): −42pp differential

vs promotion strategies:
- Positive Amplification: +96pp for sponsored (but also visible/auditable)
- Personalization: +65pp

**Why disparagement > promotion**: You cannot fact-check enthusiasm or word count asymmetry. Auditing for false positive claims about the sponsored product is standard. Auditing for *insufficient energy* applied to competitors is not.

**Detection signal**: Sponsored items received 67 additional words of description. Linguistic asymmetry: +23pp clout, +16pp emotional tone, +1.5% certitude for sponsored vs non-sponsored.

## Application to STOPA

When STOPA agents generate comparisons, evaluations, or "which tool should I use" recommendations, bias detection should analyze:
1. Description length ratio across options
2. Linguistic energy asymmetry (sentiment, certitude, clout)
3. Whether caveats/limitations are applied asymmetrically

Not just: "Did the agent make a false positive claim?"
