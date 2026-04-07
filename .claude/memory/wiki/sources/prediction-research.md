---
title: "Prediction Systems — Research Brief"
slug: prediction-research
source_type: research_output
date_ingested: 2026-04-07
entities_extracted: 10
claims_extracted: 5
---

# Prediction Systems — Research Brief

> **TL;DR**: Survey of state-of-the-art modular prediction and forecasting approaches. The dominant 2024-2025 paradigm combines LLMs as event reasoners with purpose-built numeric forecasters (Chronos-2, TimesFM). No single library handles the full heterogeneous correlation problem — practical solution is a 3-layer pipeline: encode text/events → causal discovery via Tigramite → predict with Chronos-2 or Darts.

## Key Claims

1. Using LLMs directly as numeric forecasters is unreliable — removing the LLM from Time-LLM-style models often improves performance. — `[verified]`
2. Chronos-2 (Amazon) ranks #1 on GIFT-Eval 2026; TimesFM 2.0 (Google) ranks #1 on Monash benchmark — no universal winner. — `[verified]`
3. 12-LLM ensemble is statistically equivalent to a 925-person human crowd on forecasting tournament questions. — `[verified]`
4. Best LLM (o3) Brier 0.1352 vs superforecaster median 0.0225 — still a 6× gap as of 2025. — `[verified]`
5. Feast feature store is the recommended cross-project backbone for multi-project prediction reuse. — `[argued]`

## Relations

- Chronos-2 `ranks #1 on` GIFT-Eval
- Tigramite `is best tool for` time series causal discovery
- autopredict `is execution agent for` Polymarket (does NOT generate predictions)
- PyWhy `contains` DoWhy, causal-learn, EconML
- LAMP `combines` Temporal Point Process + LLM abductive reasoning + EBM reranking

## Entities

| Entity | Type | Status |
|--------|------|--------|
| Chronos-2 | tool | new |
| TimesFM | tool | new |
| Tigramite | tool | new |
| GIFT-Eval | concept | new |
| autopredict | tool | new |
| PyWhy | tool | new |
| LAMP | paper | new |
| Feast | tool | new |
| ForecastBench | concept | new |
| GDELT | concept | new |
