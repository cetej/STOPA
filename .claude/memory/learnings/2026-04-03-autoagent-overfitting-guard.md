---
date: 2026-04-03
type: best_practice
severity: high
component: orchestration
tags: [autoloop, autoresearch, self-evolve, reward-hacking, overfitting]
summary: "AutoAgent's anti-overfitting guard: ask 'if this exact eval case disappeared, would this change still be worthwhile?' before accepting improvements. Prevents metric gaming."
source: external_research
uses: 1
harmful_uses: 0
confidence: 0.8
verify_check: "Grep('exact eval case disappeared', path='.claude/skills/autoloop/SKILL.md') → 1+ matches"
related: []
successful_uses: 0
---

## AutoAgent Overfitting Guard

AutoAgent (kevinrgu/autoagent) discovered that meta-agents overfit by inserting rubric-specific prompting so task agents can game metrics.

**Guard question**: Before accepting a KEEP decision, ask: "If this exact eval case disappeared, would this change still be a worthwhile harness improvement?"

- If YES → genuine improvement, keep
- If NO → flag as potential overfitting, log warning in run diary

**Why:** STOPA's existing reward hacking detection (complexity creep, churn cycling, metric spike) catches structural overfitting but not semantic overfitting — where the change is technically clean but only helps on specific eval cases.

**How to apply:** Add this check to autoloop and autoresearch KEEP decision logic, alongside existing reward hacking checks.
