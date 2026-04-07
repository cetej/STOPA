# Vertikální škálování v orchestraci — Research Brief

**Datum:** 2026-04-07
**Otázka:** Jak implementovat systematickou traversaci mezi úrovněmi abstrakce (mikro/mezo/makro) v orchestračním systému STOPA?
**Scope:** complex (3 domény: akademická AI, SW architektura, token ekonomika)
**Zdrojů konzultováno:** 12 přímých čtení, 80+ URL z discovery

---

## Executive Summary

Současné orchestrační systémy (včetně STOPA) operují horizontálně — rozlišují role agentů (scout, critic, worker), ale nerozlišují **úroveň abstrakce**, na které agent pracuje. Výzkum ukazuje, že toto je zásadní mezera:

1. **Flat RAG selhává na komplexních kódových bázích** [VERIFIED][2] — logika distribuovaná přes hierarchickou adresářovou strukturu je neviditelná pro snippet-level retrieval. HCAG (arXiv:2603.20299) dokazuje, že hierarchická abstrakce (projekt→modul→funkce) je cost-optimální vs flat a iterativní RAG.

2. **Multi-agent hierarchie násobí tokeny 26-77×** [VERIFIED][8,9] — ale hierarchická paměť (xMemory) redukuje o 48% [SINGLE-SOURCE][7] a komprese skills o 75% [VERIFIED][1]. Vertikální škálování je tedy drahé jen pokud se dělá naivně.

3. **Tři agenti jsou optimum** [VERIFIED][3] — HexMachina empiricky prokázala, že 3-agent core (Orchestrator/Analyst/Coder) překonává 5-agent design kvůli "dilution from additional roles". Více agentů ≠ lepší výsledek.

4. **Fázová separace (discovery→improvement) je kritická** [VERIFIED][3] — bez ní agenti konvergují na mělké heuristiky. Pro vertikální škálování to znamená: nejdřív zmapuj stav na všech úrovních, teprve pak plánuj a exekuuj.

---

## Detailní zjištění

### A. Akademické základy hierarchického reasoning

#### A1. HMAS Taxonomie — 5 os hierarchických systémů

HMAS Taxonomy (arXiv:2508.12683) definuje 5 designových os [VERIFIED][1]:

| Osa | Popis | Relevance pro STOPA |
|-----|-------|---------------------|
| **Control hierarchy** | Centralizovaný → decentralizovaný spektrum | STOPA = hybridní (orchestrator řídí, worker má autonomii) |
| **Information flow** | Jak znalosti proudí nahoru/dolů | state.md = summary nahoru; task context = detail dolů |
| **Role delegation** | Statické vs dynamické přidělování rolí | Tier system = statická alokace per budget |
| **Temporal layering** | Vysokoúrovňové plánování vs nízkoúrovňová exekuce | **KLÍČOVÁ osa pro vertikální škálování** |
| **Communication** | Struktura zpráv mezi agenty | Skill contracts (input/output) |

**Temporal layering** je přímo aplikovatelná: vysokoúrovňový agent operuje na abstraktním stavovém prostoru (architektura projektu, business intent), nízkoúrovňový na detailních akcích (editace řádku, test). Hybridní architektura (hierarchická + decentralizovaná) je doporučena jako nejškálovatelnější [VERIFIED][1].

#### A2. HCAG — Hierarchická abstrakce kódu je cost-optimální

HCAG (arXiv:2603.20299) přímo řeší multi-scale code reasoning [VERIFIED][2]:

**Problém:** Flat RAG selhává protože logika systému je distribuovaná přes hierarchickou adresářovou strukturu — cross-file závislosti, architektonické vzory neviditelné na snippet úrovni.

**Řešení — 2 fáze:**
1. **Offline hierarchická abstrakce:** LLM rekurzivně parsuje repozitář → multi-vrstvá sémantická KB propojující teorii/architekturu/implementaci
2. **Online top-down retrieval:** Level-wise search od architektury dolů k implementačním snippetům

**Vzor "architecture-then-module":** Nejdřív nastav architektonický scaffold, pak vyplň modul-level detaily. Toto přímo mapuje na `orchestrate→scout→worker` řetěz.

**Cost-optimality:** Teoretický důkaz, že hierarchická abstrakce s adaptivní kompresí uzlů je optimální vs flat RAG [VERIFIED][2].

#### A3. HTN+LLM — Čistě LLM hierarchie je křehká

