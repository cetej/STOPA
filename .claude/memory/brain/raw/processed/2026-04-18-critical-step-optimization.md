---
date: 2026-04-18
source: https://arxiv.org/abs/2602.03412
type: paper
title: "Verified Critical Step Optimization for LLM Agents"
authors: Mukai Li, Qingcheng Zeng, Tianqing Fang, Zhenwen Liang, Linfeng Song, Qi Liu, Haitao Mi, Dong Yu
tags: [rl, post-training, critical-steps, process-reward, preference-learning, agent-optimization]
---

## Summary

Critical Step Optimization (CSO) focuses preference learning only on "critical steps" — decision points where alternate actions demonstrably flip outcomes from failure to success. Analyzes failed trajectories, uses PRMs to identify candidate critical steps, verifies alternatives through continued policy execution. Uses only verified successful alternatives for training. 37% relative improvement on GAIA-Text-103, 26% on XBench-DeepSearch, using supervision at only 16% of trajectory steps.

## Key Concepts

- Critical steps: decision points where action flips failure→success
- Process Reward Models (PRMs) to identify candidate critical steps
- Verified alternatives: only train on steps confirmed successful
- 16% supervision coverage achieves 37% improvement
- Complements trajectory-level preference learning

## Claims

- 37% relative improvement on GAIA-Text-103
- 26% relative improvement on XBench-DeepSearch
- Only 16% of trajectory steps need supervision
- Verified alternatives > noisy step-level labels

## Entities

Authors: Mukai Li, Qingcheng Zeng, Tianqing Fang, Zhenwen Liang, Linfeng Song, Qi Liu, Haitao Mi, Dong Yu
Benchmarks: GAIA-Text-103, XBench-DeepSearch
