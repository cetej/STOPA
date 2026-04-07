---
name: Context Rot
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [vertical-scaling-research]
tags: [context-engineering, token-efficiency, llm-behavior]
---

# Context Rot

> Chroma Research finding that ALL tested LLMs degrade in performance as context length increases; even 1 distractor document degrades output, 4 distractors compound the effect.

## Key Facts

- Source: Chroma Research (https://research.trychroma.com/context-rot) (ref: sources/vertical-scaling-research.md)
- All 18 tested models degrade with longer context (ref: sources/vertical-scaling-research.md)
- Claude shows the largest gap between focused (~300 tokens) and full context (~113K) (ref: sources/vertical-scaling-research.md)
- Even 1 distractor document reduces performance (ref: sources/vertical-scaling-research.md)
- Counterintuitive: shuffled haystacks outperform logically structured ones (ref: sources/vertical-scaling-research.md)

## Relevance to STOPA

Key justification for level-tagged context in vertical scaling: give each agent only the context relevant to its abstraction level. Contradicts the assumption that more context = better results. Directly impacts orchestrate worker context design.

## Mentioned In

- [Vertikální škálování Research](../sources/vertical-scaling-research.md)
