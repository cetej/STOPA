---
source: arxiv.org/abs/2603.01896
date: 2026-04-25
type: paper
title: "Agentic Code Reasoning"
arxiv: "2603.01896"
wiki: concepts/agentic-code-reasoning.md
---

# Agentic Code Reasoning

## Authors
Shubham Ugare, Satish Chandra

## Key Concepts
- Agentic Code Reasoning: agents reason about code semantics WITHOUT execution
- Semi-formal reasoning: explicit premises → execution paths → formal conclusions
- Functions as verifiable certificate (prevents skipping cases / unsupported claims)
- Execution-free reward signals for RL training

## Main Claims
Structured semi-formal prompting substantially outperforms unstructured CoT on code reasoning. The verification-certificate framing forces agents to demonstrate logical rigor instead of asserting answers.

## Core Findings
- Patch equivalence accuracy: 78% → 88% on curated set; 93% on real-world patches
- Code QA on RubberDuckBench: 87% accuracy
- Fault localization on Defects4J: +5 points Top-5 accuracy
- Enables execution-free reward signals for code RL pipelines

## Entities
- RubberDuckBench, Defects4J
- arXiv: 2603.01896
- Subject: Software Engineering / AI / Programming Languages
