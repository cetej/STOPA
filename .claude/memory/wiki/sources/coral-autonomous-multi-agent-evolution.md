---
title: "CORAL: Towards Autonomous Multi-Agent Evolution for Open-Ended Discovery"
slug: coral-autonomous-multi-agent-evolution
source_type: url
url: "https://arxiv.org/abs/2604.01658"
url_github: "https://github.com/Human-Agent-Society/CORAL"
date_ingested: 2026-04-08
date_published: "2026-04-02"
entities_extracted: 4
claims_extracted: 7
---

# CORAL: Towards Autonomous Multi-Agent Evolution for Open-Ended Discovery

> **TL;DR**: CORAL je lightweight framework pro autonomní multi-agent evoluci — každý agent běží v isolovaném git worktree branchi, sdílí knowledge přes `.coral/public/` symlink, a orchestrátor může průběžně zasílat heartbeat prompty. Výsledek: 3-10× vyšší improvement rate vs evolutionary baselines na 10 diversních task typech.

## Key Claims

1. Git worktree per agent eliminuje konflikty bez komunikačního overheadu — izolace je filesystem-level — `[argued]`
2. Sdílení přes `.coral/public/` symlink (ne message passing) = zero sync overhead — `[argued]`
3. 3-10× vyšší improvement rate vs evolutionary baselines na 10 task typech (math, algorithmic, systems) — `[verified]`
4. Kernel engineering: 1363 → 1103 cyklů se 4 co-evolving agenty — `[verified]`
5. Heartbeat-triggered prompts umožňují mid-run steering bez restartu agenta — `[argued]`
6. Warm-start (literature review před implementací) snižuje cold-start penalty — `[argued]`
7. Knowledge reuse, ne jen multi-agent parallelismus, je primární driver gainů — `[argued]`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| [CORAL](../entities/coral.md) | tool | new |
| [Shared Public State Pattern](../entities/shared-public-state-pattern.md) | concept | new |
| [Heartbeat-Triggered Intervention](../entities/heartbeat-triggered-intervention.md) | concept | new |
| [Open-Ended Discovery](../entities/open-ended-discovery.md) | concept | new |

## Relations

- CORAL `extends` GEA — oba dělají group evolution, CORAL přidává open-ended discovery + izolaci
- CORAL `uses` git worktree isolation — filesystem-level agent isolation pattern (CAID arXiv:2602.19260)
- Shared Public State Pattern `part_of` CORAL — core coordination mechanismus
- Heartbeat-Triggered Intervention `part_of` CORAL — orchestrator steering pattern
- CORAL `inspired_by` Voyager — lifelong skill accumulation, continuous exploration
- Open-Ended Discovery `contrasts` autoresearch — autoresearch má fixed eval target, CORAL nemá

## Cross-References

- Related learnings: `2026-04-03-autoagent-parallel-candidates.md`, `2026-04-03-autoagent-overfitting-guard.md`, `2026-03-29-claudini-autoresearch-loop.md`
- Related wiki articles: [orchestration-multi-agent](../orchestration-multi-agent.md), [skill-evaluation](../skill-evaluation.md)
- Related entities: gea-group-evolving-agents.md, acceptance-gated-self-evolution.md, vertical-scaling-orchestration.md
- Contradictions: none detected
