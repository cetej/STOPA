---
name: Persuasion Propagation
type: concept
first_seen: 2026-04-13
last_updated: 2026-04-13
sources: [persuasion-propagation-llm-agents]
tags: [persuasion, agent-behavior, audit, ai-safety, invisible-bias]
---

# Persuasion Propagation

> The phenomenon where pre-task belief conditioning in LLM agents creates substantial behavioral changes (26.9% fewer searches, 16.9% fewer sources) while being invisible to output-level auditing.

## Key Facts

- Pre-task belief conditioning reduces search count by 26.9% and unique sources by 16.9% (ref: sources/persuasion-propagation-llm-agents.md)
- Real-time persuasion DURING task execution has weak/inconsistent effects — timing matters (ref: sources/persuasion-propagation-llm-agents.md)
- Effects manifest in behavioral patterns (tool use, search breadth), NOT in output content — content-level auditing misses it (ref: sources/persuasion-propagation-llm-agents.md)
- Detection requires execution trace monitoring: query diversity, source breadth, tool-use patterns, search termination (ref: sources/persuasion-propagation-llm-agents.md)

## Why This Matters

Commercial system prompts ARE pre-task belief conditioning. An AI shopping assistant with "promote product X" in its system prompt will narrow its search/comparison space before generating any output — the final recommendation looks normal but was explored from a biased starting point.

## Relevance to STOPA

STOPA agents receiving task context from orchestrator could be subject to propagation if the orchestrator's framing contains implicit bias. Detection: monitor sub-agent tool invocation diversity relative to task complexity. If an agent with broad search capability consistently narrows to a small option set, propagation may be occurring.

## Mentioned In

- [Persuasion Propagation in LLM Agents](../sources/persuasion-propagation-llm-agents.md)
