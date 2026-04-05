# Gradient Descent Optimization Algorithms — Research Brief

**Date:** 2026-04-04
**Paper:** Sebastian Ruder — "An overview of gradient descent optimization algorithms" (arXiv:1609.04747)
**Scope:** standard (obsah paperu + dopad + post-2017 vývoj)
**Sources consulted:** 37

## Executive Summary

Ruderův přehled (2016, revidován 2017) je nejcitovanější survey optimalizačních algoritmů pro deep learning s ~6 700 citacemi na Semantic Scholar [VERIFIED][2]. Paper systematicky pokrývá 9 optimalizačních algoritmů (od Momentu po AMSGrad), 5 distribuovaných architektur a 4 doplňkové strategie, přičemž doporučuje Adam jako nejlepší celkovou volbu [VERIFIED][1].

Od poslední revize paperu (červen 2017) bylo publikováno 20+ významných optimizérů, které paper nepokrývá [VERIFIED][3-22]. Nejvýznamnější mezera je absence **AdamW** (decoupled weight decay) [VERIFIED][3] — de facto standard pro trénování transformerů. Další zásadní chybějící oblasti: learning-rate-free metody (Schedule-Free, D-Adaptation), sharpness-aware trénování (SAM), second-order metody (Sophia, SOAP) a sign-based optimizéry (Lion).

Paper zůstává cenný jako pedagogická reference pro pochopení evoluce od vanilla SGD k adaptivním metodám, ale pro aktuální praxi (2024-2026) je nutné ho doplnit o novější vývoj — zejména AdamW, Schedule-Free a SOAP.

## Detailed Findings

### 1. Obsah a struktura paperu

Paper je strukturován v 5 hlavních částech [VERIFIED][1]:

**Taxonomie GD variant:**
- Batch GD, Stochastic GD, Mini-batch GD (identifikován jako de facto standard)

**4 výzvy motivující adaptivní metody:**
- Volba learning rate, learning rate schedules, sparse/heterogenní features, sedlové body (nikoliv lokální minima — hlavní překážka v nekonvexní optimalizaci, cituje Dauphin et al. 2014) [VERIFIED][1]

**9 optimalizačních algoritmů** s matematickými derivacemi [VERIFIED][1]:

| Algoritmus | Rok | Klíčová inovace |
|-----------|-----|-----------------|
| Momentum | — | Akumulace předchozích gradientů, γ=0.9 |
| NAG | — | Gradient na odhadované budoucí pozici (lookahead) |
| Adagrad | 2011 | Per-parameter adaptivní LR; slabina: LR klesá k nule |
| Adadelta | 2012 | Exponenciální průměr místo akumulace; nepotřebuje LR |
| RMSprop | 2012 | Nezávisle na Adadeltě; identický první update |
| Adam | 2015 | RMSprop + momentum + bias correction; **doporučen jako nejlepší** |
| AdaMax | 2015 | Adam s ℓ∞ normou |
| Nadam | — | Adam + NAG lookahead |
| AMSGrad | 2018 | Running maximum místo EMA pro druhý moment |

**Hierarchie adaptivních metod** [VERIFIED][1]:
```
Adagrad → Adadelta / RMSprop → Adam → AdaMax / Nadam / AMSGrad
```

**Distribuované architektury:** Hogwild!, Downpour SGD, Delay-tolerant, TensorFlow, EASGD [VERIFIED][1]

**Doplňkové strategie:** Shuffling/Curriculum Learning, Batch Normalization, Early Stopping, Gradient Noise [VERIFIED][1]

### 2. Citační dopad a recepce

**Citace:** ~6 713 na Semantic Scholar, ~729 vysoce vlivných citací [INFERRED][2]. Ruderova nejcitovanější práce (celkem ~56K citací přes všechny publikace).

**Akademická recepce** [VERIFIED][2]:
- Citován v nových surveys i v 2025 (arXiv:2511.20725)
- Zařazen jako "key paper" v DL kurzech (zhanglabtools 2024, HKUST)
- **Není** na čtecím seznamu MIT OCW 6.7960 ani Stanford CS231n — funguje jako practitioner supplement, ne primární text flagship kurzů

**Praktická recepce** [VERIFIED][2]:
- Přeložen komunitou do japonštiny, čínštiny a korejštiny
- Diskutován na Hacker News
- Republikován OpenDataScience (ODSC)
- 2+ nezávislé GitHub implementace
- Duální existence blog + arXiv = dosah na praktiky i akademiky

