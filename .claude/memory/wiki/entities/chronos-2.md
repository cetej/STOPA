---
name: Chronos-2
type: tool
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [prediction-research]
tags: [time-series, forecasting, foundation-model, amazon]
---

# Chronos-2

> Amazon's time series foundation model, #1 on GIFT-Eval 2026; encoder-only 120M parameters with multivariate + covariate support.

## Key Facts

- #1 on GIFT-Eval benchmark (23 datasets, 144K series, 177M datapoints) (ref: sources/prediction-research.md)
- Encoder-only architecture, 120M parameters (ref: sources/prediction-research.md)
- Supports multivariate time series and covariates — unlike original Chronos (ref: sources/prediction-research.md)
- Zero-shot inference — no training required for new domains (ref: sources/prediction-research.md)
- Paper: arXiv:2510.15821 (Ansari et al., Amazon 2025) (ref: sources/prediction-research.md)

## Relevance to STOPA

Recommended numeric forecasting component for ORAKULUM and prediction module. Use for zero-shot time series prediction after LLM-based event encoding. Counterpart to TimesFM — no single benchmark winner, choose based on dataset type.

## Mentioned In

- [Prediction Systems Research](../sources/prediction-research.md)
