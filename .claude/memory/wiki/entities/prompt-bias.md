---
name: Prompt Bias
type: concept
first_seen: 2026-04-13
last_updated: 2026-04-13
sources: [autoreason-self-refinement-framework]
tags: [evaluation, anti-pattern, review, orchestration]
---

# Prompt Bias

> Anti-pattern in critique-and-revise systems where asking a model to "find improvements" causes it to hallucinate flaws even in perfect outputs, because the prompt primes for critique regardless of actual quality.

## Key Facts

- Identified as one of 3 core failure modes in self-refinement loops (alongside scope creep and lack of restraint) (ref: sources/autoreason-self-refinement-framework.md)
- Manifests as: model always produces critique, never outputs "no changes needed" (ref: sources/autoreason-self-refinement-framework.md)
- Solution: tournament architecture where A (unchanged) always competes — "do nothing" is structurally valid (ref: sources/autoreason-self-refinement-framework.md)
- Measured in baselines: standard critique-and-revise scores degrade below single-pass quality (ref: sources/autoreason-self-refinement-framework.md)

## Relevance to STOPA

Core failure mode in STOPA's `/critic` skill when used in loops — critic asked to find issues will find (or invent) them. Tournament architecture with blind voting directly mitigates this. Also relevant to `/autoreason` and any iterative quality loop.

## Mentioned In

- [Autoreason: Self-Refinement That Knows When to Stop](../sources/autoreason-self-refinement-framework.md)