arXiv:2511.18165 ukazuje [VERIFIED][3]:
- Parsing success rate pro hierarchické plány: ~36%
- Syntaktická validita: **1% pro hierarchické** vs 20% pro flat plány
- Doporučení: LLM generuje strukturu, symbolický plánovač vynucuje konzistenci

**Pro STOPA:** Validuje circuit breakers a verification hooks. LLM self-compliance je nedostatečná — strukturální enforcement (hooks, kontrakty) je nutný.

### B. Praktické vzory pro vertikální bridging

#### B1. HexMachina — Fázová separace a kompilovaný artefakt

arXiv:2506.04651v2 [VERIFIED][3]:

- **Dvě fáze:** Discovery (mapování prostředí) → Improvement (strategie). Bez discovery agenti konvergují na "shallow 1-ply lookahead heuristics"
- **Kompilovaný artefakt:** LLM navrhne strategii → Python třída ji kóduje → exekuce bez re-dotazování LLM. **Bridge mezi strategickou inteligencí a taktickou exekucí.**
- **3 agenti > 5 agentů:** Orchestrator/Analyst/Coder překonává 5-agent design (54.1% vs 16.4% win rate against Reflexion-style)
- **"Dilution from additional roles"** — víc specializací = víc šumu

**Aplikace:** Orchestrátor by měl produkovat *plan artifact* (strukturovaný JSON/YAML), ne dělat per-step LLM volání.

#### B2. GoalAct — Průběžně aktualizovaný globální plán

arXiv:2504.16563 [INFERRED][4,5]:
- Root cause selhání: "lack of clear global goals" → agenti uvíznou v lokálních větvích
- Fix: **průběžně aktualizovaný** globální plán (ne statický upfront plán)
- +12.22% na LegalAgentBench

**Aplikace:** `state.md` by se měl aktualizovat po KAŽDÉM kroku agenta, ne jen při checkpointu.

#### B3. SA varování jako proxy pro architektonické zdraví

arXiv:2406.17354v2 [VERIFIED][8]:
- Korelace FindBugs Bloaters → Cyclic Dependency: ρ = 0.511
- **33.79% SA varování nikdy nekoreluje s žádným arch. smell** → filtrovatelný šum
- SA varování jako levný triage proxy pro architektonické rizikové zóny

### C. Token ekonomika vertikálního škálování

#### C1. Skill verbosity — 60% obsahu je odpad

SkillReducer (arXiv:2603.29919) [VERIFIED][1]:

| Metrika | Hodnota |
|---------|---------|
| Non-actionable obsah v skills | 60%+ |
| Token redukce po kompresi | 75% (359K → 84K) |
| Kvalita po kompresi | **LEPŠÍ** (0.742 vs 0.722, p=0.002) |
| Reference files per 100 skills | 1.67M tokenů (505 souborů) |
| Cross-file deduplikace | 29% úspora |

**Less-is-more efekt:** Komprimované skills jsou LEPŠÍ než originály. Méně kontextu = lepší fokus.

#### C2. Hierarchie násobí cenu 26-77×

Capgemini analýza [VERIFIED][8,9]:

| Konfigurace | Denní cena (GPT-4o) | Input token multiplier |
|-------------|---------------------|----------------------|
| Single-agent | $0.41 | 1× (13 tokenů) |
| Multi-agent | $10.54 | 77× (1,005 tokenů) |

Příčina: message history se propaguje přes úrovně, kontext roste multiplikativně.

#### C3. Context Rot — delší kontext = horší výstup

Chroma research [VERIFIED][11,12]:
- VŠECH 18 testovaných modelů degraduje s delším kontextem
- Claude vykazuje **největší gap** mezi focused (~300 tokenů) a full context (~113K)
- Již 1 distractor dokument snižuje výkon; 4 distractory ho kompoundují
- Shuffled haystacks > logicky strukturované [VERIFIED][13] — pozor na over-organization kontextu

#### C4. Tokenová kalkulace pro vertikální škálování

Na základě empirických dat odhaduji tokeny per úroveň:

| Úroveň | Vstup (čtení) | Analýza (LLM) | Celkem per level |
|---------|--------------|---------------|-------------------|
| **Mikro** (řádky, funkce) | ~500-2K tokenů (diff/snippet) | ~1-3K tokenů | **~2-5K** |
| **Mezo** (modul, API kontrakt) | ~3-10K (dependency map, imports) | ~3-5K | **~6-15K** |
| **Makro** (projekt, architektura) | ~5-20K (scout output, ADRs) | ~5-10K | **~10-30K** |
| **Cross-level kontrola** | ~2-5K (summaries z úrovní) | ~3-5K | **~5-10K** |
| **Celkem 3-level scan** | | | **~23-60K tokenů** |

