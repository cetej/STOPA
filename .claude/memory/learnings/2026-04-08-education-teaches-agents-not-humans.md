---
date: 2026-04-08
type: best_practice
severity: medium
component: skill
tags: [skill, orchestration, memory, documentation]
summary: "Education is shifting from teaching humans to teaching agents. SKILL.md files and curriculum hints are more valuable than video tutorials or documentation written for humans. If the agent understands it, it can teach the human at their level with infinite patience."
source: external_research
uses: 1
successful_uses: 0
harmful_uses: 0
confidence: 0.85
failure_class:
verify_check: "manual"
---

## Detail

Karpathy on microGPT (No Priors, 2026-03-20): "I'm explaining things to agents now. If the agent gets it, they'll do the explanation. I could have a skill for microGPT — just hints to the model to start with this, then that — a scripted curriculum."

The shift:
- Old: human writes docs/videos for other humans to consume
- New: human encodes understanding as SKILL.md context + curriculum hints for agents to execute
- Agents then teach humans at their exact level, in their language, with infinite patience

**Implication for STOPA skill design:**
- Every SKILL.md is an educational artifact for the agent, not documentation for the human
- The `description:` field routes the agent; the skill body is what the agent learns to do
- Adding "curriculum progression hints" to complex skills (e.g., `## Learning Path` section) could improve agent execution quality
- This validates the skill-body-as-context-engineering principle (behavioral-genome.md)
