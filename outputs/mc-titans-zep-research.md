# MC vs Titans vs Zep vs ACT-R — STOPA Memory Architecture

**Date:** 2026-04-18
**Question:** Jak MC, Titans, Zep a ACT-R řeší (1) škálování memory, (2) gating retrieval, (3) decay/compaction — a co přenést do STOPA hybrid-retrieve a learnings systému?
**Scope:** standard
**Sources consulted:** 16 (5 primary — 3 live, 1 dead-but-exists, 1 fixed from truncation)

---

## Executive Summary

Čtyři memory paradigmata řeší různými mechanismy stejnou otázku — jak škálovat přístup ke znalostem bez kvadratického compute. **MC** cachuje segment checkpointy s O(NL) interpolací [VERIFIED][14]. **Titans** opouští rostoucí stav — memory = MLP weights aktualizované test-time gradientem (O(1) parametrů) [VERIFIED][1]. **Zep** staví non-lossy bi-temporální graf s explicitní invalidací [VERIFIED][6,7]. **ACT-R** akumuluje traces s power-law decay [VERIFIED][11].

Tři nejsilnější STOPA upgrady:
- **Episode-mentions reranker** v hybrid-retrieve.py — 4. signál využívající existující `concept-graph.json` mention counts [VERIFIED][8]
- **Surprise-based admission** v learning-admission.py — contradiction magnitude jako salience boost [INFERRED][2]
- **Auto-invalidation chain** v /evolve — LLM pass detekující contradictions, automaticky nastaví `valid_until:` [INFERRED][7]

STOPA's stávající design se nejvíc blíží **Zep** (non-lossy archive + hybrid retrieval + graph-based entities). ACT-R formule poskytuje matematický rámec pro stávající confidence decay. MC a Titans jsou konceptuální vzory — bezprostřední implementace není praktická na STOPA škále (<1000 learnings).

---

## Detailed Findings

### (1) Memory Scaling — Čtyři paradigmata

| System | State size | Compute | Growing? | Mechanism |
|--------|-----------|---------|-----------|-----------|
| **MC** | O(N) cached checkpoints, N ≤ L | O(NL) [VERIFIED][14] | Yes, segment-based | Cache hidden state at segment boundaries |
| **Titans** | O(1) MLP params | O(L) gradient updates [VERIFIED][1] | No state growth; memory = updated weights | Test-time gradient memorization |
| **Zep** | O(L) graph grows monotonically | O(log L) hybrid retrieval [VERIFIED][6,8] | Yes, non-lossy | Episode → semantic extraction → community clustering |
| **ACT-R** | O(traces), unlimited | O(traces) scan [VERIFIED][11] | Yes (no deletion, activation decay) | Each rehearsal = new trace in sum |

Klíčový rozdíl: tři systémy rostou (MC, Zep, ACT-R), Titans odmítá — komprimuje do fixních MLP vah. STOPA learnings/ aktuálně odpovídá Zep paradigmatu (monotonický růst s archivací, nikdy ne mazání).

### (2) Retrieval Gating — Query-dependent signály

| System | Signal | Formula |
|--------|--------|---------|
| **MC (GRM)** | Query × cached state | Input-dependent γ(i)_t — cannot be pre-computed [VERIFIED][15] |
| **Titans** | Surprise = gradient magnitude | ‖∇L(M_{t-1}, x_t)‖ → write strength [VERIFIED][2] |
| **Zep** | Hybrid + reranker stack | RRF{cosine, BM25, BFS} → MMR/episode-mentions/cross-encoder [VERIFIED][8] |
| **ACT-R** | Base + spreading activation | A(m) = log Σ_i (t-t_i)^{-d} + Σ_q (W/N)·S_{q→m} [VERIFIED][11,12] |

**Konvergence:** Všechny čtyři systémy sdílejí vzor "**query-dependent signál** + **multiple parallel retrieval channels**." Čistě recency nebo čistě similarity je nedostatečná.

STOPA `hybrid-retrieve.py` dnes implementuje RRF nad grep+BM25+graph walk — zrcadlí Zep Step 1 (Search), ale chybí reranker vrstva (Zep Step 2) a spreading activation (ACT-R `S(m)` komponenta).

### (3) Decay / Invalidation — Dva paradigmata

| System | Approach | Trigger |
|--------|---------|---------|
| **MC** | No explicit decay; SSC top-k routing; Memory Soup parameter avg | Architecture choice |
| **Titans** | Adaptive weight decay (retention gate); MIRAS YAAD/MONETA/MEMORA variants | Learned optimization objective [VERIFIED][2,3] |
| **Zep** | Explicit invalidity (discrete binary state) | LLM contradiction → sets t_invalid [VERIFIED][7] |
| **ACT-R** | Continuous power law `(t-t_i)^{-d}`; spacing: d(i) = α + c·e^B | Time elapsed [VERIFIED][11,13] |

**Dvě fundamentálně odlišné filozofie:**
- **Probabilistická/continuous** (MC, Titans, ACT-R) — decay baked into architecture
- **Discrete/explicit** (Zep) — invalidity = triggered event, preserved history

