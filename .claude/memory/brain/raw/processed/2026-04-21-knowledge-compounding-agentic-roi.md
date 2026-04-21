---
title: "Knowledge Compounding: An Empirical Economic Analysis of Self-Evolving Knowledge Wikis under the Agentic ROI Framework"
arxiv: "2604.11243"
fetched: 2026-04-21
source: https://arxiv.org/abs/2604.11243
authors: [Shuide Wen, Beier Ku]
tags: [knowledge-compounding, agentic-roi, token-efficiency, llm-wiki, multi-agent]
---

# Raw Extraction

## Key Concepts
- Agentic ROI framework for LLM cost analysis
- Knowledge compounding: persistent knowledge base lowers per-query cost over time
- LLM tokens reframed as capital goods (not consumables) — appreciate through knowledge accumulation
- Time-varying cost function: Cost(t) governed by knowledge-base coverage rate H(t)

## Main Claims
- Original Agentic ROI assumes task costs are independent — breaks down with persistent KB
- 4 sequential queries: 47K tokens (compounding) vs 305K tokens (RAG baseline) = 84.6% savings
- 30-day projection: 53.7% savings (medium) to 81.3% (high concentration)
- Three mechanisms: amortized ingestion costs, auto-feedback loops, external result write-back

## Methodology
- Controlled 4-query experiment
- Qing Claw (C# OpenClaw multi-agent framework)
- arXiv:2604.11243
