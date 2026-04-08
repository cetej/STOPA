---
name: LLM-Native Validation
type: concept
first_seen: 2026-04-08
last_updated: 2026-04-08
sources: [seedance-shot-design-skill-patterns]
tags: [skill-design, validation, prompt-quality, anti-pattern]
---

# LLM-Native Validation

> Structured validation checklist executed by the LLM itself (not Python/external scripts) — enforcing hard rules on outputs before delivery to the user.

## Key Facts

- **Origin**: Seedance skill v1.8.1 replaced Python `validate_prompt.py` execution with a 7-rule LLM-native checklist after a security platform (ClawHub) flagged Python execution patterns. (ref: sources/seedance-shot-design-skill-patterns.md)
- **Structure**: Rules are numbered, each with ❌ error (must fix + rewrite) vs ⚠️ warning (advisory). Hard blocks prevent delivery of invalid output. (ref: sources/seedance-shot-design-skill-patterns.md)
- **Key rule types**: length limits, temporal logic (timestamps), professional terminology presence, filler-word hard-blocks, asset reference limits, optical/style conflict matrix, platform-specific term disambiguation. (ref: sources/seedance-shot-design-skill-patterns.md)
- **Python scripts remain** as standalone developer/CI tools — decoupled from agent execution path. Clean separation of concerns. (ref: sources/seedance-shot-design-skill-patterns.md)
- **Anti-rationalization built-in**: "Prompts failing validation are forbidden from being shown to users" — hard stop, not suggestion. (ref: sources/seedance-shot-design-skill-patterns.md)

## Relevance to STOPA

`/critic`, `/klip`, `/nano` could adopt this pattern: numbered rules with explicit error vs warning tiers, hard-block before delivery. Stronger than current "self-check" which is advisory. Related to `schema-utility-decoupling` (entity exists) — LLM-native validation is the runtime enforcement complement to schema design.

## Mentioned In

- [Seedance 2.0 Shot Design — Skill Architecture Patterns](../sources/seedance-shot-design-skill-patterns.md)
