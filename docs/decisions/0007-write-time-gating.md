---
date: 2026-03-30
status: IMPLEMENTING
component: memory
tags: [learnings, scribe, gating, arxiv]
---

# 0007 — Write-Time Gating for learnings

## Context
arXiv:2603.15994 research on filtering low-quality learnings before persistence.

## Decision
Implement salience gate in /scribe, `source:` field, stricter dedup. Variant B (minimal effort, backwards compatible).

## Consequences
- Higher quality learnings, less noise
- New `source:` field on all learnings (backwards compatible — missing = `auto_pattern`)
