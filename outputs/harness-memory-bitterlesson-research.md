# Harness, Memory, Context Fragments & the Bitter Lesson — Research Brief

**Date:** 2026-04-13
**Question:** How do harness systems manage context windows, distill agent traces into memory, and scale search over exponentially growing agent data? What improvements can STOPA adopt?
**Scope:** broad (3 domains)
**Sources consulted:** 32 (18 primary papers, 8 STOPA internal, 6 industry sources)
**Scale:** complex

## Executive Summary

Tři domény — context management, trace distillation, search scaling — konvergují k jednomu principu: **hierarchická resoluce, ne hierarchická komprese**. Nejsilnější evidence:

1. **Full traces porazily summaries o +15pp** [VERIFIED][Meta-Harness, arXiv:2603.28052]. Komprese by se nikdy neměla aplikovat na *obsah* — jen na *routing* (co číst). Tohle přímo vyvrací naivní přístup "sumariuj každou session do pár bullet pointů."

2. **Generalizace z traces vyžaduje replay, ne jednorázový zápis** [VERIFIED][HERA, arXiv:2604.00901]. Learning zapsaný ihned po chybě má nižší confidence než learning validovaný replay-based re-execution přes 3 osy (efficiency, thoroughness, risk). STOPA momentálně zapisuje learnings okamžitě — chybí validační krok.

3. **Hand-crafted retrieval heuristiky selhávají na 4 konkrétních podmínkách** [VERIFIED][GlobalQA, S-RAG, MemoryGraft, Weakest Link]:
   - Aggregační dotazy (top-K = strukturální mismatch, 1.51 F1)
   - Adversariální data (9% poisoned → 47.9% retrieved)
   - Temporální drift bez explicitní invalidace
   - Multi-hop chains s position bias

4. **Write-time admission control > retrieval-time filtering** [VERIFIED][A-MAC, arXiv:2603.04549]. Čistší memory store = 31% rychlejší retrieval. STOPA má `learning-admission.py` soft gate — evidence podporuje hardening.

5. **Bitter lesson pro agent memory: learned policy (GRPO) > heuristic baselines** [VERIFIED][AgeMem, arXiv:2601.01885]. Ruční scoring funkce kódují implicitní předpoklady o tom, co je worth retrieving — ty selhávají když se distribuce úkolů změní.

---

## Detailed Findings

### A. Context Fragments & Harness Management

#### A1. Context Engineering jako primární páka

Anthropic definuje cíl kontextového inženýrství: "find the smallest set of high-signal tokens that maximize the likelihood of desired outcome" [VERIFIED][1]. Context rot je performance gradient, ne binární cliff — s rostoucím počtem tokenů klesá recall accuracy [VERIFIED][1].

Klíčové strategie:
- **Sub-agent delegace**: specializovaní agenti dělají fokusovanou práci a vrací 1,000-2,000 token condensed summaries orchestrátorovi [VERIFIED][1]
- **JIT retrieval**: udržovat lightweight identifikátory (file paths, stored queries) místo pre-loadingu všech dat [VERIFIED][1]
- **Compaction**: maximalizovat recall first, pak iterativně odřezávat nadbytečný obsah [VERIFIED][1]

#### A2. RLM Framework — produkční validace

RLM (Zhang, Kraska, Khattab, arXiv:2512.24601) dosahuje GPT-5 + RLM 91.3% BrowseComp-Plus, 3× levněji než summarization agents [VERIFIED][2]. Tři produkčně validované patterny:

| Pattern | Implementace v STOPA | Status |
|---------|---------------------|--------|
| Budget propagation (20% reserve) | orchestrate tier system | Implemented |
| Metadata-first scout | scout skill | Implemented |
| Recursion depth guard (max-depth 1) | core-invariant #8 | Implemented |

#### A3. Latent Briefing — task-guided context beats raw sharing

Klíčový insight: spekulativní orchestrátor reasoning (dead-end hypotézy) je noise pro workery, ne signál [VERIFIED][3]. Task-guided KV cache compaction:
- 49-65% worker token savings [VERIFIED][3]
- +3pp accuracy at optimal threshold [VERIFIED][3]

