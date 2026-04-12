---
name: Resolver Context Router
type: concept
first_seen: 2026-04-12
last_updated: 2026-04-12
sources: [garry-tan-thin-harness-fat-skills]
tags: [skill-design, orchestration, memory, routing]
---

# Resolver (Context Router)

> A routing table for context — detects the current task type and loads the appropriate skill or reference document, rather than stuffing everything into the system prompt.

## Key Facts

- Task type detected → Resolver activates → Relevant skill/doc loaded → Model proceeds (ref: sources/garry-tan-thin-harness-fat-skills.md)
- Example: developer changes a prompt → resolver loads docs/EVALS.md → model knows to run eval suite (ref: sources/garry-tan-thin-harness-fat-skills.md)
- Scales infinitely: CLAUDE.md can shrink to ~200 lines of pointers instead of 20,000 lines of content (ref: sources/garry-tan-thin-harness-fat-skills.md)
- Built-in resolver in CC: skill `description` field matches user intent automatically — "You never have to remember that /ship exists" (ref: sources/garry-tan-thin-harness-fat-skills.md)
- Resolver design: don't memorize context, route to it on demand (ref: sources/garry-tan-thin-harness-fat-skills.md)

## Relevance to STOPA

STOPA's skill `description` field IS the built-in resolver. The CLAUDE.md @-include pattern (CLAUDE.md with @RTK.md pointers) is the manual resolver layer. `/triage` is the explicit routing skill when description-matching fails.

## Mentioned In

- [Key Concepts for AI Agentic Skills Design — Thin Harness Fat Skills](../sources/garry-tan-thin-harness-fat-skills.md)
