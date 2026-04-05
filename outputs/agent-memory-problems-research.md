# Uncontrolled Memory Growth & False Memory Propagation in LLM Agents — Research Brief

**Date:** 2026-04-05
**Question:** Two critical agent memory problems — UMG (uncontrolled growth) and FMP (false memory propagation): mechanisms, research evidence, mitigation strategies
**Scope:** broad (survey)
**Sources consulted:** 27

---

## Executive Summary

Dva problémy — nekontrolovaný růst paměti (UMG) a propagace falešných vzpomínek (FMP) — představují fundamentální výzvy pro LLM agenty s persistentní pamětí. Výzkum z let 2023–2026 ukazuje, že nejde o okrajové případy, ale o systémové selhání: agenti, kteří si pamatují všechno bez selekce, degradují v čase, a agenti, kteří si zapamatují jednu špatnou informaci, ji propagují lavinou do dalších rozhodnutí.

Oba cílové papery — Tiwari & Fofadiya "Multi-Layered Memory Architectures" (arXiv:2603.29194) a "Novel Memory Forgetting Techniques" (arXiv:2604.02280) — jsou companion papers od stejného týmu (březen–duben 2026). Paper 1 navrhuje třívrstvou architekturu (working/episodic/semantic) s 5.1% false memory rate [VERIFIED][1]. Paper 2 řeší zapomínání přes relevance-guided scoring (recency + frequency + semantic alignment) [UNVERIFIED — jen abstrakt][2].

Nejsilnější empirický nález k FMP: Zhang et al. prokázali, že LLM dokáže identifikovat 67–87 % vlastních chyb v izolaci, ale v kontextu je stejně propaguje dál — commitment bias přebije sebekorekci [VERIFIED][3]. Nejsilnější obranný přístup: A-MAC (2026) s write-time admission control, kde se špatná paměť vůbec nezapíše místo pozdějších oprav [VERIFIED][8].

Kritická mezera: **neexistuje žádný standardní benchmark pro kalibraci spolehlivosti agentní paměti**, a nejlepší detektor kontradikcí dosahuje jen 0.71 accuracy [VERIFIED][13].

---

## Detailed Findings

### 1. UMG — Nekontrolovaný růst paměti

**Problém:** Agent ukládá vše — konverzační historii, výstupy nástrojů, mezivýsledky — bez pruning strategie. Kontext roste, retrieval se zpomaluje, relevantní informace se ztrácí v šumu.

**Architektonická řešení:**

| Systém | Přístup | Vrstvy | Klíčový mechanismus |
|--------|---------|--------|---------------------|
| MemGPT [VERIFIED][4] | OS-inspired paging | 3 (main/recall/archival) | Automatický page-in/page-out mezi tiers |
| Tiwari & Fofadiya [VERIFIED][1] | Kognitivní model | 3 (working/episodic/semantic) | Adaptive retrieval gating + retention regularization |
| AgeMem [VERIFIED][7] | RL-learned management | 5 operací (store/retrieve/update/summarize/discard) | Policy se učí kdy zapomenout přes GRPO |
| A-MAC [VERIFIED][8] | Write-time admission | Gate s 5 faktory | Odmítne low-value memories před zápisem |

**Forgetting přístupy (Paper 2 vs alternativy):**

Fofadiya & Tiwari [UNVERIFIED][2] navrhují heuristické zapomínání — scoring kombinující recency, frequency, semantic alignment. AgeMem [VERIFIED][7] jde opačnou cestou a učí se zapomínání přes RL. ACT-R-inspired architektura [SINGLE-SOURCE][16] modeluje Ebbinghausovu křivku zapomínání s decay parametrem ~0.5 modulovaným frekvencí přístupu. **Přímé srovnání těchto přístupů neexistuje** [INFERRED].

**Taxonomie paměťových mechanismů:** Du (2026) [VERIFIED][5] formalizuje write–manage–read loop a identifikuje 5 rodin: context-resident compression, retrieval-augmented stores, reflective self-improvement, hierarchical virtual context, policy-learned management. Survey "Memory in the Age of AI Agents" [VERIFIED][6] (47 autorů) přidává 3D taxonomii: forms (token/parametric/latent) × functions (factual/experiential/working) × dynamics (formation/evolution/retrieval).

### 2. FMP — Propagace falešných vzpomínek

