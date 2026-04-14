---
name: Nexus Optimizer
type: concept
first_seen: 2026-04-13
last_updated: 2026-04-13
sources: [nexus-common-minima-generalization]
tags: [optimizer, pretraining, generalization, gradient-similarity]
---

# Nexus Optimizer

> Gradient approximator pro LLM pretraining, který maximalizuje cosine similarity gradientů mezi data sources. Inner-outer loop architektura: inner model dělá sequential normalized SGD, displacement slouží jako pseudo-gradient pro outer optimizer (AdamW/Muon).

## Key Facts

- Core princip: "Sum of Minima" (AdamW default) → "Intersection of Minima" (Nexus) — task-specific minima geometricky blízko sebe (ref: sources/nexus-common-minima-generalization.md)
- Theorem 3.1: CosSim(nabla L_i, nabla L_j) upper bounds closeness — maximalizace similarity = minimalizace vzdálenosti minim (ref: sources/nexus-common-minima-generalization.md)
- Implementace: inner_model clone, NSGD inner steps, pseudo_grad = inner_model - model, outer optimizer step (ref: sources/nexus-common-minima-generalization.md)
- 3B model: +15% GSM8k, +8% MATH500, +4% HumanEval, pretrain loss identický s AdamW (ref: sources/nexus-common-minima-generalization.md)
- Ortogonální k Muon: Muon zlepšuje loss (vertikální), Nexus zlepšuje geometrii (horizontální v loss landscape) — kombinovatelné (ref: sources/nexus-common-minima-generalization.md)
- Overhead: téměř nulový — same forward/backward count, jen model copy (CPU offloadable) (ref: sources/nexus-common-minima-generalization.md)
- Retence: na GSM8k/HumanEval >95% správných odpovědí z AdamW zachováno + nové exkluzivní — additive, ne destruktivní (ref: sources/nexus-common-minima-generalization.md)
- Autoři: Tsinghua University + ByteDance Seed (Huanran Chen, Xiao Li, Yinpeng Dong, Jun Zhu)

## Relevance to STOPA

Nexus ukazuje, že pretraining loss není dostatečný proxy pro kvalitu modelu — pro STOPA evaluace to znamená, že metriky jako "loss klesá" nejsou důkazem zlepšení. Analogie pro iterativní skills: convergence na training objective ≠ generalizace na reálný use case. Critic by měl hodnotit downstream chování, ne training progress.

## Mentioned In

- [Nexus: Common Minima Generalization](../sources/nexus-common-minima-generalization.md)