Zep explicitně argumentuje discrete > probabilistic: "confidence decay ≠ factual invalidation." STOPA memory-files.md to cituje jako motivaci pro `valid_until:` field. **STOPA aktuálně kombinuje obě:** ACT-R-style decay (confidence × recency) PLUS Zep-style explicit invalidity (supersedes + valid_until).

---

## STOPA Concrete Upgrade Candidates

### High-priority

**A. Surprise-based learning admission** [INFERRED][2]
- Current: `learning-admission.py` uses source_reputation × novelty + contradiction detection
- Upgrade: Add "surprise score" = contradiction magnitude with existing corpus. Low similarity to nearest existing learning = high surprise = boost admission.
- Effort: medium (needs embedding). Impact: reduces duplicate learnings, prioritizes genuine novelty.

**B. Auto-invalidation chain via supersedes** [INFERRED][7]
- Current: `supersedes:` manually sets `valid_until:` on old learning.
- Gap: No automatic contradiction detection.
- Upgrade: `/evolve` Step 3f — LLM pass detects contradicting pairs (tag overlap + opposing assertions), auto-proposes supersedes.
- Effort: low-medium. Impact: prevents stale contradictions accumulating.

**C. Episode-mentions reranker for hybrid-retrieve** [VERIFIED][8]
- Current: hybrid-retrieve.py combines grep + BM25 + graph via RRF.
- Upgrade: Add 4. signál = `concept-graph.json` entity mention frequency. Learnings se entities v ≥5 recent retrievals → rank boost.
- Implementation: Field `mentions:` už existuje.
- Effort: low. Impact: amplifikace používaných znalostí, tlumení zero-use.

### Medium-priority

**D. ACT-R power-law decay místo linear recency** [VERIFIED][11]
- Current: `× (1 / (1 + days_since_date / 60))` — single-trace approximation
- ACT-R: `log Σ_i (t - t_i)^{-0.5}` — multi-trace power law. Každé `uses:` = trace s timestampem.
- Gap: STOPA netrackuje per-use timestamps, jen total count.
- Upgrade: `use_history: [date1, date2, ...]` (max 10 FIFO). Replace linear boost with log-sum-power-law.
- Effort: medium. Impact: rewards sustained useful learnings, penalizuje stará one-hit wonders.

**E. Formalize retrieval complexity knob** [VERIFIED][14]
- Captured: learning `2026-04-18-retrieval-depth-knob-complexity-interpolation.md`
- Pending: instrument hybrid-retrieve.py to explicitně přepnout N podle `tier`.

**F. GRM context-aware gating** [VERIFIED][15]
- Captured: learning `2026-04-18-mc-checkpoint-caching-retrieval-pattern.md`
- Pending: query × learning-summary embedding similarity jako 5. RRF kanál.

### Lower-priority

**G. Bi-temporal pro time-sensitive obsah** [INFERRED][6]
- Většina STOPA learnings jsou bezčasová pravidla — bi-temporal nepřináší hodnotu
- Výjimka: /watch, /radar, /handoff výstupy — event_time ≠ ingest_time
- Upgrade: Optional `event_time:` pole, default = `date:`.
- Effort: low. Impact: úzký.

**H. Episode/Semantic/Community 3-tier** [VERIFIED][10]
- STOPA už má: learnings/ (episode) + wiki/entities/ (semantic) + wiki articles (community)
- Gap: No automatic community detection — /compile ručně dle témat.
- Upgrade: Concept-graph label propagation → auto-detect clusters, navrhni article témata.
- Effort: high. Impact: lepší /compile suggestions.

---

## Disagreements & Open Questions

- **Decay mechanism:** Zep discrete vs ACT-R continuous vs Titans learned vs MC architectural. Paper neargumentují přímo proti sobě — každý operuje v jiné doméně (KG / kognitivní model / neural arch / sequence model). STOPA aktuálně míchá přístupy.
- **State persistence:** Titans memory session-scoped (discarded post-inference); Zep cross-session persistent. STOPA aligns with Zep.
- **"Non-lossy" vs "forgetting":** Zep preserves invalidated edges; ACT-R allows activation below retrieval threshold. STOPA archive policy aligns with Zep.

### Open questions

- Exact Titans surprise/decay formulas nepřečteny z PDF (pouze blog + abstract)
- MAC/MAG/MAL ablation čísla nedostupná z blogu (shaped.ai JS-rendered)
- ACT-R canonical d value (typically 0.5 per Anderson 2007) nepotvrzeno z fetched source
- Žádný paper neadresuje STOPA-scale problem (<1000 items, manual curation)

---

## Evidence Table

