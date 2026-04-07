---
title: "Single-Agent LLMs Outperform Multi-Agent Systems on Multi-Hop Reasoning Under Equal Thinking Token Budgets"
slug: single-agent-vs-multi-agent-thinking-budget
source_type: url
url: "https://arxiv.org/abs/2604.02460"
date_ingested: 2026-04-07
date_published: "2026-04-02"
entities_extracted: 3
claims_extracted: 5
---

# Single-Agent LLMs vs Multi-Agent Systems Under Equal Thinking Token Budgets

> **TL;DR**: Při kontrolovaném compute budgetu (thinking tokeny) single-agent systémy konzistentně dosahují stejného nebo lepšího výkonu než multi-agent systémy na multi-hop reasoning. Výhody MAS v literatuře jsou artefakt nekontrolovaného compute, ne architektonická superiorita.

## Key Claims

1. SAS ≥ MAS na multi-hop reasoning při rovném thinking token budgetu — ověřeno na 3 modelech a 5 MAS architekturách — `verified`
2. Data Processing Inequality formálně dokazuje, že každý agent-handoff ztrácí informaci — `argued`
3. MAS získává výhodu pouze při těžkém poškození kontextu (α ≥ 0.7) — `verified`
4. Standardní benchmarky MAS jsou artefakt nekontrolovaného compute, ne architektonické superiority — `argued`
5. Thinking token plateau nastává kolem 1 000–2 000 tokenů, výnosy klesají — `verified`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| [Data Processing Inequality](../entities/data-processing-inequality.md) | concept | new |
| [Thinking Token Budget](../entities/thinking-token-budget.md) | concept | new |
| [arXiv:2604.02460](../entities/arxiv-2604-02460.md) | paper | new |
| DeepSeek-R1 | tool | existing (mentioned as test model) |

## Relations

- arXiv:2604.02460 `uses` Data Processing Inequality — theoretical grounding
- arXiv:2604.02460 `contradicts` BIGMAS (directed-graph multi-agent) — challenges MAS superiority claims
- arXiv:2604.02460 `uses` Thinking Token Budget — experimental methodology

## Cross-References

- Related learnings: `2026-03-29-bigmas-directed-graph-orchestration.md` (contradicted by claim 1), `2026-04-02-distributed-systems-amdahl-gate.md` (complementary — Amdahl gate also limits MAS scaling)
- Related wiki articles: `orchestration-multi-agent.md` (directly relevant to main theme)
- Contradictions: WARNING: contradicts implicit assumption in bigmas learning that more agents = better reasoning — paper shows this holds only under equal compute