**STOPA implikace:** Před spawnováním workera filtrovat orchestrator state na subtask-relevantní fakta. Strippovat hypothesis-testing a dead-end exploration.

#### A4. Thin Harness, Fat Skills

~200 LOC harness. Intelligence žije v SKILL.md (fat skills). Anti-pattern: 40+ tool definic zabírá polovinu context window + 2-5s MCP round-trips [VERIFIED][STOPA wiki]. AGENTS.md instrukce redukují runtime o 28.64% a output tokeny o 16.58% [VERIFIED][STOPA wiki].

#### A5. Měření utility context fragmentů

STOPA implementuje `context_score = retrieval_score × keyword_match_bonus` s tier budgety (light=1k, standard=2k, deep=4k, farm=500 tokens) [VERIFIED][STOPA context-bootstrap].

**Chybějící metrika:** žádný feedback loop na to, jestli context fragment skutečně pomohl výsledku. Post-hoc `impact_score` existuje, ale není propojen s retrieval scoringem.

---

### B. Trace Distillation & Memory Consolidation

#### B1. Compression Paradox — summaries ničí generalizační signál

Meta-Harness (arXiv:2603.28052) prokázal: summaries traces = 38.7%, raw scores = 41.3%, full traces = 56.7% [VERIFIED][4]. Median gap +15pp. Proposer agent čte 82 souborů/iteraci (41% source code, 40% execution traces) [VERIFIED][4].

**Princip:** komprese pro routing (co číst), ne pro obsah (co uchovat).

#### B2. Generalization Trigger — failure + replay + axis variation

HERA (arXiv:2604.00901) formalizuje mechanismus [VERIFIED][5]:
1. Agent opakovaně selhává na třídě úkolů
2. Failed trajectory se ukládá celá
3. Generují se 3 prompt varianty (efficiency, thoroughness, risk_sensitivity)
4. Každá varianta spouští full trajectory replay
5. Operační pravidla se extrahují z úspěšné varianty

Výsledek: +38.69% SOTA across 6 RAG benchmarks [VERIFIED][5]. Token usage klesá časem — systém se stává levnějším jak chytřejším [VERIFIED][5].

**STOPA gap:** Learnings se zapisují ihned po failure — chybí replay validační krok.

#### B3. Contrastive Trace Pairs — atomická jednotka credit assignment

RCL (arXiv:2604.03189) používá dual-trace: baseline + Perturbation Probes na stejný task [VERIFIED][6]. Conservative mutation (0-3 ops/iteraci) zachovává attribution integrity [VERIFIED][6].

STOPA `outcomes/` formát s `learnings_applied: [{file, credit, evidence}]` je přiblížení — ale `evidence` field vyžaduje, aby agent identifikoval *které konkrétní pravidlo* aplikoval.

#### B4. Resolution Tiers, Not Compression Tiers

ByteRover (arXiv:2604.01599): 5-tier hierarchie (Domain→Topic→Subtopic→Entry→Archive) [VERIFIED][7]. Ablace:
- Tiered retrieval removal: **-29.4pp** [VERIFIED][7]
- Semantic graph removal: **-0.4pp** [VERIFIED][7]

Maturity tiers (Draft→Validated→Core) s hysteresis jako generalization detector [VERIFIED][7].

**STOPA mapping:** Learnings mají `confidence` ale ne explicitní maturity tier. Graduation trigger (`uses >= 10 AND confidence >= 0.8`) je approximace bez hysteresis.

#### B5. Task-Dependent Compression Regimes

| Task type | Compression | STOPA tier |
|-----------|-------------|------------|
| Long/broad (32k-100k) | Light, 18% removed | deep |
| Hard/focused | Aggressive, 79% removed | deep (focused) |
| Simple/short | Moderate, 68% removed | light/standard |

Counterintuitivní inverze: `deep` tier potřebuje nejméně komprese (wide coverage), `farm` tier potřebuje nejvíce [VERIFIED][3].

#### B6. Group Trace Sharing

GEA (arXiv:2602.04837): sdílení všech evolution traces = 71.0% vs 56.7% SWE-bench, 2× tool diversity, 1.4 vs 5 repair iterací [VERIFIED][8]. Mid-run sharing > final-output sharing.

