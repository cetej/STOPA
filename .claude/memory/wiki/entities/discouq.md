---
name: DiscoUQ
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [beyond-mode-research]
tags: [uncertainty, multi-agent, hypothesis, calibration, ensemble]
---
# DiscoUQ

> Framework (arXiv:2603.20975) running 5 role-differentiated parallel agents (Analytical, Devil's Advocate, Historical, Systematic + consensus) with a 17-feature disagreement classifier to produce calibrated P(correct).

## Key Facts

- 5 roles: Evidence-only, Devil's Advocate (minority interpretation), Historical (precedents), Systematic (logical consistency), plus consensus (ref: sources/beyond-mode-research.md)
- 17-feature disagreement classifier detects uncertainty signal from agent output divergence (ref: sources/beyond-mode-research.md)
- High embedding dispersion between agent outputs → flag for manual review (ref: sources/beyond-mode-research.md)
- Paper: arXiv:2603.20975 (ref: sources/beyond-mode-research.md)

## Relevance to STOPA

Reference architecture for MONITOR's competing hypotheses approach and for STOPA critic expansion. Disagreement between parallel agents is a direct uncertainty signal — when 2 of 5 agents disagree significantly, escalate rather than proceed.

## Mentioned In

- [Reaching Beyond the Mode — Multi-Answer RL and Uncertainty Quantification](../sources/beyond-mode-research.md)
