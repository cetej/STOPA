---
date: 2026-04-04
type: architecture
severity: high
component: skill
tags: [skill, orchestration, token-optimization, SKILL0]
summary: "SKILL0 (arXiv:2604.02268) Dynamic Curriculum pattern adapted for STOPA: compact skill variants (~7% of full size) for repeat session invocations, impact_score for helpfulness-driven learning graduation, progressive withdrawal protocol in orchestrator."
source: external_research
uses: 0
harmful_uses: 0
confidence: 0.6
verify_check: "Glob('**/*.compact.md') -> 5+ matches"
successful_uses: 0
---

## What happened

SKILL0 paper introduced in-context RL with progressive skill withdrawal — full context during training, zero context at inference. Adapted 3 patterns for STOPA's inference-time skill system:

1. **Compact skill variants** — SKILL.compact.md alongside SKILL.md (7-9% of full size)
2. **Impact scoring** — `impact_score` field in learnings measures on-policy helpfulness, not just usage count
3. **Progressive withdrawal** — orchestrator tracks session invocations, loads compact on repeat

## Prevention/fix

- When creating new large skills (>300 lines), create compact variant simultaneously
- Impact score measured by critic: before/after quality comparison
- Graduation now has two paths: traditional (uses>=10, confidence>=0.8) OR impact-driven (impact>=0.7, uses>=5)
