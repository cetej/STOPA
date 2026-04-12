---
date: 2026-04-11
type: architecture
severity: medium
component: general
tags: [inference, efficiency, architecture, watch-item]
summary: "CALM (arXiv:2510.27688) komprimuje K tokenů do 1 spojitého vektoru — K=4 je sweet spot (44% méně FLOPs, >99.9% rekonstrukce). Přenositelné principy: batch K segmentů v pipeline, likelihood-free eval (BrierLM), 4:1 komprese memory."
source: external_research
confidence: 0.6
uses: 0
successful_uses: 0
harmful_uses: 0
verify_check: manual
---

## CALM — Continuous Autoregressive Language Models

**Paper:** arXiv:2510.27688 (Shao, Li, Meng, Zhou)

**Technika:** Autoenkodér komprimuje K tokenů → 1 latentní vektor (dim=32K). Generativní hlava (Energy Transformer, single-step) predikuje vektory místo tokenů. K=4 překonává diskrétní baseline na compute frontier.

**Klíčová čísla:**
- K=4: 44% méně training FLOPs, 34% méně inference FLOPs
- Rekonstrukce: >99.9% i s noise σ≈0.3
- BrierLM (likelihood-free eval): korelace -0.966 s cross-entropy
- K=1 horší než baseline, K=8 capacity-limited

**Přenositelné principy pro STOPA:**
1. **Pipeline batching (NG-ROBOT):** K=4 segmentů do jednoho API callu — validováno jako sweet spot
2. **Likelihood-free eval:** BrierLM vzor pro /eval bez logprobs
3. **Memory komprese:** 4:1 komprese zachovává informaci — validuje /compile přístup
4. **Watch item:** až provideři adoptují CALM-style inference, automatický speedup bez změn

**Limitace:** Context-free autoenkodér (bez kondicionování na předchozí vektory). K=8+ potřebuje větší modely. Diskrétní vstupy nutné (kontinuální degradují).
