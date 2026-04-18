---
date: 2026-03-23
type: best_practice
severity: high
component: skill
tags: [competitive-analysis, superpowers, anti-rationalization, trigger-description]
uses: 1
summary: "superpowers v5 insight: skill description triggers matching — CC reads description, not body. Anti-rationalization prompts improve quality."
source: external_research
maturity: draft
confidence: 1.0
---

## Problém
Analysis of obra/superpowers (v5.0.5) for pattern adoption into STOPA.

## Root Cause
N/A — adoption analysis.

## Reseni
5 adopted patterns: two-stage review, agent status codes, anti-rationalization tables, trigger-only descriptions, 3-fix escalation. Key insight: skill description summary causes Claude to shortcut instead of reading full body (tested and confirmed). DONE_WITH_CONCERNS status is highest value — prevents silent shipping.

## Prevence
Always test skill descriptions empirically — summaries look helpful but degrade execution quality.
