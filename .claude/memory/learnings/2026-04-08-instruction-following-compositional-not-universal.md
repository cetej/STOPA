---
date: 2026-04-08
type: best_practice
severity: medium
component: skill
tags: [skill-design, prompting, orchestration, instruction-following]
summary: "Instruction-following uses task-specific representations, not a universal mechanism. Mixing constraint types (format + content + semantic) in one prompt is less effective than separate specialized prompts per constraint domain."
source: external_research
maturity: draft
uses: 1
successful_uses: 0
harmful_uses: 0
confidence: 1.0
verify_check: manual
related: []
---

# Instruction-Following is Compositional, Not Universal

## What happened

arXiv:2604.06015 (Rocchetti & Ferrara, 2026) tested 9 instruction tasks across 3 models using diagnostic probing. Found that:
- General probes underperform specialist probes → minimal shared representations between instruction types
- Cross-task transfer is weak, clusters by similarity only
- Early layers = structural constraints (format, word count), late layers = semantic (topic, sentiment)
- Constraint satisfaction is continuous monitoring during generation, NOT pre-generation planning

## Rule

When designing skill prompts that combine multiple constraint types (e.g., "write a short, formal, positive article about X"), split them into domain-specific constraint blocks or separate skill invocations — don't front-load all constraints in a single mixed prompt.

**Why**: Different constraint types activate different neural representations. Mixed-constraint prompts compete for different layer-level resources and may show weaker adherence than domain-focused prompts.

**How to apply**: In SKILL.md, separate structural constraints (format, length, structure) from semantic constraints (content, topic, tone). Consider interleaving constraint reminders during generation rather than front-loading all at the top. This aligns with heartbeat mid-run steering (CORAL pattern).

## Reference

Source: https://arxiv.org/abs/2604.06015
