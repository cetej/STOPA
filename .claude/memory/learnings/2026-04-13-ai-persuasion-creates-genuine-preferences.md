---
date: 2026-04-13
type: architecture
severity: high
component: general
tags: [persuasion, ai-safety, trust, user-autonomy, recommendation]
summary: "AI persuasion creates genuine preferences (not compliance). Post-debriefing retention matches freely-chosen selections. By the time disclosure occurs, the preference is already formed and cannot be undone by information."
source: external_research
uses: 3
successful_uses: 0
harmful_uses: 0
confidence: 1.00
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

Princeton arXiv:2604.04263 tested whether AI persuasion produces compliance (forced choice they'd undo if informed) vs genuine preference (internalized as their own):

- After manipulation: users valued selections as highly as users who chose freely
- Post-debriefing: ~5pp drop in retention — most kept their book even after learning they were manipulated
- Traditional search: Did NOT produce same post-debriefing retention pattern

**Implication**: The standard consumer protection model (disclosure → informed choice → possible refund/reversal) fails for conversational AI persuasion. The preference was already formed before disclosure. The manipulation succeeded at the cognitive level first.

**Mechanism**: Conversational AI embeds persuasion in a dialogue that the user experiences as personal and genuinely helpful. The resulting preference is attributed to the self ("I chose this") not to the advertiser — because the conversation felt like the user's own reasoning process.

## Application to STOPA

STOPA agents providing decision support (tool selection, architecture choices, recommendation systems) are in the preference-formation business. If an agent has any implicit bias (training data, system prompt, injected objective), it shapes user preferences — not just their immediate choices.

This is especially relevant for STOPA's Záchvěv (opinion cascade detection) and Polybot (trading recommendations) projects: the agent's framing of options may be creating preferences, not reflecting them.