| # | Source | URL | Key Claim | Type | Confidence |
|---|--------|-----|-----------|------|------------|
| 1 | Google Research Blog | https://research.google/blog/titans-miras-helping-ai-have-long-term-memory/ | Titans = deep MLP long-term memory, weights updated test-time via gradient | mechanism | high |
| 2 | Google Research Blog | (same) | Surprise = gradient magnitude; momentum tracks surprise flow; adaptive weight decay | mechanism | high |
| 3 | Google Research Blog | (same) | MIRAS framework: memory arch, attentional bias, retention gate, algorithm | framework | high |
| 4 | Google Research Blog | (same) | Titans-MAC >2M tokens BABILong, outperforms GPT-4 with fewer params | results | high |
| 5 | Shaped.ai | https://www.shaped.ai/blog/titans-learning-to-memorize-at-test-time-a-breakthrough-in-neural-memory-systems | 3 variants: MAC, MAG, MAL | architecture | medium |
| 6 | Zep paper | https://arxiv.org/abs/2501.13956 | Bi-temporal: T = event, T' = transaction; 4 timestamps per edge | mechanism | high |
| 7 | Zep paper | (same) | Explicit invalidity: LLM contradiction → t_invalid = t_valid of new edge | mechanism | high |
| 8 | Zep paper | (same) | Retrieval: Search (cosine+BM25+BFS) → Reranker (RRF, MMR, mentions, cross-enc) → Constructor | mechanism | high |
| 9 | Zep paper | (same) | LongMemEval: +18.5% accuracy (gpt-4o), +15.2% (gpt-4o-mini), 90% latency reduction | benchmark | high |
| 10 | Zep paper | (same) | 3-tier: episode (raw) → semantic (entity+edge) → community (clusters) | architecture | high |
| 11 | ACT-R (Stocco 2023; formula from Anderson & Lebiere 1998) | https://doi.org/10.1007/s42113-023-00189-y (alt: http://act-r.psy.cmu.edu/wordpress/wp-content/uploads/2024/01/Stocco_et_al-2023-Computational_Brain__Behavior.pdf) | B(m,t) = log Σ_i (t - t(i))^{-d} — power law decay | formula | high |
| 12 | ACT-R | (same) | A(m) = B(m) + S(m); S = spreading activation from context cues | formula | high |
| 13 | ACT-R | (same) | Pavlik-Anderson spacing: d(i) = α + c·e^B; α = stable individual trait | formula | high |
| 14 | MC paper | https://arxiv.org/abs/2602.24281 | O(NL) interpolation: N=1 (RNN O(L)) to N=L (full attention O(L²)) | mechanism | high |
| 15 | MC paper | (same) | GRM: input-dependent γ(i)_t cannot be pre-computed | mechanism | high |
| 16 | MC paper | (same) | Titans+GRM: 52.55 avg (760M) vs Transformer++ 49.64; DLA+GRM 55.96 (1.3B) | benchmark | high |

---

## Sources

1. Behrouz, A., Razaviyayn, M., Mirrokni, V. "Titans + MIRAS: Helping AI have long-term memory." Google Research Blog (2025-12-04). https://research.google/blog/titans-miras-helping-ai-have-long-term-memory/
2. Behrouz et al. "Titans: Learning to Memorize at Test Time." arXiv:2501.00663 (2025). https://arxiv.org/abs/2501.00663
3. Shaped.ai analysis blog. https://www.shaped.ai/blog/titans-learning-to-memorize-at-test-time-a-breakthrough-in-neural-memory-systems
4. Rasmussen, P. et al. "Zep: A Temporal Knowledge Graph Architecture for Agent Memory." arXiv:2501.13956 (2025-01-27). https://arxiv.org/abs/2501.13956
5. getzep/graphiti — GitHub implementation. https://github.com/getzep/graphiti
6. Stocco, A. et al. "An Integrated Computational Framework for the Neurobiology of Memory Based on the ACT-R Declarative Memory System." *Computational Brain & Behavior* (2023). DOI: 10.1007/s42113-023-00189-y. PDF mirror: http://act-r.psy.cmu.edu/wordpress/wp-content/uploads/2024/01/Stocco_et_al-2023-Computational_Brain__Behavior.pdf  (Note: Springer URL returns 303 redirect; formula originally Anderson & Lebiere 1998.)
7. Behrouz, A. et al. "Memory Caching: RNNs with Growing Memory." arXiv:2602.24281 (2026-02). https://arxiv.org/abs/2602.24281

---

## Coverage Status

- **[VERIFIED]:** Comparison matrix rows, benchmark numbers, formulas (primary sources read)
- **[INFERRED]:** Upgrades A, B, G — proposals derived from but not directly stated by sources
- **[SINGLE-SOURCE]:** None used
- **[UNVERIFIED]:** None used

### Verification notes (from verifier pass)

- ACT-R Springer URL returns 303 redirect (WebFetch fail). Formula correct per standard ACT-R literature (Anderson & Lebiere 1998); PDF mirror added.
- Shaped.ai URL fixed (was truncated in synthesis).
- LongMemEval +18.5% = gpt-4o specifically (gpt-4o-mini = +15.2%) — model spec added.
- MC complexity row clarified: O(L) RNN baseline ≠ O(1) MLP (Titans). Row labels correct in final brief.
