---
title: "Group-Evolving Agents: Open-Ended Self-Improvement via Experience Sharing"
slug: group-evolving-agents-gea
source_type: url
url: "https://arxiv.org/abs/2602.04837"
date_ingested: 2026-04-08
date_published: "2026-02-04"
entities_extracted: 3
claims_extracted: 6
---

# Group-Evolving Agents: Open-Ended Self-Improvement via Experience Sharing

> **TL;DR**: GEA překonává izolovanou self-evolution tím, že skupina agentů sdílí evoluční trajektorie — každý patch, log i selhání. Dosahuje 71.0% na SWE-bench Verified (+14pp vs baseline) a 1.4 bug-fix iterací vs 5. Evoluované patche jsou přenositelné mezi GPT a Claude rodinami.

## Key Claims

1. Skupina agentů jako evoluční jednotka překonává izolované větvení — zabraňuje ztrátě beneficiálních objevů — `[verified]`
2. GEA: 71.0% SWE-bench Verified vs 56.7% (self-evolving baseline), 88.3% vs 68.3% (Polyglot) — `[verified]`
3. GEA matched human-designed frameworks (71.8% / 52.0%) bez human guidance — `[verified]`
4. Integruje tools ze 17 vs 9 ancestor agentů (~2× diversity) — `[verified]`
5. Bug repair: 1.4 iterací vs 5 pro nezávislou evoluci — `[verified]`
6. Evoluované patche cílí na workflows/tools (ne model prompty) → přenositelnost přes GPT + Claude — `[argued]`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| [GEA (Group-Evolving Agents)](../entities/gea-group-evolving-agents.md) | paper | new |
| [Performance-Novelty Selection](../entities/performance-novelty-selection.md) | concept | new |
| [Group Experience Sharing](../entities/group-experience-sharing.md) | concept | new |

## Relations

- GEA `extends` Reflexion — přidává group-level sdílení k reflexivní self-improvement smyčce
- GEA `extends` Voyager — lifelong skill accumulation na group level místo single-agent
- Performance-Novelty Selection `inspired_by` UCB1 — exploration/exploitation trade-off
- Group Experience Sharing `part_of` GEA — core mechanismus

## Cross-References

- Related learnings: `2026-04-06-osft-self-sharpening.md`, `2026-04-03-autoagent-parallel-candidates.md`
- Related wiki articles: [orchestration-multi-agent](../orchestration-multi-agent.md) (multi-agent coordination), [skill-design](../skill-design.md) (skill evolution)
- Related entities: acceptance-gated-self-evolution.md, voyager.md, reflexion.md
- Contradictions: none detected
