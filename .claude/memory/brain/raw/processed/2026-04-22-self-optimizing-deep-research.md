---
title: Self-Optimizing Multi-Agent Systems for Deep Research
source_url: https://arxiv.org/abs/2604.02988
fetched: 2026-04-22
type: arxiv-paper
authors: Arthur Câmara, Vincent Slot, Jakub Zavrel
---

# Self-Optimizing Multi-Agent Systems for Deep Research

**Paper**: arXiv:2604.02988  
**Venue**: ECIR 2026 (Workshop on Conversational Search for Complex Information Needs)

## Abstract

Deep Research multi-agent systems plan, retrieve, and synthesize evidence across many documents. Instead of manually crafted prompts + fixed architectures, this work explores self-play optimization enabling agents to autonomously discover high-quality prompt configurations.

## Key Contributions

**Core finding**: "enabling agents to self-play and explore different prompt combinations can produce high-quality Deep Research systems" that rival expert-engineered approaches.

**Architecture**:
- Orchestrator agent coordinates overall process
- Parallel worker agents execute individual research tasks
- Agents autonomously experiment with prompt variations through self-play

## Significance

- Shifts from static hand-crafted systems to adaptive self-improving architectures
- Self-optimizing systems can match/surpass manually engineered solutions
- Reduces development cost and maintenance overhead
- Prompt engineering bottleneck → learned through agent self-play

## Connection to STOPA

Maps to STOPA's `/autoresearch` skill which iterates on research strategies. The self-play optimization pattern suggests autoresearch could be enhanced to try multiple prompt strategies autonomously rather than relying on a fixed approach.
