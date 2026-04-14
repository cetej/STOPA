---
title: "Nexus: Same Pretraining Loss, Better Downstream Generalization via Common Minima"
slug: nexus-common-minima-generalization
source_type: url
url: "https://arxiv.org/abs/2604.09258"
date_ingested: 2026-04-13
date_published: "2026-04-13"
entities_extracted: 3
claims_extracted: 6
---

# Nexus: Same Pretraining Loss, Better Downstream Generalization via Common Minima

> **TL;DR**: Nexus optimizer maximalizuje gradient similarity mezi pretraining tasks, čímž konverguje k "Intersection of Minima" místo "Sum of Minima". Při identickém pretraining lossu dosahuje +15% GSM8k, +8% MATH, +4% HumanEval na 3B modelu. Ortogonální ke zlepšením z nižšího lossu (Muon). Overhead téměř nulový.

## Key Claims

1. Pretraining loss sám o sobě nedostačuje pro predikci downstream generalizace — dva modely se stejným loss mohou mít drasticky odlišný downstream výkon — `[verified]`
2. Closeness (geometrická vzdálenost task-specific minim od konvergovaného bodu) je second-order property přímo korelující s generalizací (Theorem 2.2) — `[verified]`
3. Gradient cosine similarity je upper bound na closeness → maximalizace CosSim ≈ minimalizace vzdálenosti minim — `[verified]`
4. 3B model: +15% GSM8k, +8% MATH500, +4% HumanEval, OOD loss -0.012 při stejném pretraining loss — `[verified]`
5. Nexus je ortogonální k Muon — Muon zlepšuje loss, Nexus zlepšuje geometrii; kombinovatelné — `[argued]`
6. Overhead téměř nulový — stejný počet forward/backward passes, jen kopie modelu pro inner loop — `[verified]`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| [Nexus optimizer](../entities/nexus-optimizer.md) | concept | new |
| [Common minima](../entities/common-minima.md) | concept | new |
| [Gradient similarity](../entities/gradient-similarity.md) | concept | new |

## Relations

- Nexus optimizer `extends` AdamW — adds inner-loop gradient similarity maximization
- Nexus optimizer `uses` common minima — theoretical basis
- Nexus optimizer `competes_with` Muon — orthogonal mechanisms (geometry vs loss)
- Gradient similarity `part_of` Nexus optimizer — core objective

## Cross-References

- Related learnings: `2026-04-08-direction-magnitude-decoupling-optimization.md` (RLSD direction/magnitude — related optimizer geometry), `2026-04-08-early-iteration-unreliable-eval.md` (ScaleRL: pretraining loss ≠ final quality — Nexus provides theoretical explanation)
- Related wiki sources: [scalerl-scaling-rl-compute-llms](scalerl-scaling-rl-compute-llms.md), [rlsd-self-distilled-rlvr](rlsd-self-distilled-rlvr.md), [learning-is-forgetting-llm-lossy-compression](learning-is-forgetting-llm-lossy-compression.md)
- Contradictions: none
