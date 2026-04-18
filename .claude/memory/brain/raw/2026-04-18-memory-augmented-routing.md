---
date: 2026-04-18
source: https://arxiv.org/abs/2603.23013
type: paper
title: "Knowledge Access Beats Model Size: Memory Augmented Routing for Persistent AI Agents"
authors: Xunzhuo Liu, Bowei He, Xue Liu, Andy Luo, Haichen Zhang, Huamin Chen
tags: [memory, routing, retrieval, hybrid-retrieval, cost-reduction, persistent-agents]
---

## Summary

Shows that up to 47% of production queries are semantically similar to prior interactions. A lightweight 8B model with retrieved conversational context recovers 69% of a 235B model's performance while reducing inference cost by 96%. Memory and knowledge access matter more than raw model scale for user-specific repetitive queries. Hybrid retrieval (BM25 + cosine similarity) adds +7.7 F1 over either method alone.

## Key Concepts

- Memory-augmented routing: route queries to cheap/expensive inference based on memory hit
- Knowledge access > model size for repetitive user-specific queries
- 47% of production queries semantically similar to prior interactions
- 8B + memory = 69% of 235B model performance at 4% cost
- Hybrid retrieval: BM25 + cosine similarity, +7.7 F1 over single method

## Claims

- 96% cost reduction vs large model, 69% performance recovery
- 96% of queries can be routed to cheap inference path
- Hybrid retrieval consistently outperforms single-method retrieval

## Entities

Authors: Xunzhuo Liu, Bowei He, Xue Liu, Andy Luo, Haichen Zhang, Huamin Chen
Benchmarks: LoCoMo (152 questions), LongMemEval (500 questions)
