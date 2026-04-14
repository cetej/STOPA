---
date: 2026-04-13
type: best_practice
severity: high
component: orchestration
tags: [evaluation, generalization, loss-landscape, skill-evaluation, optimizer]
summary: "Pretraining loss není dostatečný proxy pro downstream kvalitu — dva modely se stejným loss mohou mít drasticky odlišný downstream výkon (Nexus: +15% GSM8k při identickém loss). Pro STOPA: training-set metriky nestačí, evaluace musí zahrnovat OOD/downstream testy."
source: external_research
uses: 2
harmful_uses: 0
successful_uses: 0
confidence: 0.80
maturity: draft
related: [2026-04-08-early-iteration-unreliable-eval.md]
verify_check: "manual"
skill_scope: [autoloop, self-evolve, eval, critic]
---

# Pretraining Loss Nestačí jako Generalizační Proxy

Nexus (arXiv:2604.09258, Tsinghua + ByteDance) formálně dokazuje, že pretraining loss je nedostatečný proxy pro downstream generalizaci. Dva modely s identickým pretraining loss mohou mít radikálně odlišný downstream výkon (+15% GSM8k) kvůli odlišné geometrii v loss landscape (Sum vs Intersection of Minima).

**STOPA relevance**: Toto přímo platí pro iterativní skills (/autoloop, /self-evolve):
- Convergence na training objektivu (critic score na known evals) ≠ zlepšení na nových úlohách
- Skill s perfektním score na eval setu může být přetrénovaný na ten konkrétní eval set
- Evaluace by měla zahrnovat OOD/held-out případy — ne jen in-distribution metriky

**Analogie pro multi-task orchestraci**: Gradient similarity = alignment mezi subtasky. Pokud subtasky konfliktují (nízká gradient similarity), agregátní "vše hotovo" signál maskuje špatnou downstream kvalitu.

**Potvrzuje**: ScaleRL (early performance unreliable), RLSD (direction/magnitude decoupling).