**Publikační historie** [VERIFIED][1,2]:
- Leden 2016: blog post na ruder.io
- Září 2016: arXiv submission
- Červen 2017: revize (přidán AdaMax, Nadam)
- 2018, 2020: blog aktualizace (AMSGrad, AdamW zmínka)

### 3. Post-2017 vývoj — co paper nepokrývá

Od poslední revize paperu bylo publikováno 20+ významných optimizérů [VERIFIED][3-22]:

#### 2017-2018: Korekce a základ

| Optimizer | Paper | Inovace |
|-----------|-------|---------|
| **AdamW** | arXiv:1711.05101 | L2 ≠ weight decay pro adaptivní metody; decoupled WD. De facto standard pro transformery [INFERRED][3] |
| AdaFactor | arXiv:1804.04235 | Sublineární paměť faktorizací 2. momentu; default pro T5 [VERIFIED][5] |
| Shampoo | arXiv:1802.09568 | Kronecker-faktorizovaný preconditioner [VERIFIED][6] |
| LARS | arXiv:1708.03888 | Layer-wise adaptive rate scaling pro velké batche [VERIFIED][7] |

#### 2019: Large-batch a stabilita

| Optimizer | Paper | Inovace |
|-----------|-------|---------|
| RAdam | arXiv:1908.03265 | Analytická oprava variance → eliminuje warmup heuristiku [VERIFIED][8] |
| LAMB | arXiv:1904.00962 | LARS pro Adam; BERT za 76 minut [VERIFIED][9] |
| Lookahead | arXiv:1907.08610 | Meta-wrapper: fast + slow weights [VERIFIED][10] |

#### 2020: Generalizace a geometrie

| Optimizer | Paper | Inovace |
|-----------|-------|---------|
| AdaBelief | arXiv:2010.07468 | Step size podle "překvapení" gradientu [VERIFIED][12] |
| SAM | arXiv:2010.01412 | Sharpness-aware: min-max hledání plochých minim [VERIFIED][13] |
| Gradient Centralization | arXiv:2004.01461 | Zero-mean gradienty; one-liner pro jakýkoliv optimizer [VERIFIED][11] |

#### 2022-2023: LLM éra

| Optimizer | Paper | Inovace |
|-----------|-------|---------|
| Adan | arXiv:2208.06677 | Správná integrace Nesterova do adaptivních metod [VERIFIED][14] |
| Lion | arXiv:2302.06675 | Sign-only update; 2x paměťově efektivnější než Adam [VERIFIED][15] |
| Sophia | arXiv:2305.14342 | Diagonální Hessian pro LLM; 2x rychlejší než Adam [VERIFIED][16] |
| D-Adaptation | arXiv:2301.07733 | LR-free learning; ICML 2023 Outstanding Paper [VERIFIED][17] |
| Prodigy | arXiv:2306.06101 | Vylepšení D-Adaptation; standard pro LoRA fine-tuning [VERIFIED][18] |

#### 2024: Strukturální metody

| Optimizer | Paper | Inovace |
|-----------|-------|---------|
| SOAP | arXiv:2409.11321 | Adam v eigenbázi Shampoo preconditioneru; 40% méně iterací [VERIFIED][19] |
| AdEMAMix | arXiv:2409.03137 | Dvě EMA (fast + slow); paměť přes 10K+ kroků [VERIFIED][20] |
| Schedule-Free | arXiv:2405.15682 | Žádný LR schedule; vyhrál MLCommons AlgoPerf 2024 [VERIFIED][21] |
| Muon | blog post | SGD-Nesterov + Newton-Schulz ortogonalizace [SINGLE-SOURCE][22] |

### 4. Hlavní chybějící paradigmata

Paper nepokrývá tyto celé kategorie, které se staly zásadními po 2017 [INFERRED][3-22]:

1. **Weight decay decoupling** — AdamW je dnes *default*, paper to vůbec nezmiňuje (blog update 2020 přidal stručnou zmínku)
2. **Learning-rate-free metody** — D-Adaptation, Prodigy, Schedule-Free eliminují LR jako hyperparametr
3. **Sharpness-aware training** — SAM formalizoval spojení ploché loss landscape ↔ generalizace
4. **Second-order metody pro DL** — Sophia, SOAP, Shampoo umožňují praktické second-order trénování
5. **Evolved/discovered optimizers** — Lion nalezen programovou evolucí, ne lidským designem
6. **Large-batch scaling** — LARS, LAMB umožňují batch 32K+ bez ztráty přesnosti
7. **Mixed precision training** — interakce s optimizéry (gradient scaling) zcela chybí

