---
date: 2026-04-15
type: best_practice
severity: high
component: skill
tags: [autoloop, autoresearch, self-evolve, optimization, scaling-laws, iteration-strategy, test-time-compute, stopping-criterion]
summary: "Parcae (arXiv:2604.12946): iterativní optimalizace sleduje saturující exponenciální decay L(T)=L∞+Z·exp(-z·T), ne lineární zlepšení. Tréninková hloubka (počet iterací při vývoji) = strop runtime scalingu. Farm tier: per-item variable depth místo uniformní. Tři ortogonální osy: iterace × data × model size."
source: external_research
maturity: draft
uses: 3
successful_uses: 0
harmful_uses: 0
confidence: 1.0
skill_scope: [autoloop, autoresearch, self-evolve]
related: [2026-04-08-early-iteration-performance-unreliable.md, 2026-04-11-iteration-paradox-meta-pattern.md, 2026-04-15-best-of-n-parallel-candidates.md]
verify_check: "manual"
---

## Detail

Parcae (Prairie et al., UCSD + Together AI, arXiv:2604.12946) — stabilní looped transformer se scaling laws pro iterativní compute. Tři transferable principy:

### 1. Exponenciální decay model pro iterativní optimalizaci

Test-time compute v looped modelech sleduje:
```
L(T) = L∞ + Z · exp(-z · T)
```
kde L∞ = ireducibilní floor, Z = initial gap, z = decay rate, T = počet iterací.

**Proč lepší než sigmoidální (ScaleRL):** Méně parametrů (3 vs 4), explicitní floor (L∞), snadno fittovatelné po 3-4 bodech. Parcae dosahuje 0.85-1.3% prediction error.

**STOPA dopad:** Autoloop/autoresearch mohou po 4+ iteracích fitovat exponenciální decay na score trajectory. Pokud predikovaný L∞ je pod target, STOP early — zbývající iterace přidají < Z·exp(-z·T_current) zlepšení. Aktuálně plateau detection funguje na "3 iterace bez zlepšení" — exponenciální model predikuje ceiling DŘÍVE.

### 2. Tréninková hloubka = inference ceiling (µ_rec princip)

Parcae ukazuje, že test-time gains plateau kolem µ_rec (průměrná tréninková hloubka). Více iterací při inference nepomůže přes strop daný tréninkem.

**STOPA dopad:** Pokud skill byl self-evolved s max 5 iteracemi, nasazení s 15 iteracemi nepřinese úměrné zlepšení. Self-evolve by měl explicitně trackovat "kolik iterací použil" a toto číslo propagovat jako recommended_max_iterations do optstate.

### 3. Per-item variable depth (farm tier)

Parcae vzorkuje různou hloubku per-sekvenci místo uniform per-batch. Nižší variance, lepší stabilita.

**STOPA dopad:** Farm tier (20+ souborů, linter fixy, migrace) aktuálně aplikuje stejný effort na všechny items. Variabilní effort per-item (jednoduchý fix = 1 iterace, komplexní = 3) by byl efektivnější. Orchestrátor by klasifikoval item complexity PŘED distribucí do workerů.

### Bonus: Ortogonální škálovací osy

Parcae ukazuje tři nezávislé osy: iterace (looping) × data (tokeny) × parametry. Pro STOPA budget planning: model size (haiku/sonnet/opus) × context size × počet iterací jsou nezávislé osy — optimální mix záleží na task typu, ne na jedné "víc je líp" dimenzi.
