---
title: "MoM + TARo: Inspirace pro vylepšení STOPA ekosystému"
slug: mom-taro-research
source_type: research_output
date_ingested: 2026-04-07
entities_extracted: 7
claims_extracted: 5
---

# MoM + TARo: Inspirace pro vylepšení STOPA ekosystému

> **TL;DR**: MoM (Mixture-of-Minds, arXiv:2510.20176) ukazuje, že role-specific reward funkce a sequential training (planner > worker) přináší +5-17% kvalitu v multi-agent RL. TARo (arXiv:2603.18411) dokazuje, že adaptivní per-token routing překonává fixní interpolaci o +8.4% na MATH500 a šetří 40-60% budget. Oba principy jsou přímo aplikovatelné na STOPA — role-specific critic scoring a dynamické tier routing místo fixního light/standard/deep výběru při startu tasku.

## Key Claims

1. MoM role-specific rewards (BLEU pro planner, execution success pro coder, exact match pro answerer) přináší +5-17% kvalitu — `[verified]`
2. TARo adaptivní per-token routing překonává fixní interpolaci o +8.4% na MATH500 — `[verified]`
3. TARo weak-to-strong transfer: router trénovaný na 3B/8B funguje na 14B/70B bez retrainingu — `[verified]`
4. MoM best-of-N parallel rollouts: 8x rollouts přidává +3.65% kvalitu — `[verified]`
5. RouteLLM dosahuje 2x cost reduction s preference-based routingem — `[argued]`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| MoM (Mixture-of-Minds) | paper | new |
| TARo (Token-level Adaptive Routing) | paper | new |
| RouteLLM | tool | new |
| GDPO (Decoupled Group Relative Policy Optimization) | paper | new |
| Process Reward Models (PRMs) | concept | new |
| Best-of-N rollouts | concept | new |
| Weak-to-strong transfer (routing) | concept | new |

## Relations

- `MoM` `validates` `Role-specific critic scoring`
- `TARo` `validates` `Weak-to-strong transfer (routing)`
- `RouteLLM` `implements` `Preference-based routing`
- `GDPO` `solves` `Reward collapse in multi-criteria scenarios`
- `Process Reward Models (PRMs)` `enable` `Per-role step-level scoring`
- `Best-of-N rollouts` `combines with` `Process Reward Models (PRMs)`
- `TARo` `is complementary to` `MoM`
