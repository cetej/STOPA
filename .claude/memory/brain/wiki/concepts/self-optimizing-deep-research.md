---
title: Self-Optimizing Multi-Agent Deep Research
category: concepts
tags: [deep-research, self-optimization, multi-agent, prompt-optimization, self-play]
sources: [raw/processed/2026-04-22-self-optimizing-deep-research.md]
updated: 2026-04-22
---

# Self-Optimizing Multi-Agent Deep Research

**Paper**: arXiv:2604.02988  
**Authors**: Arthur Câmara, Vincent Slot, Jakub Zavrel  
**Venue**: ECIR 2026 — Workshop on Conversational Search for Complex Information Needs

## Core Finding

"Enabling agents to self-play and explore different prompt combinations can produce high-quality Deep Research systems" that rival expert-engineered approaches.

Self-play optimization → removes dependency on expert prompt engineering.

## Architecture

| Component | Role |
|-----------|------|
| Orchestrator agent | Coordinates overall research process |
| Parallel worker agents | Execute individual research subtasks |
| Self-play mechanism | Agents explore prompt variations autonomously |

The system learns which prompt configurations work best through experimentation — without human engineers manually tuning prompts.

## Key Shift

| Before | After |
|--------|-------|
| Static architecture | Adaptive self-improving |
| Hand-crafted prompts | Learned through self-play |
| Brittle manual maintenance | Self-correcting |
| Expert-dependent | Scalable |

## Significance

1. **Prompt engineering bottleneck removed**: agents discover effective strategies themselves
2. **Parity with expert systems**: self-optimizing systems match/surpass manually engineered ones
3. **Scalability**: no need for human prompt tuning as tasks evolve

## STOPA Relevance

Directly relevant to STOPA's `/autoresearch` skill. Current autoresearch uses fixed strategy templates per iteration. Self-play optimization would allow autoresearch to:
- Try multiple prompt strategies per research question
- Keep configurations that produced better eval scores
- Build a library of effective strategies across sessions

The self-play mechanism parallels STOPA's SEPL ε→κ (Evaluate→Commit) loop but applied to the orchestrator's own prompts, not just the target artifact.

## Related Concepts

→ [swe-agents-survey.md](swe-agents-survey.md)  
→ [critical-step-optimization.md](critical-step-optimization.md)  
→ [memfactory.md](memfactory.md)
