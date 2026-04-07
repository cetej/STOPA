---
name: MixMCP
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [beyond-mode-research]
tags: [calibration, forecasting, uncertainty, market-prior, prediction-markets]
---
# MixMCP

> Method for blending prediction market prior probability (α=0.7) with LLM probability estimate (α=0.3) to produce better-calibrated event forecasts than either alone; paper arXiv:2602.21229.

## Key Facts

- Formula: `p_final = 0.7 × market_price + 0.3 × LLM_estimate` (ref: sources/beyond-mode-research.md)
- α=0.7 was empirically optimal on KalshiBench-style evaluation (ref: sources/beyond-mode-research.md)
- Paper: arXiv:2602.21229 (ref: sources/beyond-mode-research.md)
- Transfer caveat: α=0.7 validated on policy questions (Kalshi); may differ for crypto/sports on Polymarket (ref: sources/beyond-mode-research.md)

## Relevance to STOPA

Direct implementation target for ORAKULUM/POLYBOT: when Polymarket market price is available, blend it with LLM estimate at 0.7/0.3 ratio. Measurably better calibration than relying on LLM alone.

## Mentioned In

- [Reaching Beyond the Mode — Multi-Answer RL and Uncertainty Quantification](../sources/beyond-mode-research.md)
