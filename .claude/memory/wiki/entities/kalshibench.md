---
name: KalshiBench
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [beyond-mode-research]
tags: [calibration, forecasting, uncertainty, prompt-template]
---
# KalshiBench

> Benchmark and prompt template (arXiv:2512.16030) for evaluating LLM calibration on prediction market questions; the `<think><answer><confidence>` template measurably improves calibration, with prompt template impact exceeding model size impact.

## Key Facts

- Evaluated on 300 real Kalshi questions using ECE (Expected Calibration Error) and Brier score (ref: sources/beyond-mode-research.md)
- Prompt template: `<think>[reasoning]</think><answer>[yes/no]</answer><confidence>[0-100]</confidence>` (ref: sources/beyond-mode-research.md)
- Larger models are better calibrated; but prompt template has larger impact than model size (ref: sources/beyond-mode-research.md)
- Paper: arXiv:2512.16030 (ref: sources/beyond-mode-research.md)

## Relevance to STOPA

Immediately applicable to ORAKULUM project — add `<think><answer><confidence>` template to all forecasting prompts. Zero cost, measurable calibration improvement. Also useful in any STOPA orchestrate decision where probability estimates are needed.

## Mentioned In

- [Reaching Beyond the Mode — Multi-Answer RL and Uncertainty Quantification](../sources/beyond-mode-research.md)