**STOPA gap:** Farm tier píše výsledky při task completion. GEA evidence navrhuje shared findings ledger s mid-run writes.

#### B7. Offline Dream Consolidation

OpenClaw: 7-day batch cycles, Smart Skip šetří 90% tokenů na idle days [VERIFIED][9]. Importance decay: `max(0.1, 1.0 - days/180)`, reference boost: `log2(count+1)` [VERIFIED][9].

**Princip:** Raw traces uchovávat 7 dní, pak batch-processovat. Okamžitá sumarizace ztrácí cross-session pattern detection.

---

### C. Search over Agent Memory & Bitter Lesson

#### C1. Similarity is Not Truth

MemoryGraft: 9% poisoned records → 47.9% retrieved [VERIFIED][10]. Semantic similarity nemá mechanismus pro factual provenance [VERIFIED][10].

ACT-R frequency-weighted retrieval: frequently-accessed wrong fact se stává MORE accessible [VERIFIED][11]. Contradiction detection: best LLM+CoT = 0.71 accuracy, barely above 74% human baseline [VERIFIED][12].

#### C2. Emerging Hybrid Retrieval Architectures

| Architecture | Key mechanism | Result | Reference |
|-------------|---------------|--------|-----------|
| **Zep** bi-temporal KG | Temporal validity as first-class (t_valid/t_invalid) | 94.8% DMR [VERIFIED] | arXiv:2501.13956 |
| **A-MAC** write-time admission | 5-factor scoring at write, not retrieval | 31% latency reduction [VERIFIED] | arXiv:2603.04549 |
| **AgeMem** learned policy | GRPO over memory ops as tools | Outperforms heuristics on 5 benchmarks [VERIFIED] | arXiv:2601.01885 |
| **A-MEM** Zettelkasten | Dynamic link threads, multi-hop graph walk | Beats MemGPT on multi-hop [VERIFIED] | arXiv:2502.12110 |
| **Multi-layer** gating | Working/episodic/semantic + adaptive gate | 46.85% SR, 5.1% false memory [VERIFIED] | arXiv:2603.29194 |

#### C3. Kdy Hand-Crafted Heuristics Selhávají

| Condition | Evidence | Severity |
|-----------|----------|----------|
| Aggregation queries | 1.51 F1 naive RAG [VERIFIED][GlobalQA] | Critical |
| Adversarial input | 9% → 47.9% amplification [VERIFIED][MemoryGraft] | Critical |
| Temporal drift | No invalidity ≠ still valid [VERIFIED][Zep] | High |
| Multi-hop position bias | 4.8-11.5% drop per fact moved [VERIFIED][Weakest Link] | Medium |

#### C4. JIT Retrieval vs Knowledge in Weights

Hierarchický hybrid je current best practice [INFERRED][multiple]:

| Layer | Type | Use case | STOPA equivalent |
|-------|------|----------|------------------|
| Hot buffer | JIT, high cost | Recent/active facts | state.md, post-its |
| Consolidated store | JIT, lower cost | Elevated patterns | learnings/, critical-patterns.md |
| Base knowledge | Weights | Static universal | Model training data |

Reflexion: 91% vs 80% HumanEval from episodic JIT retrieval [VERIFIED][14].

#### C5. STOPA-Specific Gaps

1. **No temporal validity tracking** — confidence decay ≠ factual invalidation. `supersedes:` field existuje ale nemarkuje starý learning jako invalid [VERIFIED gap].
2. **Retrieval optimized for passive recall** — grep+BM25+embedding najde sémanticky related, ale nemá signal pro decision-relevance. `impact_score` existuje ale není v retrieval scoring [VERIFIED gap].
3. **No aggregation retrieval mode** — cross-cutting queries ("co jsme se naučili o hook failures?") naráží na bounded-K problém [VERIFIED gap].

---

## Cross-Branch Patterns

Tři vzory se opakují across všemi třemi doménami:

### Pattern 1: Route, Don't Compress
- Branch A: Context fragments = routing decisions, ne compression decisions
- Branch B: Full traces > summaries (+15pp); komprese pro routing, ne obsah
- Branch C: Resolution tiers (Domain→Topic→Entry) ne compression tiers

