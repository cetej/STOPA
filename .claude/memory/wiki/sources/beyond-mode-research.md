---
title: "Reaching Beyond the Mode — Multi-Answer RL and Uncertainty Quantification"
slug: beyond-mode-research
source_type: research_output
date_ingested: 2026-04-07
entities_extracted: 8
claims_extracted: 5
---
# Reaching Beyond the Mode — Multi-Answer RL and Uncertainty Quantification

> **TL;DR**: MIT CSAIL paper (arXiv:2603.24844) trains LLMs via RLVR to generate K diverse answers in a single forward pass with structured tags, achieving 56% token savings vs best-of-K while improving calibration. Prompt-only replication fails — requires fine-tuning on 4×A100. The broader UQ ecosystem (KalshiBench prompt template, MixMCP market blending, DiscoUQ parallel agents, Conformal prediction) provides zero-to-low-cost adaptations applicable directly to STOPA orchestration and ORAKULUM forecasting.

## Key Claims

1. Multi-Answer RL generates K candidate answers in a single forward pass using structured tags, using 56% fewer tokens than best-of-K while maintaining the same recall — `[verified]`
2. Prompt-only approaches to multi-answer generation fail — fine-tuning is required; this was experimentally confirmed by the paper authors — `[verified]`
3. KalshiBench prompt template (`<think><answer><confidence>`) measurably improves LLM calibration on forecasting tasks — prompt template has larger impact than model size — `[verified]`
4. MixMCP blending market prior (α=0.7) with LLM estimate (α=0.3) outperforms either alone for event probability forecasting — `[verified]`
5. DiscoUQ 5-role parallel hypothesis agents with 17-feature disagreement classifier produces calibrated P(correct) — disagreement = uncertainty signal — `[verified]`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| Multi-Answer RL (arXiv:2603.24844) | paper | new |
| KalshiBench | concept | new |
| MixMCP | concept | new |
| DiscoUQ | concept | new |
| Conformal Prediction for LLMs | concept | new |
| PCE Decision Tree | concept | new |
| GRPO (Group Relative Policy Optimization) | concept | new |
| llm_osint | tool | new |

## Relations

- Multi-Answer RL `uses` GRPO
- KalshiBench `evaluates` calibration via Brier score / ECE
- MixMCP `blends` market prior with LLM estimate
- DiscoUQ `implements` parallel hypothesis agents
- Conformal Prediction for LLMs `provides` coverage guarantee for prediction sets
