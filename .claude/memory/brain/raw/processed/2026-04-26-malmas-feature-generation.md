---
source: arxiv.org/abs/2604.20261
date: 2026-04-26
type: paper
title: "Memory-Augmented LLM-based Multi-Agent System for Automated Feature Generation on Tabular Data"
arxiv: "2604.20261"
venue: "ACL 2026"
wiki: concepts/malmas-feature-generation.md
---

# MALMAS — Memory-Augmented Multi-Agent for Tabular Feature Generation

## Authors
Fengxian Dong, Zhi Zheng, Xiao Han, Wei Chen, Jingqing Ruan, Tong Xu, Yong Chen, Enhong Chen

## Key Concepts
- Multi-agent decomposition of feature generation
- Router Agent: dynamically activates appropriate agent subset per iteration
- Three memory types: procedural (HOW operations), feedback (WHAT worked), conceptual (WHY semantically)
- Semantic-aware feature creation leveraging LLM domain knowledge

## Main Claims
Existing AutoML feature generation relies on fixed operator libraries (no semantics) or LLM-based systems with predetermined patterns (constrained search space). MALMAS expands the search via dynamic agent routing and memory-driven refinement.

## Core Findings
- Router-driven dynamic activation expands feature space exploration
- Three-layer memory enables iterative refinement toward higher-quality, more diverse features
- ACL 2026 acceptance
- Code: GitHub fxdong24/MALMAS

## Entities
- ACL 2026
- arXiv: 2604.20261
- Subject: ML / AutoML / Tabular Data