S Sonnet 4.6 pricing ($3/$15 per M input/output):
- Light scan (jen mikro+mezo): ~$0.03-0.05
- Full scan (3 úrovně + cross-level): ~$0.08-0.20
- Deep scan (3 úrovně + 2 critic passes): ~$0.15-0.40

---

## Implementační varianty

### Varianta A: Lightweight — Hierarchický scout output

**Princip:** Neměnit orchestraci, jen restrukturovat výstup `/scout` na 3 úrovně.

**Co se změní:**
- Scout output formát: `project architecture → affected modules → specific files/lines`
- `state.md` obsahuje abstraction level tag per subtask
- Žádní noví agenti, žádné nové skills

**Implementace:**
```
Scout output format (nový):
## Level 1: Project Architecture
- Monorepo, 3 packages: core, api, web
- Build: turborepo, shared tsconfig

## Level 2: Affected Modules
- api/src/auth/ — session management (5 files)
- core/src/tokens/ — JWT validation (2 files)
- Dependency: auth → tokens (tight coupling)

## Level 3: Specific Scope
- auth/middleware.ts:45 — session check
- tokens/validate.ts:12-30 — expiry logic
```

**Tokenový dopad:**
- Zvýšení scout output: +2-5K tokenů (hierarchická struktura vs flat list)
- Snížení celkového spotřeby: -10-20% (worker agents dostanou cílenější kontext → méně retries)
- **Net: neutrální až mírně pozitivní**

**Effort:** Low. 1 den implementace (úprava scout SKILL.md).

**Rizika:** Žádná — je to jen lepší formátování existujícího výstupu.

**Doporučení:** ✅ Implementovat ihned jako základ pro varianty B a C.

---

### Varianta B: Medium — `/telescope` skill

**Princip:** Nový skill pro explicitní 3-level analýzu s cross-level konzistencí.

**Workflow:**
```
1. MIKRO scan
   - Ruff/lint na changed files → code-level issues
   - Diff analysis → co se mění a proč

2. MEZO scan
   - Import/dependency analysis → affected modules
   - API contract check → mění se interface?
   - Test coverage na affected modules

3. MAKRO scan
   - Scout-level architecture check
   - ADR/decisions.md konzistence
   - Cross-module dependency impact

4. CROSS-LEVEL SYNTHESIS
   - Mikro findings × Mezo contracts → konzistentní?
   - Mezo changes × Makro architecture → narušení?
   - Bottleneck identification → která úroveň limituje celek?
```

**Agent design (HexMachina-inspired):**
- 3 agenti: Mikro-Analyst (Haiku), Mezo-Analyst (Sonnet), Makro-Analyst (Sonnet)
- Paralelní běh → synthesis v lead agentovi
- Cross-level check jako 4. krok po merge

**Tokenový odhad:**

| Krok | Model | Tokeny | Cena |
|------|-------|--------|------|
| Mikro scan | Haiku | ~5K | ~$0.005 |
| Mezo scan | Sonnet | ~15K | ~$0.05 |
| Makro scan | Sonnet | ~25K | ~$0.08 |
| Cross-level synthesis | Sonnet | ~10K | ~$0.03 |
| **Celkem** | | **~55K** | **~$0.17** |

S 3 paralelními agenty: wall time ~2-3 min.

**Kdy spouštět:**
- Po orchestrate PŘED worker assignmentem (preventivní)
- Jako diagnostika při critic FAIL (reaktivní)
- Na vyžádání uživatelem

**Output formát:**
```markdown
## Vertical Consistency Report

### Health per Level
| Level | Status | Issues | Risk |
|-------|--------|--------|------|
| Mikro | ✅ clean | 0 lint | low |
| Mezo | ⚠️ warning | 2 contract changes | medium |
| Makro | ❌ conflict | ADR-007 violated | high |

### Cross-Level Findings
- Mikro fix (auth/middleware.ts:45) changes session API →
  breaks Mezo contract (auth module exports) →
  violates Makro decision (ADR-007: stateless auth)

### Bottleneck: MEZO level
- Module coupling between auth↔tokens is the weakest link
- Recommendation: decouple before proceeding
```

**Effort:** Medium. 3-5 dní (nový skill + 3 agent prompts + output template).

**Rizika:**
- Makro scan vyžaduje existující ADRs/decisions.md → bez nich je degradovaný
- Mezo scan závisí na kvalitě dependency analysis → Python/JS OK, jiné jazyky horší

