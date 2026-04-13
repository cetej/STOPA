---
title: "Proactive Defense: Compound AI for Detecting Persuasion Attacks and Measuring Inoculation Effectiveness"
slug: bries-compound-ai-persuasion-defense
source_type: url
url: "https://arxiv.org/abs/2511.21749"
date_ingested: 2026-04-13
date_published: "2025-11-23"
entities_extracted: 1
claims_extracted: 4
---

# BRIES — Compound AI Persuasion Defense

> **TL;DR**: Multi-agent defense system (Twister/Detector/Defender/Assessor) for persuasion detection. GPT-4 achieves F1>0.90 on explicit fallacies but open-source models fail on subtle rhetorical patterns. Temperature tuning critically impacts detection. Deepresearch found F1<0.20 for the specific patterns Princeton identified as most effective (active hedging, understated description).

## Key Claims

1. GPT-4 achieves superior detection on complex persuasion techniques vs Llama3/Mistral — `[verified]`
2. Temperature settings critically influence detection (Gemma/GPT-4 better at low temp, Llama3/Mistral at high) — `[verified]`
3. Different attack types target specific cognitive dimensions (socio-emotional-cognitive signatures) — `[argued]`
4. Subtle rhetorical patterns (omission-based, tonal asymmetry) remain undetectable by current compound AI — `[verified]` (Princeton cross-reference)

## Entities

| Entity | Type | Status |
|--------|------|--------|
| [BRIES](../entities/bries.md) | tool | new |

## Relations

- `BRIES` `attempts_to_solve` `AI Commercial Persuasion` — but fails on subtle patterns
- `BRIES` `uses` compound AI architecture — 4 specialized agents

## Cross-References

- Related: `ai-commercial-persuasion.md` — BRIES detection gap = Princeton's most effective patterns
- Related: `general-security-environment.md` — security defense architecture
