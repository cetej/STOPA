---
title: "Persuasion Propagation in LLM Agents"
slug: persuasion-propagation-llm-agents
source_type: url
url: "https://arxiv.org/abs/2602.00851"
date_ingested: 2026-04-13
date_published: "2026-02-15"
entities_extracted: 1
claims_extracted: 4
---

# Persuasion Propagation in LLM Agents

> **TL;DR**: Pre-task belief conditioning creates substantial behavioral changes in LLM agents — 26.9% fewer searches, 16.9% fewer unique sources visited — while being invisible to output-level auditing. Real-time persuasion during execution has weak/inconsistent effects. Detection requires behavior-level monitoring (execution traces), not output analysis.

## Key Claims

1. Pre-task belief conditioning reduces agent search count by 26.9% — `[verified]`
2. Belief-prefilled agents visit 16.9% fewer unique sources — `[verified]`
3. Real-time persuasion during task execution has weak, inconsistent behavioral effects — `[verified]`
4. Persuasion effects manifest in behavioral patterns, escaping content-level auditing — `[argued]`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| [Persuasion Propagation](../entities/persuasion-propagation.md) | concept | new |

## Relations

- `Persuasion Propagation` `extends` `AI Commercial Persuasion` — shows mechanism is invisible pre-task
- `Persuasion Propagation` `contradicts` output-level auditing assumption

## Cross-References

- Related: `ai-commercial-persuasion.md` — commercial system prompt = pre-task belief conditioning
- Related: `lh-deception-long-horizon-agent` — invisible chains of deception
