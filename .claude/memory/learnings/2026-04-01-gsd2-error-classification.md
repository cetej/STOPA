---
date: 2026-04-01
type: architecture
severity: high
component: orchestration
tags: [error-handling, circuit-breaker, gsd2]
summary: "Classify errors before counting fix attempts: infrastructure (ENOENT/OOM) = immediate stop, transient (429/timeout) = 1 retry, logic = normal 3-fix escalation. Prevents wasting LLM budget on unrecoverable states."
source: external_research
maturity: draft
uses: 0
harmful_uses: 0
confidence: 0.7
verify_check: "Grep('Infrastructure.*STOP|Infrastructure.*IMMEDIATE', path='.claude/skills/orchestrate/SKILL.md') -> 1+ matches"
successful_uses: 0
---

## Description

GSD-2 pattern: classify errors into infrastructure/transient/logic BEFORE counting
toward fix attempt budget. Infrastructure errors (ENOENT, OOM, disk full) get
immediate stop — retrying wastes LLM tokens on unrecoverable states. Transient
errors (rate limit, timeout) get 1 retry with delay.

Implemented in `.claude/hooks/error-classifier.py` as a utility module.
Updated core-invariants.md rule #7 and orchestrate SKILL.md circuit breakers.

## Prevention

Always classify error type before deciding whether to retry.
Use `error-classifier.py` for programmatic classification.