## Disagreements & Open Questions

- **Adam vs SGD generalizace:** Ruder doporučuje Adam, ale Wilson et al. (2017) ukázali, že SGD generalizuje lépe. Tato debata pokračuje — SAM a Schedule-Free se snaží spojit rychlost Adamu s generalizací SGD [INFERRED][13,21]
- **AMSGrad praktická hodnota:** Paper (blog update 2018) ho prezentuje jako opravu Adamu, ale praktické výsledky jsou smíšené [SINGLE-SOURCE][4]
- **Distribuovaná sekce zastaralá:** Hogwild! a Downpour SGD jsou historicky zajímavé, ale moderní distribuce používá gradient all-reduce (Horovod, PyTorch DDP) [INFERRED]
- **Přesný citation count:** Semantic Scholar ~6 713, ale API rate-limited — Google Scholar typicky ukazuje vyšší čísla [UNVERIFIED]

## Evidence Table

| # | Source | URL | Key Claim | Type | Confidence |
|---|--------|-----|-----------|------|------------|
| 1 | Ruder blog (full text) | https://ruder.io/optimizing-gradient-descent/ | 9 algoritmů, Adam doporučen, taxonomie | primary | high |
| 2 | Semantic Scholar | https://www.semanticscholar.org/paper/769ef3d5021cd71c37d2c403f231a53d1accf786 | ~6,713 citací | primary | medium |
| 3 | Loshchilov & Hutter | https://arxiv.org/abs/1711.05101 | AdamW — decoupled weight decay | primary | high |
| 4 | Reddi et al. | https://openreview.net/forum?id=ryQu7f-RZ | AMSGrad — max operator fix (ICLR 2018) | primary | high |
| 5 | Shazeer & Stern | https://arxiv.org/abs/1804.04235 | AdaFactor — sublinear memory | primary | high |
| 6 | Gupta et al. | https://arxiv.org/abs/1802.09568 | Shampoo — Kronecker preconditioner | primary | high |
| 7 | You et al. | https://arxiv.org/abs/1708.03888 | LARS — layer-wise scaling | primary | high |
| 8 | Liu et al. | https://arxiv.org/abs/1908.03265 | RAdam — rectified variance | primary | high |
| 9 | You et al. | https://arxiv.org/abs/1904.00962 | LAMB — BERT 76min | primary | high |
| 10 | Zhang et al. | https://arxiv.org/abs/1907.08610 | Lookahead — slow/fast weights | primary | high |
| 11 | Yong et al. | https://arxiv.org/abs/2004.01461 | Gradient Centralization | primary | high |
| 12 | Zhuang et al. | https://arxiv.org/abs/2010.07468 | AdaBelief — gradient surprise | primary | high |
| 13 | Foret et al. | https://arxiv.org/abs/2010.01412 | SAM — sharpness-aware | primary | high |
| 14 | Xie et al. | https://arxiv.org/abs/2208.06677 | Adan — proper Nesterov integration | primary | high |
| 15 | Chen et al. | https://arxiv.org/abs/2302.06675 | Lion — evolved sign momentum | primary | high |
| 16 | Liu et al. | https://arxiv.org/abs/2305.14342 | Sophia — diagonal Hessian for LLM | primary | high |
| 17 | Defazio & Mishchenko | https://arxiv.org/abs/2301.07733 | D-Adaptation — LR-free | primary | high |
| 18 | Mishchenko & Defazio | https://arxiv.org/abs/2306.06101 | Prodigy — improved D-Adaptation | primary | high |
| 19 | Vyas et al. | https://arxiv.org/abs/2409.11321 | SOAP — Adam in Shampoo eigenbasis | primary | high |
| 20 | Pagliardini et al. | https://arxiv.org/abs/2409.03137 | AdEMAMix — dual EMA | primary | high |
| 21 | Defazio et al. | https://arxiv.org/abs/2405.15682 | Schedule-Free — no LR schedule | primary | high |
| 22 | Jordan | https://kellerjordan.github.io/posts/muon/ | Muon — Newton-Schulz orthogonalization | blog | medium |
| 23 | arXiv:2511.20725 | https://arxiv.org/html/2511.20725v1 | Paper stále citován v 2025 surveys | secondary | high |
| 24 | zhanglabtools 2024 | https://github.com/zhanglabtools/DeepLearningTheory.course.2024 | Zařazen jako key paper | secondary | high |
| 25 | MIT OCW 6.7960 | https://ocw.mit.edu/courses/6-7960-deep-learning-fall-2024/pages/readings/ | Chybí na MIT reading listu | secondary | high |
| 26 | CS231n | https://cs231n.github.io/neural-networks-3/ | Chybí na Stanford | secondary | high |
| 27 | ODSC | https://opendatascience.com/an-overview-of-gradient-descent-optimization-algorithms/ | Republished pro praktiky | secondary | high |
| 28 | GitHub impl 1 | https://github.com/jElhamm/Overview-Gradient-Descent-Optimization-By-Sebastian-Ruder | Community implementace | secondary | high |

