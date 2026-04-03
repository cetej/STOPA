---
date: 2026-03-31
status: DONE
component: orchestration
tags: [effort, tiers, budget]
---

# 0003 — /effort and orchestrate tier alignment

## Context
`/effort` Low/Med/High and orchestration budget tiers were independently configured, causing mismatches.

## Decision
`/effort` automatically aligns with the chosen orchestration tier. Implemented in orchestrate skill+commands.

## Consequences
- Single source of truth for resource allocation per task