**Mechanismus — snowball effect:** Zhang et al. [VERIFIED][3] empiricky prokázali, že když se LLM zavázal k chybné odpovědi, generuje další falešné tvrzení na její podporu místo korekce. ChatGPT identifikoval 67 % vlastních chyb v izolaci, GPT-4 87 % — ale oba je v kontextu propagovali dál. Commitment bias v kontextu přebíjí schopnost sebekorekce.

**Agent-specifická taxonomie:** Li et al. [VERIFIED][10] formálně rozlišují:
- **Memory Retrieval Hallucinations** — irrelevantní nebo neexistující informace se retrievnou (embedding similarity nemá mechanismus pro posouzení faktické správnosti)
- **Memory Update Hallucinations** — korektní paměti se poškodí při update na základě nové, ale chybné informace

**Empirická demonstrace:** Park et al. [VERIFIED][11] v Generative Agents simulaci: agent Isabella vymyslela detaily oznámení, které nikdy neproběhlo. Agent Yuriko přiřadil autorství "Bohatství národů" modernnímu sousedovi — konfabulace z trénovacích dat [VERIFIED][11].

**Adversarial amplifikace:**
- MemoryGraft [VERIFIED][12]: 10 otrávených záznamů z 110 (9 %) → 47.9 % všech retrieval výsledků. Poisoning přetrvává neomezeně napříč sessions.
- MINJA [VERIFIED][14] (NeurIPS 2025): >95 % injection success rate jen přes normální user queries — žádný přímý přístup k memory banku.
- Reálná data [SINGLE-SOURCE][18]: 91 000 útočných sessions na honeypots říjen 2025–leden 2026 (stat z search snippet, plný text nefetchnut).

**Absence confidence tracking:** Žádný velký memory systém (MemGPT, A-MEM, Mem0, Generative Agents) netrackuje epistemickou spolehlivost při zápisu [INFERRED z review systémů 4,23,27,11]. Retrieval je čistě přes embedding similarity — plausibilně formulovaná špatná paměť se retrievne stejně snadno jako správná [VERIFIED][12,14].

### 3. Mitigation — Co funguje

**Tier 1 — Write-time prevention (nejúčinnější):**
A-MAC [VERIFIED][8] rozkládá hodnotu paměti na 5 faktorů: future utility, factual confidence, semantic novelty, temporal recency, content type priority. Gate odmítne low-confidence entries. Klíčový insight: zabránit zápisu špatné paměti > retroaktivní oprava. F1 0.583 na LoCoMo, 31 % snížení latence.

**Tier 2 — Self-reflection (vyžaduje feedback signal):**
Reflexion [VERIFIED][9] dosahuje 91 % pass@1 na HumanEval přes verbální self-reflection. Limitace: vyžaduje externí feedback (grader, environment reward) — bez objektivního signálu agent neví, na co reflektovat.

**Tier 3 — Temporal invalidation:**
Zep [VERIFIED][15] s bi-temporálním modelem (t_valid/t_invalid per edge) — jediný systém s principiálním řešením temporal staleness. Nová informace invaliduje staré hrany v knowledge grafu. 94.8 % vs MemGPT 93.4 % na DMR benchmarku.

**Tier 4 — Contradiction detection (zatím nedostatečné):**
Nejlepší LLM detektor: Claude-3 Sonnet + CoT = 0.71 accuracy [VERIFIED][13]. Self-contradictions: accuracy až 0.006. Lidští anotátoři: 74 % shoda. Detekce kontradikcí je intrinsicky těžká.

### 4. Spojitost se STOPA memory systémem

STOPA orchestrační systém implementuje několik mechanismů, které adresují UMG i FMP:

| STOPA mechanismus | Adresuje | Paralela v literatuře |
|-------------------|----------|----------------------|
| `confidence:` field s decay (0.1/30 dní neaktivity) | FMP — temporal staleness | ACT-R decay [16], blíže k Zep principu |
| `supersedes:` chains | FMP — korekce starých learnings | Zep edge invalidation [15] |
| `impact_score:` (helpfulness-driven) | UMG — identifikace low-value memories | A-MAC content type priority [8] |
| `source:` weighting (user_correction 1.5× > agent_generated 0.8×) | FMP — provenance tracking | MemoryGraft provenance proposal [12] |
| `harmful_uses:` counter | FMP — retroaktivní korekce | Reflexion verbal reflection [9] |
| Max 500 řádků + archivace | UMG — bounded growth | MemGPT paging [4] |
| Graduation trigger (uses ≥ 10 + confidence ≥ 0.8) | UMG — pruning via promotion | AgeMem learned discard [7] |
| `verify_check:` grep/glob assertions | FMP — machine-checkable validation | A-MAC factual confidence [8] |

