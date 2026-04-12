---
date: 2026-04-10
type: architecture
severity: high
component: orchestration
tags: [evolution, optimization, population, scoring, mutation]
summary: "EGGROLL (Oxford/MILA 2026) dokazuje 3 principy pro evoluci skills: (1) rank-1 perturbace staci pokud je populace dostatecna, (2) populacni z-score normalizace stabilizuje selekci, (3) tri rezimy sigma (linearizace/kriticka/divergence) urcuji optimalnost mutaci."
source: external_research
uses: 1
successful_uses: 0
harmful_uses: 0
confidence: 0.8
skill_scope: [prompt-evolve, self-evolve, autoloop]
verify_check: "Grep('EGGROLL', path='.claude/skills/prompt-evolve/SKILL.md') → 1+ matches"
---

## EGGROLL principy pro STOPA evoluci

Paper: "Evolution Strategies at the Hyperscale" (Sarkar, Fellows et al., Oxford FLAIR/WhiRL + MILA, 2026)
URL: https://eshyperscale.github.io/

### 3 adoptovane principy

**1. Low-rank perturbace (rank-1 staci)**
Theorem 3: i rank-1 perturbace konverguji k true ES gradientu rychlosti O(r^-1). 
Preklady do prompt/skill evoluce: kazdy variant mutuje jednu osu (detail/delka/styl/struktura). Celkovy update pres populaci je full-rank.
Implementovano v: prompt-evolve Phase 2 (Low-Rank Mutation Principle), autoloop Population Mode.

**2. GRPO-style populacni scoring**
z_i = (s_i - mu) / max(sigma_global, 0.01) normalizuje fitness skore pres celou populaci.
Stabilnejsi selekce nez raw score porovnani, zejmena kdyz eval rubrics se lisi mezi kategoriemi.
Implementovano v: prompt-evolve Phase 4 (Population-Normalized Scoring).

**3. Tri rezimy sigma (mutation strength)**
- Linearizace (sigma prilis male): konverguje ale neexploruje
- Kriticka zona (sigma spravne): optimalni signal-to-noise
- Divergence (sigma prilis velke): updaty diverguji
Preklad: rozsah editace musi odpovidat fazi evoluce (male opravy na zacatku, vetsi explorace na konci).
Implementovano v: self-evolve Adaptive Mutation Strength.

### Dalsi relevantni poznatky z paperu

- RWKV-7 jako efektivni inference model (konstantni state size = vic populace do GPU)
- Integer-only trenovani (EGG model) — gradient-free optimalizace umoznuje int8 pretraining
- Deterministicky RNG — perturbace se rekonstruuji on-demand, nemuseji se drzet v pameti (analogie: ukladat seed mutace misto celeho kandidata)