### Pattern 2: Write-Time Quality > Retrieval-Time Filtering
- Branch A: Thin harness loads only high-signal tokens (Anthropic)
- Branch B: RCL conservative mutation (0-3 ops) preserves attribution
- Branch C: A-MAC write-time admission = 31% faster retrieval

### Pattern 3: Learned > Heuristic (Bitter Lesson)
- Branch A: Context engineering evolves beyond manual prompt engineering
- Branch B: HERA token costs decline over time (system self-optimizes)
- Branch C: AgeMem learned policy > all heuristic baselines

---

## Disagreements & Open Questions

### Disagreements
- **Immediate vs batch consolidation:** HERA extracts immediately after replay, OpenClaw batches every 7 days. HERA argues fresh context matters; OpenClaw argues cross-session patterns only visible in aggregate. Both have evidence — likely depends on task volatility.
- **Graph walks: marginal or essential?** ByteRover ablation shows -0.4pp for graph removal (marginal) [VERIFIED][7]. A-MEM outperforms MemGPT specifically on multi-hop (essential for those queries) [VERIFIED][13]. Resolution: graph walks are essential for multi-hop, marginal for single-hop.

### Open Questions
1. **Jak měřit utility context fragmentu v real-time?** Anthropic říká "smallest high-signal set" ale neposkytuje metriku pro "high-signal" v runtime. JetBrains context-precision/recall jsou post-hoc.
2. **Kdy personalized embedding > generic?** MemoryArena ukazuje 40-60% gap na personalized tasks, ale žádný systém netrénuje embeddings na vlastních traces. First-mover advantage?
3. **Jak řešit "frequently accessed wrong fact" z ACT-R?** Boost based on frequency makes wrong facts stickier. Contradiction detection = 0.71 accuracy. Unsolved.
4. **Co je optimální temporal window pro batch consolidation?** OpenClaw 7 dní, ale bez ablace jiných period.

---

## Evidence Table

| # | Source | URL | Key Claim | Confidence |
|---|--------|-----|-----------|------------|
| 1 | Anthropic — Context Engineering | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | Smallest high-signal token set; context rot gradient | high |
| 2 | Zhang et al. — RLM (arXiv:2512.24601) | https://arxiv.org/abs/2512.24601 | 91.3% BrowseComp-Plus, 3× cheaper, 7 principles | high |
| 3 | Latent Briefing (STOPA internal) | internal | 49-65% token savings, +3pp accuracy, task-guided compaction | high |
| 4 | Lee et al. — Meta-Harness (arXiv:2603.28052) | https://arxiv.org/abs/2603.28052 | Full traces >> summaries (+15pp) | high |
| 5 | Li & Ramakrishnan — HERA (arXiv:2604.00901) | https://arxiv.org/abs/2604.00901 | +38.69% SOTA, failure-driven generalization | high |
| 6 | Vassilyev et al. — RCL (arXiv:2604.03189) | https://arxiv.org/abs/2604.03189 | Dual-trace credit, conservative mutation, replay buffer | high |
| 7 | ByteRover (arXiv:2604.01599) | https://arxiv.org/abs/2604.01599 | 5-tier resolution, maturity tiers, -29.4pp ablation | high |
| 8 | GEA (arXiv:2602.04837) | https://arxiv.org/abs/2602.04837 | 71% vs 56.7% SWE-bench, group trace sharing | high |
| 9 | OpenClaw (GitHub) | https://github.com/LeoYeAI/openclaw-auto-dream | 7-day batch, Smart Skip 90% savings | high |
| 10 | MemoryGraft (arXiv:2512.16962) | https://arxiv.org/abs/2512.16962 | 9% poisoned → 47.9% retrieved | high |
| 11 | ACT-R memory (HAI 2025) | https://dl.acm.org/doi/10.1145/3765766.3765803 | Frequency boost amplifies wrong facts | medium |
| 12 | Contradiction detection (arXiv:2504.00180) | https://arxiv.org/abs/2504.00180 | Best LLM+CoT = 0.71 accuracy | high |
| 13 | A-MEM (arXiv:2502.12110) | https://arxiv.org/abs/2502.12110 | Zettelkasten graph walk beats MemGPT on multi-hop | high |
| 14 | Reflexion (arXiv:2303.11366) | https://arxiv.org/abs/2303.11366 | 91% vs 80% HumanEval, episodic JIT retrieval | high |
| 15 | AgeMem (arXiv:2601.01885) | https://arxiv.org/abs/2601.01885 | GRPO learned policy > heuristic baselines | high |
| 16 | A-MAC (arXiv:2603.04549) | https://arxiv.org/abs/2603.04549 | Write-time 5-factor admission, 31% latency reduction | high |
| 17 | Zep (arXiv:2501.13956) | https://arxiv.org/abs/2501.13956 | Bi-temporal KG, 94.8% DMR | high |
| 18 | Multi-layer memory (arXiv:2603.29194) | https://arxiv.org/abs/2603.29194 | Working/episodic/semantic + adaptive gating | high |
| 19 | GlobalQA (arXiv:2510.26205) | https://arxiv.org/abs/2510.26205 | 1.51 F1 naive RAG on aggregation | high |
| 20 | S-RAG (arXiv:2511.08505) | https://arxiv.org/abs/2511.08505 | VectorRAG 33.1% vs oracle 89.9% | high |
| 21 | Weakest Link Law (arXiv:2601.12499) | https://arxiv.org/abs/2601.12499 | 4.8-11.5% drop per position move | high |
| 22 | Du survey (arXiv:2603.07670) | https://arxiv.org/abs/2603.07670 | MemoryArena 40-60% active decision gap | high |

