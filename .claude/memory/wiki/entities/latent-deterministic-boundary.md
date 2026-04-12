---
name: Latent-Deterministic Boundary
type: concept
first_seen: 2026-04-12
last_updated: 2026-04-12
sources: [garry-tan-thin-harness-fat-skills]
tags: [skill-design, orchestration, architecture]
---

# Latent-Deterministic Boundary

> The design boundary separating model judgment (latent space operations) from code execution (deterministic operations) — confusing the two is the most common mistake in agent design.

## Key Facts

- **Latent** (model does): judgment, synthesis, pattern recognition, interpretation, quality assessment (ref: sources/garry-tan-thin-harness-fat-skills.md)
- **Deterministic** (code does): database queries, arithmetic, file operations, API calls, combinatorial optimization (ref: sources/garry-tan-thin-harness-fat-skills.md)
- "Dinner table test": LLM seats 8 people considering personalities = fine. 800 people = hallucinated seating chart that looks plausible (ref: sources/garry-tan-thin-harness-fat-skills.md)
- Correct pattern: Latent (interpret task) → Deterministic (query/compute) → Latent (synthesize) → Deterministic (format/write) → Latent (verify) (ref: sources/garry-tan-thin-harness-fat-skills.md)
- Skills should orchestrate the boundary — tell model what judgment to apply, hand off to deterministic for execution (ref: sources/garry-tan-thin-harness-fat-skills.md)

## Relevance to STOPA

Critical design principle for all skills: steps should alternate between model reasoning (in skill body) and tool calls (Python/Bash). Skills that push deterministic work into model reasoning produce unreliable outputs.

## Mentioned In

- [Key Concepts for AI Agentic Skills Design — Thin Harness Fat Skills](../sources/garry-tan-thin-harness-fat-skills.md)