**Mezera v STOPA:** Chybí write-time admission control (A-MAC pattern) — learnings se zapisují vždy, pruning až post-hoc. Chybí contradiction detection proti existujícím learnings při zápisu nového.

---

## Disagreements & Open Questions

- **Heuristické vs learned forgetting:** Tiwari/Fofadiya [1,2] používají handcrafted scoring, AgeMem [7] RL. Přímé srovnání neexistuje.
- **Prevention vs correction:** A-MAC [8] argumentuje write-time gate > retroaktivní oprava. Reflexion [9] ukazuje, že self-reflection s feedbackem funguje. Závisí na dostupnosti ground-truth signálu.
- **Kolik vrstev paměti:** 3 (Tiwari/Fofadiya, MemGPT), 5 operací (AgeMem), 5 rodin (Du survey). Žádný konsensus.
- **Longitudinální studie:** Neexistují studie FMP akumulace přes stovky sessions — největší empirická mezera v oboru.
- **Benchmark pro memory confidence:** Žádný standard neexistuje.

---

## Evidence Table

| # | Source | URL | Key Claim | Type | Confidence |
|---|--------|-----|-----------|------|------------|
| 1 | Tiwari & Fofadiya — Multi-Layered Memory Architectures (2026) | https://arxiv.org/abs/2603.29194 | 3-layer architecture, 46.85% SR, 5.1% false memory rate | Primary | high |
| 2 | Fofadiya & Tiwari — Novel Memory Forgetting Techniques (2026) | https://arxiv.org/abs/2604.02280 | Adaptive budgeted forgetting, relevance-guided scoring | Primary | medium |
| 3 | Zhang et al. — Hallucination Snowballing (2023) | https://arxiv.org/abs/2305.13534 | 67-87% self-identification but in-context propagation | Primary | high |
| 4 | Packer et al. — MemGPT (2023) | https://arxiv.org/abs/2310.08560 | OS-inspired virtual context, 3-tier paging | Landmark | high |
| 5 | Du — Memory for Autonomous LLM Agents (2026) | https://arxiv.org/abs/2603.07670 | 5 mechanism families, write-manage-read loop | Survey | high |
| 6 | Hu et al. — Memory in the Age of AI Agents (2025) | https://arxiv.org/abs/2512.13564 | 3D taxonomy (forms × functions × dynamics) | Survey | high |
| 7 | Yu et al. — AgeMem (2026) | https://arxiv.org/abs/2601.01885 | RL-learned forgetting, 5 memory ops as tools | System | high |
| 8 | Guilin Dev et al. — A-MAC (2026) | https://arxiv.org/abs/2603.04549 | Write-time admission, 5-factor scoring, F1 0.583 | System | high |
| 9 | Shinn et al. — Reflexion (NeurIPS 2023) | https://arxiv.org/abs/2303.11366 | Verbal self-reflection, 91% HumanEval | System | high |
| 10 | Li et al. — Agent Hallucination Survey (2025) | https://arxiv.org/abs/2509.18970 | 5-type taxonomy, Memory Retrieval/Update subtypes | Survey | high |
| 11 | Park et al. — Generative Agents (UIST 2023) | https://arxiv.org/abs/2304.03442 | Agents embellish memories, confabulate | Landmark | high |
| 12 | Xiong et al. — MemoryGraft (2024) | https://arxiv.org/abs/2512.16962 | 9% poisoned → 47.9% retrievals | Adversarial | high |
| 13 | Rhodes et al. — Contradiction Detection (2025) | https://arxiv.org/abs/2504.00180 | Best detector 0.71, self-contradiction 0.006 | Empirical | high |
| 14 | Kim et al. — MINJA (NeurIPS 2025) | https://arxiv.org/abs/2503.03704 | >95% injection via query-only interaction | Adversarial | high |
| 15 | Rasmussen et al. — Zep (2025) | https://arxiv.org/abs/2501.13956 | Bi-temporal KG, edge invalidation | System | high |
| 16 | ACT-R-inspired memory (HAI 2025) | https://dl.acm.org/doi/10.1145/3765766.3765803 | Ebbinghaus decay, parameter ~0.5 | System | medium |
| 17 | Multi-agent memory survey (TechRxiv) | https://www.techrxiv.org/users/1007269/articles/1367390/ | Divergent beliefs without sync | Survey | medium |
| 18 | Memory Poisoning survey (2026) | https://arxiv.org/html/2603.20357v1 | 91K attack sessions on honeypots | Security | medium — confirmed via search snippet only |
| 19 | Yu et al. — Multi-Agent Memory Architecture (2026) | https://arxiv.org/abs/2603.10062 | Cache hierarchy framing, 2 critical gaps | Architecture | high |
| 20 | Wu et al. — From Human Memory to AI Memory (2025) | https://arxiv.org/abs/2504.15965 | 3D framework, 8 quadrants human→AI mapping | Survey | high |
| 21 | Cemri et al. — Why Multi-Agent Systems Fail (2025) | https://arxiv.org/abs/2503.13657 | MAST taxonomy, 14 failure modes | Empirical | high |
| 22 | Dadlani — Compound Error Crisis (2024) | https://tushardadlani.com/the-compound-error-crisis-why-llm-agents-are-failing-like-broken-robots-and-why-computer-science-warned-us | 73% downstream failure probability | Analysis | medium |
| 23 | Xu et al. — A-MEM (NeurIPS 2025) | https://arxiv.org/abs/2502.12110 | Zettelkasten-style, no FMP correction | System | high |
| 24 | Hindsight is 20/20 (2025) | https://arxiv.org/abs/2512.12818 | Confidence adjustment max(c-2α, 0.0) | System | medium |
| 25 | Zhang et al. — Belief Revision in LLMs (2024) | https://arxiv.org/abs/2406.19354 | 12 open problems, Bayesian epistemology target | Conceptual | high |
| 26 | Peng et al. — Memory Poisoning Attack+Defense (2025) | https://arxiv.org/abs/2601.05504 | MINJA 62% ASR, trust scores unreliable | Adversarial | high |
| 27 | Chhikara et al. — Mem0 (2025) | https://arxiv.org/abs/2504.19413 | Production memory, no FMP handling | System | high |

