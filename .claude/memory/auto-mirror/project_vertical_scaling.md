---
name: project_vertical_scaling
description: Vertical scaling (micro/mezo/macro) — 3-phase rollout for multi-level abstraction awareness in STOPA orchestration
type: project
originSessionId: a5b7e65e-c38d-4b15-8b7e-167054790bf5
---
Vertikální škálování orchestrace — systematická traversace mezi úrovněmi abstrakce (mikro/mezo/makro).

**Fáze A** (2026-04-07, DONE): Hierarchický scout output — 3-level format (Level 1 MAKRO, Level 2 MEZO, Level 3 MIKRO + Cross-Level Assessment). Implementováno v scout.md.

**Fáze B** (IN PROGRESS, started 2026-04-21): /telescope skill implementována. Integrována do orchestrate jako opt-in flag `--telescope`. Design: 3 paralelní agenti (M1 Mikro/Haiku, M2 Mezo/Sonnet, M3 Makro/Sonnet) → Cross-Level Synthesis → Vertical Consistency Report + log do telescope-log.md. Correlated FP guard při unanimous consensus. Go/No-Go kritéria: N≥10 runs, ≥1 cross-level catch per 8 tasks, FP rate <10%.

**Fáze C** (scheduled 2026-05-18): Čeká na Phase B Go/No-Go evaluaci. Auto-trigger na deep tier pokud kritéria splněna.

**Why:** Flat RAG selhává na komplexních kódových bázích (HCAG arXiv:2603.20299). 3-agent core je optimum (HexMachina arXiv:2506.04651v2). Multi-agent hierarchie 26× dražší, ale komprese 48-75% úspora.

**How to apply:** Při orchestraci > standard tier: scout MUSÍ produkovat 3-level output. Cross-Level Assessment sekce je kde se surfacují vertikální konflikty. Pro telescope validation: `/orchestrate --telescope <task>`.

**Research:** outputs/vertical-scaling-research.md (full brief), outputs/vertical-scaling-explained.md (příklad), outputs/vertical-scaling-report.md (zpráva + Mermaid)
