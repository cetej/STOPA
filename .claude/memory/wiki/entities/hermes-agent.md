---
name: Hermes Agent
type: tool
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [swarm-kb-research]
tags: [orchestration, code-quality, review]
---

# Hermes Agent

> NousResearch AI agent with a quality gate architecture: 3-axis scoring (procedure adherence × output correctness × token conciseness), fail-closed JSON contract, and reviewer isolation.

## Key Facts

- Developed by NousResearch (ref: sources/swarm-kb-research.md)
- 3-axis scoring: procedure adherence, output correctness, token conciseness (0-1 each) (ref: sources/swarm-kb-research.md)
- Fail-closed contract: `security_concerns.length > 0 OR logic_errors.length > 0` → `passed = false` (ref: sources/swarm-kb-research.md)
- Reviewer isolation: fresh LLM context, XML data wrapping, truncated diff (max 15K chars) (ref: sources/swarm-kb-research.md)
- Quality gate architecture (issue #406) is a community proposal, not confirmed shipped code (ref: sources/swarm-kb-research.md)
- Skills = structured prompt injection with CRUD layer, not actual capability change (ref: sources/swarm-kb-research.md)

## Relevance to STOPA

Fail-closed JSON contract pattern is directly adoptable in `/critic` skill — replace free-form text verdict with structured `{passed, security_concerns, logic_errors, suggestions, confidence}`. Reviewer isolation techniques prevent verbosity bias.

## Mentioned In

- [Swarm KB Research](../sources/swarm-kb-research.md)
