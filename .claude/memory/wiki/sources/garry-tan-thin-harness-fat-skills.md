---
title: "Key Concepts for AI Agentic Skills Design (Thin Harness, Fat Skills)"
slug: garry-tan-thin-harness-fat-skills
source_type: file
url: ""
date_ingested: 2026-04-12
date_published: "2026 (exact date unknown)"
author: Garry Tan
entities_extracted: 7
claims_extracted: 7
---

# Key Concepts for AI Agentic Skills Design — Thin Harness, Fat Skills

> **TL;DR**: Skills are parameterized method calls encoding judgment and process; the harness should be ~200 lines of code; intelligence belongs in skills (fat), not in the harness (thin). The latent/deterministic boundary is the foundational design decision in every agent system.

## Key Claims

1. "Every step in your system is either latent (model judgment) or deterministic (code) — confusing them is the most common mistake in agent design" — `[argued]`
2. Purpose-built narrow tools are 75× faster than generic MCP wrappers (Playwright CLI 100ms vs Chrome MCP 15s per operation) — `[verified]`
3. Skill improvement via learning loop: examine execution traces → extract patterns → write rules back into skill file (12% OK → 4% OK, 66% improvement) — `[verified]`
4. The thin harness is ~200 lines of code; fat skills contain 90% of the value — `[asserted]`
5. Diarization is a latent-only operation: "No SQL query produces this. No RAG pipeline produces this." — `[argued]`
6. "If I ask you for something twice, you failed." — all repeated tasks must become skills — `[asserted]`
7. Markdown is "a more perfect encapsulation of capability than rigid source code" because it describes process, judgment, and context in the model's native language — `[argued]`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| [Garry Tan](../entities/garry-tan.md) | person | new |
| [Thin Harness Fat Skills](../entities/thin-harness-fat-skills.md) | concept | new |
| [Diarization Intelligence](../entities/diarization-intelligence.md) | concept | new |
| [Latent-Deterministic Boundary](../entities/latent-deterministic-boundary.md) | concept | new |
| [Resolver Context Router](../entities/resolver-context-router.md) | concept | new |
| [Skills as Method Calls](../entities/skills-as-method-calls.md) | concept | new |
| [Purpose-Built Tooling](../entities/purpose-built-tooling.md) | concept | new |

## Relations

- `thin-harness-fat-skills` `part_of` `three-layer-architecture` — describes the overall architecture
- `diarization-intelligence` `part_of` `fat-skills` — diarization is the model-judgment layer of knowledge extraction
- `latent-deterministic-boundary` `part_of` `thin-harness-fat-skills` — boundary defines the interface between layers
- `resolver-context-router` `inspired_by` `skill-description-routing` — built-in resolver in CC maps exactly to the concept
- `purpose-built-tooling` `competes_with` `mcp` — narrow Python tools vs. generic MCP wrappers (75× speed difference)
- `skills-as-method-calls` `extends` `skill-design` — parameterization principle extends STOPA skill design rules
- `garry-tan` created `thin-harness-fat-skills` (framework)

## Cross-References

- Related learnings: `karpathy-nopriors-autoagent-loopy-era.md` (program.md = fat skills), `2026-04-08-education-teaches-agents-not-humans.md` (skills educate agents)
- Related wiki articles: [skill-design](../skill-design.md) (description routing, compact variants), [pipeline-engineering](../pipeline-engineering.md) (harness/deterministic layer)
- Contradictions: none — validates and extends existing STOPA design principles
