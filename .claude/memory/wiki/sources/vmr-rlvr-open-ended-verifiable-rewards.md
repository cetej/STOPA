---
title: "VMR-RLVR: Verifiable Multiple-Choice Reformulation for RLVR"
slug: vmr-rlvr-open-ended-verifiable-rewards
source_type: url
url: "https://arxiv.org/abs/2511.02463"
date_ingested: 2026-04-13
date_published: "2025-11"
entities_extracted: 2
claims_extracted: 6
---

# VMR-RLVR: Verifiable Multiple-Choice Reformulation for RLVR

> **TL;DR**: Přeformuluje open-ended úlohy (kreativní psaní, subjektivní otázky) na binární pairwise choice, čímž zachovává verifiable reward signal pro RLVR bez potřeby reward modelu. Reasoning modely zlepšení +3.29 bodů; non-reasoning modely minimálně.

## Key Claims

1. RLVR selhává na open-ended úlohy — binární pairwise reformulation to opravuje bez reward modelu — `[argued]`
2. DeepSeek-R1-Distill-Qwen-14B trénovaný VMR-RLVR překonal 32B model průměrně o 3.29 bodů — `[verified]`
3. VMR-RLVR > DPO na stejných datech — učí se hlubšímu porozumění kvality, ne jen napodobování — `[verified]`
4. Non-reasoning modely (Qwen2.5-14B) profitují minimálně — metoda vyžaduje pre-existing reasoning schopnost — `[verified]`
5. Pairwise comparison je dostatečný verifiable signal pro iterativní RL trénink — `[argued]`
6. Binární choice eliminuje reward hacking typický pro auxiliary reward models — `[argued]`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| [VMR-RLVR](../entities/vmr-rlvr.md) | concept | new |
| [DeepSeek-R1](../entities/deepseek-r1.md) | tool | updated |

## Relations

- VMR-RLVR `extends` RLVR — přidává multiple-choice reformulation layer
- VMR-RLVR `competes_with` DPO — stejná data, VMR-RLVR vítězí
- VMR-RLVR `competes_with` RLHF — eliminuje potřebu reward modelu
- DeepSeek-R1 `used_by` VMR-RLVR — testovací model (14B distill varianta)

## Cross-References

- Related learnings: `2026-04-08-direction-magnitude-decoupling-optimization.md` (RLSD — podobná RL optimalizace), `reasoning-with-sampling` (MCMC = RL bez tréninku — komplementární přístup)
- Related wiki sources: [rlsd-self-distilled-rlvr](rlsd-self-distilled-rlvr.md), [reasoning-with-sampling](reasoning-with-sampling.md), [scalerl-scaling-rl-compute-llms](scalerl-scaling-rl-compute-llms.md)
- Contradictions: none detected
