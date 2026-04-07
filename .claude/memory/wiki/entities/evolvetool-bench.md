---
name: EvolveTool-Bench
type: paper
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [toolgenesis-research]
tags: [testing, tool-creation, benchmarks]
---

# EvolveTool-Bench

> arXiv:2604.00392 (duben 2026) — komplementární benchmark k Tool-Genesis; hodnotí tool libraries jako software artefakty (reuse, redundancy, regression, safety), ne jednotlivé nástroje.

## Key Facts

- Systémy s podobnou task completion (63–68%) se mohou lišit o 18% v library health (ref: sources/toolgenesis-research.md)
- Zaměřuje se na library-level metriky: redundance, regrese, bezpečnost
- Nezávisle validuje: "outcome-only evaluation je nedostatečná" — stejný závěr jako Tool-Genesis
- Komplementární k Tool-Genesis: task-level vs. library-level perspektiva

## Relevance to STOPA

Varování pro STOPA skills maintenance: outcome (SR) ≠ library health. Navrhuje pravidelný audit skills library (redundance, zastaralost) — relevantní pro /sweep skill.

## Mentioned In

- [Tool-Genesis Research Brief](../sources/toolgenesis-research.md)