**Doporučení:** ✅ Implementovat po Variantě A. Hlavní hodnota systému.

---

### Varianta C: Full — Multi-scale orchestrace

**Princip:** Modifikovat `/orchestrate` aby dekomponoval úkoly na 3 úrovních a vynucoval vertikální konzistenci.

**Architektura:**

```
orchestrate (coordinator)
├── Phase 1: DISCOVER (telescope-lite)
│   ├── mikro-scout (Haiku) → code-level mapping
│   ├── mezo-scout (Haiku) → module-level mapping
│   └── makro-scout (Sonnet) → architecture-level mapping
│
├── Phase 2: PLAN (cross-level)
│   ├── Merge 3 scout outputs
│   ├── Identify cross-level constraints
│   ├── Tag each subtask with abstraction level
│   └── Validate: effects(level N) don't violate constraints(level N+1)
│
├── Phase 3: EXECUTE (level-aware workers)
│   ├── Worker agents get level-tagged context
│   ├── Mikro workers: jen relevant snippet + mezo summary
│   ├── Mezo workers: module map + makro constraints
│   └── Makro workers: full architecture context
│
└── Phase 4: VERIFY (cross-level critic)
    ├── Per-level verification (existující critic)
    └── Cross-level consistency check (nový)
```

**Tokenový odhad:**

| Fáze | Agenti | Model | Tokeny | Cena |
|------|--------|-------|--------|------|
| Discover (3 scouts) | 3 parallel | Haiku+Sonnet | ~40K | ~$0.10 |
| Plan (cross-level) | 1 lead | Sonnet | ~20K | ~$0.06 |
| Execute (workers) | 2-4 | Sonnet | ~100-200K | ~$0.30-0.60 |
| Verify (critic) | 1-2 | Sonnet | ~30-50K | ~$0.10-0.15 |
| **Celkem** | 7-10 | | **~190-310K** | **~$0.56-0.91** |

vs současný orchestrate (bez vertical awareness): ~150-250K tokenů, ~$0.45-0.75

**Overhead:** +25-40% tokenů, +25-40% ceny. Ale:
- Méně retries (cross-level check zastaví nekonzistentní plány dřív)
- Lepší worker context (level-tagged → méně kontextu per worker → méně context rot)
- Net impact po optimalizaci: **+10-20% ceny za výrazně vyšší kvalitu**

**Effort:** High. 1-2 týdny (refactor orchestrate + nové fáze + cross-level critic).

**Rizika:**
- Komplexita orchestrace roste → víc míst pro selhání
- Discovery fáze přidává latenci (~2 min navíc)
- Vyžaduje dobře definované architektonické artefakty v projektu

**Doporučení:** ⚠️ Implementovat až po validaci Variant A+B v praxi.

---

## Srovnání variant

| Dimenze | A: Hierarchický scout | B: /telescope | C: Multi-scale orchestrace |
|---------|-----------------------|---------------|---------------------------|
| **Effort** | 1 den | 3-5 dní | 1-2 týdny |
| **Token overhead** | ±0% | +~55K per scan (~$0.17) | +25-40% per task |
| **Latence** | 0 | +2-3 min | +2-5 min |
| **Hodnota** | Lepší kontext pro workery | Explicitní cross-level check | Plná vertikální konzistence |
| **Prerequisity** | Žádné | Varianta A | Varianta A + B |
| **Riziko** | Minimální | Střední (závisí na ADRs) | Vysoké (komplexita) |
| **ROI** | Okamžitý | Střední | Dlouhodobý |

### Doporučená implementační cesta

```
Týden 1: Varianta A (hierarchický scout output)
  → Validace na 2-3 reálných úkolech v NG-ROBOT

Týden 2-3: Varianta B (/telescope skill)
  → Validace jako diagnostika při critic FAIL
  → Měření: kolik false-positive issues zachytí?

Týden 4+: Varianta C (pokud B prokáže hodnotu)
  → Inkrementální — nejdřív jen discovery fáze do orchestrate
  → Cross-level critic jako opt-in (ne default)
```

---

## Disagreements & Open Questions

1. **xMemory 48% savings** [SINGLE-SOURCE][7] — chybí kontrolovaný benchmark, jen product marketing
2. **HexMachina 3-agent optimum** [VERIFIED][3] — testováno na game-playing, ne na code tasks. Transferabilita je [INFERRED]
3. **Context Rot shuffled > structured** [VERIFIED][13] — kontraintuitivní, vyžaduje ověření na code-specific tasks
4. **GoalAct continuous plan update** [INFERRED][4,5] — mechanismus aktualizace (kdy a jak) nebyl přístupný (jen abstrakt)
5. **Tokenový odhad per úroveň** je vlastní extrapolace z empirických dat — reálné náklady se mohou lišit ±50%

