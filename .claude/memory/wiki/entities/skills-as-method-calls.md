---
name: Skills as Method Calls
type: concept
first_seen: 2026-04-12
last_updated: 2026-04-12
sources: [garry-tan-thin-harness-fat-skills]
tags: [skill-design, orchestration]
---

# Skills as Method Calls

> A skill is a parameterized procedure: same steps + different arguments = radically different capability. Skills encode the process; invocations supply the domain.

## Key Facts

- Contrast: Prompt = WHAT to do (task-bound). Skill = HOW to do it (reusable, parameterized) (ref: sources/garry-tan-thin-harness-fat-skills.md)
- Example: `/investigate TARGET QUESTION DATASET` — same 7 steps produces safety investigator OR forensic accountant depending on parameters (ref: sources/garry-tan-thin-harness-fat-skills.md)
- Example: `/match-breakout` (sector-homogeneous, 30/room) vs `/match-lunch` (cross-sector serendipity, 8/table) vs `/match-live` (nearest-neighbor, 200ms) — same capability, three parameterizations (ref: sources/garry-tan-thin-harness-fat-skills.md)
- Skills contain: process (steps), judgment (when/how to weigh), context (domain knowledge), constraints (what NOT to do) (ref: sources/garry-tan-thin-harness-fat-skills.md)
- Design principle: write skills with clear parameter slots; process encodes judgment, invocation supplies domain (ref: sources/garry-tan-thin-harness-fat-skills.md)

## Relevance to STOPA

Justifies STOPA's generalist skill design over task-specific scripts. A well-parameterized skill like `/orchestrate` or `/deepresearch` serves dozens of domains without modification.

## Mentioned In

- [Key Concepts for AI Agentic Skills Design — Thin Harness Fat Skills](../sources/garry-tan-thin-harness-fat-skills.md)
