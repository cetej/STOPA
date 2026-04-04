---
name: liveprompt
variant: compact
description: Condensed liveprompt for repeat invocations within session. Use full SKILL.md for first invocation.
---

# LivePrompt — Compact (Session Re-invocation)

Research what the community uses RIGHT NOW for a topic, synthesize deployment-ready prompt.

## Pipeline

```
Phase 1: Multi-source search (Reddit, X, Discord, GitHub)
         shallow=5, standard=10, deep=15 queries
Phase 2: Deep dive top 5-8 results (WebFetch)
         Weight: recency 3x, engagement 2x, specificity 2x, evidence 2x
Phase 3: Pattern analysis → 5 categories:
         Consensus | Breakthrough | Anti-patterns | Platform nuances | Recency signals
Phase 4: Synthesize deployment-ready prompt
         No placeholders, cite sources, include anti-pattern guards
Phase 5: Output (both/prompt-only/report-only)
```

## Search Strategy

Target community discussion, not official docs:
- `site:reddit.com "{topic}" prompt OR technique {year} {month}`
- `"{topic}" "what works" OR "game changer" {year}`
- `"{topic}" "stopped working" OR "anti-pattern" {year}`
- Platform-specific boosters (ChatGPT, Claude, Midjourney, Cursor, etc.)

## Prompt Quality Checks

- [ ] Every instruction traces to community source
- [ ] No generic filler ("be helpful")
- [ ] Anti-patterns addressed
- [ ] Clear structure: role → context → task → constraints → output
- [ ] Specific enough for consistent results

## Critical Rules

- Recency > authority — 3-day Reddit post with evidence beats 6-month blog
- Evidence > claims — before/after proof required
- Every technique needs a real source — no "commonly known"
- Honest about gaps — "no data" is valid
- Never fill gaps with training data — this is about NOW
- Max 12 page fetches (diminishing returns)

## Curated Library

Check topic keywords against pre-validated prompts before searching.
Current: Systems Thinking Strategist (Donella Meadows).