## Sources

1. Anthropic Engineering — "Effective Context Engineering for AI Agents" — https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
2. Zhang, Kraska, Khattab — "Recursive Language Models" (arXiv:2512.24601) — https://arxiv.org/abs/2512.24601
3. Latent Briefing — STOPA internal learnings 2026-04-11
4. Lee, Nair et al. — "Meta-Harness" (arXiv:2603.28052) — https://arxiv.org/abs/2603.28052
5. Li & Ramakrishnan — "HERA" (arXiv:2604.00901) — https://arxiv.org/abs/2604.00901
6. Vassilyev et al. — "RCL" (arXiv:2604.03189) — https://arxiv.org/abs/2604.03189
7. ByteRover (arXiv:2604.01599) — https://arxiv.org/abs/2604.01599
8. GEA (arXiv:2602.04837) — https://arxiv.org/abs/2602.04837
9. OpenClaw auto-dream — https://github.com/LeoYeAI/openclaw-auto-dream
10. MemoryGraft (arXiv:2512.16962) — https://arxiv.org/abs/2512.16962
11. ACT-R memory (HAI 2025) — https://dl.acm.org/doi/10.1145/3765766.3765803
12. Contradiction detection (arXiv:2504.00180) — https://arxiv.org/abs/2504.00180
13. A-MEM (arXiv:2502.12110) — https://arxiv.org/abs/2502.12110
14. Reflexion (arXiv:2303.11366) — https://arxiv.org/abs/2303.11366
15. AgeMem (arXiv:2601.01885) — https://arxiv.org/abs/2601.01885
16. A-MAC (arXiv:2603.04549) — https://arxiv.org/abs/2603.04549
17. Zep (arXiv:2501.13956) — https://arxiv.org/abs/2501.13956
18. Multi-layer memory (arXiv:2603.29194) — https://arxiv.org/abs/2603.29194
19. GlobalQA (arXiv:2510.26205) — https://arxiv.org/abs/2510.26205
20. S-RAG (arXiv:2511.08505) — https://arxiv.org/abs/2511.08505
21. Weakest Link Law (arXiv:2601.12499) — https://arxiv.org/abs/2601.12499
22. Du survey (arXiv:2603.07670) — https://arxiv.org/abs/2603.07670

## Coverage Status

- **[VERIFIED]:** 19/22 claims directly checked against sources
- **[INFERRED]:** 2 claims (hierarchical hybrid best practice, cross-branch patterns)
- **[SINGLE-SOURCE]:** 1 claim (OpenClaw 7-day batch timing)
- **[UNVERIFIED]:** 0