## Sources

1. Ruder — An overview of gradient descent optimization algorithms (blog) — https://ruder.io/optimizing-gradient-descent/
2. Semantic Scholar paper page — https://www.semanticscholar.org/paper/769ef3d5021cd71c37d2c403f231a53d1accf786
3. Loshchilov, Hutter — Decoupled Weight Decay (AdamW) — https://arxiv.org/abs/1711.05101
4. Reddi, Kale, Kumar — AMSGrad — https://arxiv.org/abs/1904.09237
5. Shazeer, Stern — Adafactor — https://arxiv.org/abs/1804.04235
6. Gupta et al. — Shampoo — https://arxiv.org/abs/1802.09568
7. You et al. — LARS — https://arxiv.org/abs/1708.03888
8. Liu et al. — RAdam — https://arxiv.org/abs/1908.03265
9. You et al. — LAMB — https://arxiv.org/abs/1904.00962
10. Zhang, Lucas, Hinton, Ba — Lookahead — https://arxiv.org/abs/1907.08610
11. Yong et al. — Gradient Centralization — https://arxiv.org/abs/2004.01461
12. Zhuang et al. — AdaBelief — https://arxiv.org/abs/2010.07468
13. Foret et al. — SAM — https://arxiv.org/abs/2010.01412
14. Xie et al. — Adan — https://arxiv.org/abs/2208.06677
15. Chen et al. — Lion — https://arxiv.org/abs/2302.06675
16. Liu et al. — Sophia — https://arxiv.org/abs/2305.14342
17. Defazio, Mishchenko — D-Adaptation — https://arxiv.org/abs/2301.07733
18. Mishchenko, Defazio — Prodigy — https://arxiv.org/abs/2306.06101
19. Vyas et al. — SOAP — https://arxiv.org/abs/2409.11321
20. Pagliardini et al. — AdEMAMix — https://arxiv.org/abs/2409.03137
21. Defazio et al. — Schedule-Free — https://arxiv.org/abs/2405.15682
22. Jordan — Muon — https://kellerjordan.github.io/posts/muon/
23. arXiv:2511.20725 — 2025 GD survey — https://arxiv.org/html/2511.20725v1
24. zhanglabtools — DL Theory Course 2024 — https://github.com/zhanglabtools/DeepLearningTheory.course.2024
25. MIT OCW 6.7960 — https://ocw.mit.edu/courses/6-7960-deep-learning-fall-2024/pages/readings/
26. CS231n — https://cs231n.github.io/neural-networks-3/
27. ODSC republication — https://opendatascience.com/an-overview-of-gradient-descent-optimization-algorithms/
28. GitHub implementation — https://github.com/jElhamm/Overview-Gradient-Descent-Optimization-By-Sebastian-Ruder

## Coverage Status

- **[VERIFIED]:** Obsah paperu (9 algoritmů, taxonomie, doporučení), všech 20 post-2017 optimizérů (arXiv URLs ověřeny), akademická a praktická recepce, absence na MIT/Stanford
- **[INFERRED]:** Chybějící paradigmata (syntéza z evidence), Adam vs SGD debata, zastaralost distribuované sekce
- **[SINGLE-SOURCE]:** Muon (blog post, ne peer-reviewed paper), AMSGrad praktická hodnota
- **[UNVERIFIED]:** Přesný Google Scholar citation count (bot-blocked)
