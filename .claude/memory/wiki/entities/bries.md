---
name: BRIES
type: tool
first_seen: 2026-04-13
last_updated: 2026-04-13
sources: [bries-compound-ai-persuasion-defense]
tags: [persuasion, detection, compound-ai, defense, ai-safety]
---

# BRIES

> Compound AI system for detecting persuasion attacks using 4 specialized agents: Twister (adversarial content generation), Detector (attack classification), Defender (inoculation content), Assessor (causal effectiveness measurement).

## Key Facts

- GPT-4 as Detector achieves F1>0.90 on explicit fallacies (Appeal to Authority, Fear, Flag Waving) (ref: sources/bries-compound-ai-persuasion-defense.md)
- F1<0.20 on subtle patterns: Red Herring, Conversation Killer, Questioning Reputation — precisely the patterns Princeton found most commercially effective (ref: sources/bries-compound-ai-persuasion-defense.md)
- Temperature tuning critical: GPT-4/Gemma optimal at low temp, Llama3/Mistral at high temp (ref: sources/bries-compound-ai-persuasion-defense.md)
- Maps attack types to socio-emotional-cognitive signatures for targeted inoculation (ref: sources/bries-compound-ai-persuasion-defense.md)

## Critical Limitation

The system's failure mode aligns exactly with the commercially most effective persuasion: omission-based tactics (selective neglect, understated description, asymmetric hedging) are not explicit enough for classifier-based detection.

## Relevance to STOPA

If STOPA implements persuasion detection for agent outputs, BRIES architecture is a starting point but insufficient alone. Must be augmented with asymmetry scoring (description length ratio, clout differential) to cover the subtle patterns.

## Mentioned In

- [Proactive Defense: Compound AI](../sources/bries-compound-ai-persuasion-defense.md)