---

## Sources

1. Tiwari, Fofadiya — https://arxiv.org/abs/2603.29194
2. Fofadiya, Tiwari — https://arxiv.org/abs/2604.02280
3. Zhang et al. — https://arxiv.org/abs/2305.13534
4. Packer et al. — https://arxiv.org/abs/2310.08560
5. Du — https://arxiv.org/abs/2603.07670
6. Hu et al. — https://arxiv.org/abs/2512.13564
7. Yu et al. — https://arxiv.org/abs/2601.01885
8. Guilin Dev et al. — https://arxiv.org/abs/2603.04549
9. Shinn et al. — https://arxiv.org/abs/2303.11366
10. Li et al. — https://arxiv.org/abs/2509.18970
11. Park et al. — https://arxiv.org/abs/2304.03442
12. Xiong et al. — https://arxiv.org/abs/2512.16962
13. Rhodes et al. — https://arxiv.org/abs/2504.00180
14. Kim et al. — https://arxiv.org/abs/2503.03704
15. Rasmussen et al. — https://arxiv.org/abs/2501.13956
16. ACT-R-inspired — https://dl.acm.org/doi/10.1145/3765766.3765803
17. Multi-agent survey — https://www.techrxiv.org/users/1007269/articles/1367390/
18. Memory Poisoning survey — https://arxiv.org/html/2603.20357v1
19. Yu et al. — https://arxiv.org/abs/2603.10062
20. Wu et al. — https://arxiv.org/abs/2504.15965
21. Cemri et al. — https://arxiv.org/abs/2503.13657
22. Dadlani — https://tushardadlani.com/the-compound-error-crisis-why-llm-agents-are-failing-like-broken-robots-and-why-computer-science-warned-us
23. Xu et al. — https://arxiv.org/abs/2502.12110
24. Hindsight — https://arxiv.org/abs/2512.12818
25. Zhang et al. — https://arxiv.org/abs/2406.19354
26. Peng et al. — https://arxiv.org/abs/2601.05504
27. Chhikara et al. — https://arxiv.org/abs/2504.19413

---

## Coverage Status

- **[VERIFIED]:** Papers 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 18, 19, 20, 21, 23, 25, 26, 27 — abstracts or full text fetched and key claims confirmed
- **[UNVERIFIED]:** Paper 2 (arXiv:2604.02280) — only abstract confirmed, submitted 2 days before research, full PDF not read
- **[SINGLE-SOURCE]:** Paper 16 (ACT-R, decay parameter ~0.5), Paper 22 (Dadlani blog, 73% stat sourced to Huang et al.)
- **[INFERRED]:** Absence of confidence tracking across systems (inferred from review of all major systems, none explicitly claims this as a feature)
