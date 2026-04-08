---
name: Activation Steering
type: concept
first_seen: 2026-04-08
last_updated: 2026-04-08
sources: [llms-follow-instructions-skillful-coordination]
tags: [interpretability, orchestration, model-intervention]
---

# Activation Steering

> Technique that injects or modifies activation vectors at specific model layers to steer model behavior without changing weights.

## Key Facts

- Structural constraints (format, word count) live in early layers — steering there affects formatting compliance (ref: sources/llms-follow-instructions-skillful-coordination.md)
- Semantic constraints (topic, sentiment) live in late layers — steering there affects content (ref: sources/llms-follow-instructions-skillful-coordination.md)
- Layer-type mapping enables *targeted* steering: intervention at wrong layer = low effect; intervention at right layer = high effect (ref: sources/llms-follow-instructions-skillful-coordination.md)
- Previously used for alignment interventions (Anthropic emotion vectors — calm steering, desperation suppression)

## Relevance to STOPA

STOPA's panic-detector hook applies behavioral steering via hook injection. Understanding that structural vs semantic constraints live at different layers could inform more targeted hook intervention points if STOPA moves to activation-level steering in future.

## Mentioned In

- [How LLMs Follow Instructions: Skillful Coordination, Not a Universal Mechanism](../sources/llms-follow-instructions-skillful-coordination.md)
