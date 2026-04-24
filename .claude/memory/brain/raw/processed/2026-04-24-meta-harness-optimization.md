---
source: arxiv.org/abs/2603.28052
date: 2026-04-24
type: paper
title: "Meta-Harness: End-to-End Optimization of Model Harnesses"
arxiv: "2603.28052"
wiki: concepts/meta-harness-optimization.md
---

# Meta-Harness: End-to-End Optimization of Model Harnesses

## Authors
Yoonho Lee, Roshen Nair, Qizheng Zhang, Kangwook Lee, Omar Khattab, Chelsea Finn

## Key Concepts
- Model harness = code determining information storage, retrieval, and presentation
- Automated harness optimization via code search (not text optimization)
- Context management systems as first-class optimization target
- Retrieval-Augmented Generation harness engineering
- TerminalBench-2 for agentic coding evaluation

## Main Claims
LLM performance depends significantly on harness implementation, not just model weights. Existing text optimizers are unsuitable for harness optimization — they "compress feedback too aggressively." Meta-Harness searches over the space of possible harness implementations programmatically.

## Core Findings
- Text classification: +7.7 points over SOTA context management, −75% context tokens
- Math reasoning: +4.7 accuracy on 200 IMO-level problems across 5 models
- Agentic coding: automated harnesses outperform hand-engineered baselines on TerminalBench-2
- Key insight: harness = programmable context engineering layer

## Entities
- Meta-Harness system
- TerminalBench-2 (agentic coding benchmark)
- Omar Khattab (DSPy connection: programmatic optimization)
- arXiv: 2603.28052 (March 2026, cs.AI)
