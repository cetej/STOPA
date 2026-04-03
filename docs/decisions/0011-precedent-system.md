---
date: 2026-03-28
status: DONE
component: orchestration
tags: [decisions, grep, episodic-recall]
---

# 0011 — Precedent system in orchestrate

## Context
Orchestrator needed to learn from past decisions to avoid re-debating settled questions.

## Decision
Grep decisions in orchestrate Phase 3 (Episodic Recall) before making new architectural choices.

## Consequences
- Orchestrator checks `docs/decisions/` for relevant precedents before proposing approaches
