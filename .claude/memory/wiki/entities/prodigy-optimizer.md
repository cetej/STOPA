---
name: Prodigy Optimizer
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [gradient-descent-research]
tags: [deep-learning, optimization]
---

# Prodigy Optimizer

> LR-free adaptive optimizer (arXiv:2306.06101, Mishchenko & Defazio); improvement over D-Adaptation; standard choice for LoRA fine-tuning.

## Key Facts

- Extends D-Adaptation; automatically estimates effective learning rate (ref: sources/gradient-descent-research.md)
- De facto standard for LoRA fine-tuning workflows (ref: sources/gradient-descent-research.md)
- ICML 2023 Outstanding Paper for D-Adaptation (predecessor) (ref: sources/gradient-descent-research.md)
- arXiv:2306.06101 (ref: sources/gradient-descent-research.md)

## Relevance to STOPA

Already referenced in STOPA's optimizer cheat sheet (reference_optimizers_finetuning.md): "Prodigy (LoRA)". This research confirms its standard status.

## Mentioned In

- [Gradient Descent Research](../sources/gradient-descent-research.md)
