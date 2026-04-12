---
name: Purpose-Built Tooling
type: concept
first_seen: 2026-04-12
last_updated: 2026-04-12
sources: [garry-tan-thin-harness-fat-skills]
tags: [skill-design, harness, orchestration, devops]
---

# Purpose-Built Tooling

> Narrow, domain-specific tools purpose-built for one workflow, rather than generic API wrappers that expose every endpoint as a tool.

## Key Facts

- Playwright CLI per browser operation: ~100ms. Chrome MCP (screenshot → find → click → wait → read): ~15 seconds. Difference: 75× (ref: sources/garry-tan-thin-harness-fat-skills.md)
- Generic MCP anti-pattern: 40+ tool definitions eating half the context window, 2-5 second round-trips per operation (ref: sources/garry-tan-thin-harness-fat-skills.md)
- "Software doesn't have to be precious anymore. Build exactly what you need, and nothing else." (ref: sources/garry-tan-thin-harness-fat-skills.md)
- Speed compounds: 75× per tool call × many calls per skill = orders of magnitude difference in total session cost (ref: sources/garry-tan-thin-harness-fat-skills.md)
- Mindset shift: don't wrap existing APIs generically — build narrow tools for specific workflows (ref: sources/garry-tan-thin-harness-fat-skills.md)

## Relevance to STOPA

Justifies keeping MCP servers minimal and building Python scripts (`scripts/`) for STOPA-specific operations. Validates the RTK hook approach (purpose-built token filter) over generic shell wrappers.

## Mentioned In

- [Key Concepts for AI Agentic Skills Design — Thin Harness Fat Skills](../sources/garry-tan-thin-harness-fat-skills.md)