---

## Evidence Table

| # | Zdroj | URL | Klíčový claim | Typ | Confidence |
|---|-------|-----|---------------|-----|------------|
| 1 | SkillReducer (2603.29919) | https://arxiv.org/html/2603.29919 | 75% token redukce, quality +2.8% (p=0.002) | empirical | high |
| 2 | HCAG (2603.20299) | https://arxiv.org/html/2603.20299 | Hierarchická abstrakce cost-optimální vs flat RAG | theoretical+empirical | high |
| 3 | HexMachina (2506.04651v2) | https://arxiv.org/html/2506.04651v2 | 3 agenti > 5 agentů; phase separation kritická | empirical | high |
| 4 | GoalAct (2504.16563) | https://arxiv.org/abs/2504.16563 | Continuously updated global plan +12.22% | empirical | medium |
| 5 | HMAS Taxonomy (2508.12683) | https://arxiv.org/html/2508.12683 | 5-axis framework, temporal layering klíčová | taxonomy | high |
| 6 | HTN+LLM (2511.18165) | https://arxiv.org/html/2511.18165 | Pure LLM HP validity 1%; hybrid needed | empirical | high |
| 7 | xMemory | https://venturebeat.com/orchestration/how-xmemory-cuts-token-costs-and-context-bloat-in-ai-agents | 48% token savings via hierarchical memory | product benchmark | medium |
| 8 | Capgemini | https://www.capgemini.com/be-en/insights/expert-perspectives/the-efficient-use-of-tokens-for-multi-agent-systems/ | Multi-agent 26× dražší ($10.54 vs $0.41/den) | cost analysis | high |
| 9 | Capgemini | (same) | Input tokens 77× multiplier single→multi | cost analysis | medium |
| 10 | Arch Smells + SA (2406.17354v2) | https://arxiv.org/html/2406.17354v2 | SA warnings korelují s arch. smells (ρ=0.511) | empirical, 103 projects | high |
| 11 | Context Rot (Chroma) | https://research.trychroma.com/context-rot | All 18 models degrade with longer context | benchmark | high |
| 12 | Context Rot | (same) | Even 1 distractor degrades; 4 compound | controlled experiment | high |
| 13 | Context Rot | (same) | Shuffled > logically structured haystacks | counterintuitive finding | high |

---

## Sources

1. Gao et al., "SkillReducer: Optimizing LLM Agent Skills for Token Efficiency," arXiv:2603.29919 — https://arxiv.org/html/2603.29919
2. HCAG, "Hierarchical Code/Architecture-guided Agent Generation," arXiv:2603.20299 — https://arxiv.org/html/2603.20299
3. HexMachina, "Agents of Change: Self-Evolving LLM Agents for Strategic Planning," arXiv:2506.04651v2 — https://arxiv.org/html/2506.04651v2
4. GoalAct, "Enhancing LLM-Based Agents via Global Planning and Hierarchical Execution," arXiv:2504.16563 — https://arxiv.org/abs/2504.16563
5. HMAS Taxonomy, arXiv:2508.12683 — https://arxiv.org/html/2508.12683
6. HTN+LLM Framework, arXiv:2511.18165 — https://arxiv.org/html/2511.18165
7. xMemory — https://venturebeat.com/orchestration/how-xmemory-cuts-token-costs-and-context-bloat-in-ai-agents
8. Capgemini Multi-Agent Analysis — https://www.capgemini.com/be-en/insights/expert-perspectives/the-efficient-use-of-tokens-for-multi-agent-systems/
9. Architectural Smells + Static Analysis, arXiv:2406.17354v2 — https://arxiv.org/html/2406.17354v2
10. Context Rot, Chroma Research — https://research.trychroma.com/context-rot
11. Governance as Code, Agoda Engineering — https://medium.com/agoda-engineering/governance-as-code-an-innovative-approach-to-software-architecture-verification-d93f95443662
12. HiAgent, arXiv:2408.09559 — https://arxiv.org/abs/2408.09559

## Coverage Status

- **[VERIFIED]:** 9 claimů přímo ověřených ze zdrojů
- **[INFERRED]:** 3 claimy odvozené z více zdrojů
- **[SINGLE-SOURCE]:** 1 claim (xMemory 48%)
- **[UNVERIFIED]:** 0
