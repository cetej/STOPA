---
title: "Vertikální škálování v orchestraci — Research Brief"
slug: vertical-scaling-research
source_type: research_output
date_ingested: 2026-04-07
entities_extracted: 9
claims_extracted: 5
---

# Vertikální škálování v orchestraci — Research Brief

> **TL;DR**: Current orchestration systems (including STOPA) operate horizontally — distinguishing agent roles but not abstraction levels. Research shows 3 agents outperform 5-agent designs, phase separation (discovery→improvement) is critical, and hierarchical RAG is cost-optimal over flat retrieval. Skill verbosity has 60%+ non-actionable content; compression produces better-quality outputs at 75% token reduction.

## Key Claims

1. HexMachina: 3-agent design (Orchestrator/Analyst/Coder) beats 5-agent design with 54.1% vs 16.4% win rate — "dilution from additional roles." — `[verified]`
2. SkillReducer: 75% token reduction, resulting quality IMPROVES (0.742 vs 0.722, p=0.002) — less-is-more effect. — `[verified]`
3. Multi-agent hierarchy multiplies token cost 26-77× (single-agent $0.41/day vs multi-agent $10.54/day). — `[verified]`
4. HCAG: hierarchical code abstraction (project→module→function) is cost-optimal vs flat RAG — theoretical proof. — `[verified]`
5. Pure LLM hierarchical plan validity is only 1% (HTN+LLM) — structural enforcement via hooks/contracts is necessary. — `[verified]`

## Relations

- HexMachina `validates` 3-agent optimal design
- SkillReducer `applies to` STOPA skill compression
- HCAG `maps to` orchestrate→scout→worker chain
- Context Rot (Chroma) `affects` all 18 tested models
- GoalAct `requires` continuously updated global plan in state.md

## Entities

| Entity | Type | Status |
|--------|------|--------|
| HexMachina | paper | new |
| SkillReducer | paper | new |
| HCAG | paper | new |
| HMAS Taxonomy | paper | new |
| GoalAct | paper | new |
| Context Rot | concept | new |
| xMemory | tool | new |
| HTN+LLM | concept | new |
| Capgemini Multi-Agent Analysis | concept | new |
