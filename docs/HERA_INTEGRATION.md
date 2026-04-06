# HERA Integration Plan — Experience as Infrastructure

**Source:** arXiv:2604.00901v2 (Virginia Tech, Li & Ramakrishnan)
**Date:** 2026-04-06
**Status:** Implementation plan

---

## Executive Summary

HERA (Hindsight Experience-driven Retrieval Augmentation) dosahuje +38.69% nad SOTA na RAG benchmarcích tím, ze trati kazdy failure jako infrastrukturu pro budouci queries. Tri klicove mechanismy:

1. **Experience Library** — uloziste (query_type, insight, utility_score) tuplu, rankovane podle empiricke uspesnosti
2. **Role-aware Prompt Evolution (RoPE)** — identifikace selhavajiciho agenta, generovani prompt variant, replay trajektorie, extrakce operational rules + behavioral principles
3. **Topology Evolution** — emergentni reorganizace agent grafu (pruning redundantnich agentu, augmentace novych)

STOPA je na ~45% ready: ma traces, learnings, curriculum-driven iteration. Chybi: failure attribution, topology adaptation, systematic hindsight replay.

---

## Gap Analysis: STOPA vs HERA

### Co STOPA uz ma (validace)

| HERA Concept | STOPA Equivalent | Kde |
|---|---|---|
| Experience Library (c, z, u) | learnings/ s confidence, impact_score, uses | `.claude/memory/learnings/` |
| Utility ranking | Time-weighted relevance scoring | `rules/memory-files.md` |
| Operational rules vs Behavioral principles | learnings (konkretni) vs critical-patterns (obecne) | graduation trigger |
| Trace logging | `.traces/` + `.harness/traces/` | autoloop, self-evolve, harness, eval |
| Curriculum-driven generation | self-evolve Curriculum Decision | `skills/self-evolve/SKILL.md:99-125` |
| Agent fault detection (basic) | Circuit breakers (3x loop, 2x critic fail) | `skills/orchestrate/SKILL.md:566-580` |
| Cost optimization | Progressive skill withdrawal, budget tiers | `rules/skill-files.md` |
| Consolidation (ADD/MERGE/PRUNE) | Learning admission hook + /evolve pruning | `learning-admission.py`, `/evolve` |

### Co STOPA nema (gapy)

| Gap | HERA Mechanism | Impact | Effort |
|---|---|---|---|
| **G1: Failure Classification** | 7 query types × 3 complexity = typed failures | Bez klasifikace nelze kumulovat zkusenosti per-type | Medium |
| **G2: Agent-Level Fault Attribution** | Orchestrator identifikuje KTERY agent selhal | Bez atribuce nelze cilene fixovat agenty | Medium |
| **G3: Prompt Variant Generation + Replay** | 3 osy (efficiency, thoroughness, risk) × replay | Nejsilnejsi single component (-30% bez nej) | High |
| **G4: Topology Mutation** | Replace/Augment selhavajicich agentu | Emergentni pruning = system se zlevnuje | High |
| **G5: GRPO-style Group Rollouts** | G kandidatnich topologii → mixed outcomes → reflect | Vyzaduje paralelni exekuci + porovnani | Very High |
| **G6: Failure Trajectory Storage** | Cely rozhodovaci retezec ktery vedl k selhani | Bez trajektorie nelze replay | Medium |
| **G7: Cross-Task Failure Correlation** | "Agent X selhava na logic errors ve 15%" | Prediktivni agent selection | High |

### Prioritizace (Impact × Feasibility)

```
          High Impact
              |
     G3 ●    |    ● G2
              |
   G5 ●      |      ● G1
              |
     G4 ●    |    ● G6
              |
              ● G7
          Low Impact
    Hard ─────┼───── Easy
         Feasibility
```

**Sekvence:** G1 → G6 → G2 → G3 → G4 → G7 → G5

Zduvodneni: G1 (failure classification) je prerekvizita pro vsechno ostatni. G6 (trajectory storage) umoznuje replay. G2 (attribution) umoznuje cileny fix. G3 (prompt evolution) je nejsilnejsi single component. G5 (GRPO rollouts) je nice-to-have ale extremne drahy v tokenech.

---

## Implementation Plan

### Phase 1: Failure Infrastructure (G1 + G6)

**Cil:** Kazdy failure ma typ, severity a trajektorii.

#### 1a. Failure Classification Schema

Rozsireni learnings YAML frontmatter:

```yaml
# Novy field v learnings/
failure_class: logic | syntax | timeout | resource | integration | assumption | coordination
failure_agent: orchestrate | scout | critic | ...  # ktery agent/skill selhal
failure_trajectory:
  - step: "orchestrate assigned tier:standard"
  - step: "scout found 12 files"
  - step: "agent-1 edited utils.py"
  - step: "critic FAIL: missing import (F401)"
  - root_cause: "ruff autofix removed used import"
```

**failure_class taxonomie** (inspirovano HERA query types, adaptovano na code tasks):

| Class | Popis | Priklady |
|---|---|---|
| `logic` | Spatny vystup, test fail, wrong behavior | Spatna podminka, chybejici edge case |
| `syntax` | Parse/compile error, import error | Missing import, typo, invalid YAML |
| `timeout` | Rate limit, API timeout, 503 | External service unavailable |
| `resource` | ENOENT, EACCES, OOM, disk full | File not found, permission denied |
| `integration` | Component mismatch, API contract broken | Wrong function signature, schema drift |
| `assumption` | Predpoklad o kodu/prostredi byl spatny | "Myslel jsem ze funkce vraci list" |
| `coordination` | Agent/skill interference, wrong delegation | Dva agenti edituji stejny soubor |

#### 1b. Failure Trajectory Capture

Rozsireni `state.md` o failure log:

```yaml
# Novy section v state.md (za subtasks)
## Failure Log
- id: F001
  timestamp: 2026-04-06T14:30:00
  task: "Edit auth middleware"
  failure_class: logic
  failure_agent: agent-2
  trajectory:
    - "orchestrate: tier=standard, 3 agents"
    - "scout: found auth.py, middleware.py, tests/"
    - "agent-2: edited middleware.py line 45"
    - "critic: FAIL — session token not invalidated on logout"
  root_cause: "Agent assumed stateless auth, but app uses sessions"
  resolution: "Added session.invalidate() call"
  reflexion: "Priste precist existujici testy PRED editaci"
```

**Implementace:**
- Orchestrate skill: po kazdem FAIL subtasku zapise failure entry do state.md
- Critic skill: pri FAIL verdiktu vygeneruje failure_class + root_cause
- Format: YAML v state.md (max 10 entries, pak archivace do failure-archive.md)

#### 1c. Zmeny v existujicich souborech

| Soubor | Zmena |
|---|---|
| `rules/memory-files.md` | Pridat failure_class, failure_agent, failure_trajectory do learnings schema |
| `skills/orchestrate/SKILL.md` | Phase 5 (Execute): pri subtask FAIL zapsat failure entry |
| `skills/critic/SKILL.md` | Judge phase: pri FAIL vygenerovat failure_class + root_cause |
| `skills/scribe/SKILL.md` | Pridat failure-aware learning template |

---

### Phase 2: Agent Fault Attribution (G2)

**Cil:** Orchestrator identifikuje KTERY agent zpusobil failure a provedl co spatne.

#### 2a. Attribution Mechanism

Po failure orchestrator provede **blame analysis** (inspirovano HERA Algorithm 5, Step 1):

```
Pro kazdy FAIL subtask:
1. Precti failure trajectory
2. Identifikuj "decision point" — kde se vysledek odchylil od ocekavani
3. Atribuuj: ktery agent udelal spatne rozhodnuti na decision point
4. Zapas do failure_agent pole
```

**Attribution heuristiky:**

| Signal | Attribution |
|---|---|
| Critic najde bug v kodu agenta | Agent ktery editoval soubor |
| Test selhava po editu | Agent ktery provedl edit |
| Scout nemel najit relevantni soubor | Scout |
| Spatny tier assignment | Orchestrator |
| Agent blocked — spatna dekompozice | Orchestrator |
| Dva agenti v konfliktu | Orchestrator (coordination failure) |

#### 2b. Per-Agent Failure Counters

Novy soubor `.claude/memory/agent-accountability.md`:

```markdown
## Agent Performance (rolling 30 days)

| Agent/Skill | Total Tasks | Failures | Failure Rate | Top Failure Class |
|---|---|---|---|---|
| orchestrate | 45 | 3 | 6.7% | coordination (2), assumption (1) |
| scout | 38 | 1 | 2.6% | integration (1) |
| agent-worker | 120 | 15 | 12.5% | logic (8), syntax (4), assumption (3) |
| critic | 52 | 0 | 0% | — |
```

**Pouziti:** Orchestrator pred assignmentem konzultuje accountability tabulku:
- Agent s >20% failure rate na danem failure_class → eskalace na silnejsi model
- Agent s 0% failures → preferovany pro kriticke subtasky

#### 2c. Zmeny v existujicich souborech

| Soubor | Zmena |
|---|---|
| `skills/orchestrate/SKILL.md` | Phase 5: blame analysis po FAIL; Phase 3: konzultace accountability pred assignmentem |
| `skills/eval/SKILL.md` | Novy `--failures` mode pro agent accountability report |
| `.claude/memory/` | Novy soubor `agent-accountability.md` |

---

### Phase 3: Experience Library (upgrady G1 → HERA-style)

**Cil:** Learnings se chovaji jako HERA Experience Library — rankovane podle empiricke uspesnosti, s consolidation operacemi.

#### 3a. Query Characterization

HERA klasifikuje queries do 7 typu. STOPA ekvivalent — klasifikace tasku:

```yaml
task_class: single_edit | multi_file | refactor | bug_fix | feature | research | pipeline
complexity: low | medium | high
```

Pridano do learnings jako kontextova metadata:

```yaml
# Existujici fields
failure_class: logic
failure_agent: agent-2
# Novy field
task_context:
  task_class: multi_file
  complexity: medium
  tier: standard
```

#### 3b. Utility Score = uses + success_rate

Rozsireni `uses` counteru o success tracking:

```yaml
uses: 12          # kolikrat retrieven
successful_uses: 9  # kolikrat vedl k uspechu
utility: 0.75     # = successful_uses / uses
```

**HERA utility update rule:** Po kazdem pouziti learningu:
- Pokud task PASS: `successful_uses += 1`
- Vzdy: `uses += 1`
- `utility = successful_uses / uses`

#### 3c. Consolidation Operations

Implementace HERA Algorithm 3 (ADD/MERGE/PRUNE/KEEP) do `/scribe` a `/evolve`:

| Operace | Trigger | Akce |
|---|---|---|
| **ADD** | Novy learning, zadny match v existujicich | Zapsat novy soubor |
| **MERGE** | Novy learning je komplementarni s existujicim (stejny component + compatible strategy) | Aktualizovat existujici soubor, pridat related: link |
| **PRUNE** | Novy learning je v konfliktu s existujicim A existujici ma nizkou utility | Supersedes: existujici, smazat z retrieval |
| **KEEP** | Novy learning neprinasi nic noveho | Nezapisovat |

**Zmena v `/scribe`:** Pred zapisem noveho learningu:
1. Grep existujici learnings s podobnym component + tags
2. Pro kazdy match: klasifikuj relaci (ADD/MERGE/PRUNE/KEEP)
3. Proved odpovídající operaci

Toto je evoluce existujiciho `learning-admission.py` hooku.

---

### Phase 4: Role-aware Prompt Evolution (G3)

**Cil:** Selhavajici agenti dostavaji cilene vylepseni promptu na zaklade failure analysis.

#### 4a. Adaptace RoPE pro STOPA

HERA RoPE pracuje s fixnimi agent prompty. STOPA ekvivalent: **skill prompty** (SKILL.md body) a **orchestrator instrukce pro sub-agenty**.

**Process:**

```
1. Orchestrator identifikuje selhavajiciho agenta (Phase 2 attribution)
2. Nacte posledni 3 failure trajectories pro dany agent + failure_class
3. Vygeneruje 3 prompt varianty podél os:
   - EFFICIENCY: "Minimalizuj kroky, preferuj prime reseni"
   - THOROUGHNESS: "Zkontroluj vsechny edge cases pred editem"
   - RISK_SENSITIVITY: "Pri pochybnostech se ptej, nedelej predpoklady"
4. Pro kazdou variantu: mental replay (ne skutecna exekuce — prilis drahe)
   - "Kdyby agent mel tento prompt, jak by se zachoval v trajectory X?"
5. Extrakce:
   - Operational rules: "Pred editaci auth kodu precti vsechny existujici testy"
   - Behavioral principles: "Nikdy nepredpokladej stateless auth bez overeni"
6. Consolidace do learningu s failure_class + failure_agent context
```

**Dulezity rozdil od HERA:** HERA provadi skutecny trajectory replay (drahy — N variant × full execution). STOPA adaptace pouziva **mental replay** (LLM simuluje co by se stalo) — 10x levnejsi, mensi presnost ale dostatecna pro skill-level improvement.

Pro kriticke failure (2+ opakovani stejneho failure_class): upgrade na plny replay jako v `/self-evolve`.

#### 4b. Implementace

**Novy skill `/learn-from-failure`** (nebo integrace do `/scribe`):

```
Trigger: Po 2+ failures stejneho failure_class na stejnem agent
Input: failure trajectories z state.md
Output: operational rules + behavioral principles → learnings/

Process:
1. Nacti failure trajectories (max 5 poslednich)
2. Identifikuj spolecne vzory (kde se trajektorie rozchazi od uspechu?)
3. Generuj 3 prompt varianty (efficiency/thoroughness/risk)
4. Mental replay: "S timto promptem, jak by se agent zachoval?"
5. Extrahuj operational rules (konkretni instrukce) + behavioral principles (obecne)
6. Zapas jako learning s failure_class + failure_agent + task_context
7. Pokud behavioral principle je dostatecne obecny → kandidat na critical-patterns
```

#### 4c. Zmeny v existujicich souborech

| Soubor | Zmena |
|---|---|
| `skills/orchestrate/SKILL.md` | Phase 6 (Learn): trigger /learn-from-failure pri 2+ same-class failures |
| `skills/self-evolve/SKILL.md` | Curriculum Decision: konzultovat failure history pred generovanim cases |
| Novy skill | `skills/learn-from-failure/SKILL.md` |

---

### Phase 5: Topology Evolution (G4)

**Cil:** Agent graf se reorganizuje na zaklade zkusenosti — pruning neefektivnich, augmentace novych.

#### 5a. Adaptace pro STOPA

HERA topology evolution pracuje s fixnim agent poolem. STOPA ekvivalent: **skill selection + tier assignment + wave structure**.

**Topology = (tier, skills, wave_structure, model_assignment)**

Evoluce:
- **Prune:** Skill/agent ktery opakovaně selhava na danem task_class → vynechat z budoucich assignments
- **Replace:** Selhavajici agent → nahradit jinym (nebo silnejsim modelem)
- **Augment:** Pridat verification step po agentovi s vysokym failure rate

#### 5b. Emergence Metrics

Adaptace HERA graph metrics pro STOPA:

| Metrika | STOPA Ekvivalent | Vyznam |
|---|---|---|
| \|V\| (agent count) | Pocet sub-agentu v orchestraci | Sirka kolaborace |
| Node efficiency | Task success / agent count | Per-agent uzitecnost |
| Self-loops | Agent retry count | Redundance |
| Cycles | Critic → fix → critic loops | Iterativni reasoning |
| Diameter | Max hloubka delegace | Reasoning depth |
| H_trans (transition entropy) | Variabilita agent→agent handoffs | Strukturovanost vs flexibilita |

**Tracking:** Novy section v `.claude/memory/topology-evolution.md`:

```markdown
## Topology Snapshots (per orchestration run)

| Date | Task Class | Tier | Agents | Node Eff | Retries | Critic Loops | Result |
|---|---|---|---|---|---|---|---|
| 2026-04-06 | multi_file | standard | 3 | 0.67 | 1 | 1 | PASS |
| 2026-04-06 | bug_fix | light | 1 | 1.0 | 0 | 1 | PASS |
| 2026-04-05 | refactor | deep | 5 | 0.40 | 3 | 2 | FAIL |
```

Po 20+ snapshotech: `/eval --topology` analyzuje trendy a navrhne defaultni topologie per task_class.

#### 5c. Zmeny v existujicich souborech

| Soubor | Zmena |
|---|---|
| `skills/orchestrate/SKILL.md` | Phase 3: konzultovat topology-evolution pred tier assignment; Phase 6: zapsat snapshot |
| `skills/eval/SKILL.md` | Novy `--topology` mode |
| `.claude/memory/` | Novy `topology-evolution.md` |

---

### Phase 6: GRPO-lite (G5, optional)

**Cil:** Porovnani vicerych topologii na stejnem tasku.

**HERA approach:** Sampluji G kandidatnich topologii, provede vsechny, porovna.

**STOPA adaptace (budget-aware):**
- NENI realisticke provadet N plnych orchestraci (kazda stoji $1-5)
- Alternativa: **Mental GRPO** — orchestrator vygeneruje 3 kandidatni plany, mentalně porovna, vybere nejlepsi
- Pri kritickem failu: upgrade na skutecny A/B (2 plany, provedeni obou, porovnani)

**Implementace:** Integrace do orchestrate Phase 3 (Decomposition):

```
1. Vygeneruj 3 kandidatni plany (ruzne tier/agent/wave combinations)
2. Pro kazdy plan: ohodnot pravdepodobnost uspechu na zaklade:
   - agent-accountability data (failure rates)
   - topology-evolution data (similar past topologies)
   - task complexity vs tier match
3. Vyber plan s nejvyssi expected utility
4. (Optional, pri critical task) Proved top-2 plany paralelne, porovnej
```

**Effort:** Very High — implementovat az po Phase 1-5 jsou stabilni.

---

## Implementation Timeline

| Phase | Obsah | Dotcene soubory | Effort | Prerekvizity |
|---|---|---|---|---|
| **1** | Failure Classification + Trajectory Storage | memory-files.md, orchestrate, critic, scribe | 1 session | — |
| **2** | Agent Fault Attribution | orchestrate, eval, nova memory | 1 session | Phase 1 |
| **3** | Experience Library upgrade | scribe, evolve, learning-admission.py | 1 session | Phase 1 |
| **4** | Prompt Evolution (RoPE-lite) | novy skill learn-from-failure | 1-2 sessions | Phase 1+2 |
| **5** | Topology Evolution tracking | orchestrate, eval, nova memory | 1 session | Phase 2 |
| **6** | GRPO-lite (optional) | orchestrate | 1 session | Phase 1-5 |

**Celkem:** 5-7 sessions pro Phase 1-5, Phase 6 optional.

---

## Klicove designove rozhodnuti

### 1. Mental Replay vs Full Replay

HERA provadi plny trajectory replay (Algorithm 5). V STOPA kontextu je to prilis drahe:
- Plny replay 1 orchestrace = $2-5 v tokenech
- 3 varianty × replay = $6-15 za jednu failure analysis

**Rozhodnuti:** Mental replay (LLM simuluje) jako default, plny replay jen pri:
- 3+ opakovani stejneho failure_class
- Critical severity
- Explicitni `/learn-from-failure --full-replay`

### 2. Inline vs Dedicated Skill

RoPE muze byt:
a) Inline v orchestrate (Phase 6 Learn) — jednodussi, mene flexible
b) Dedicated skill `/learn-from-failure` — reusable, testovatelny, ale dalsi skill

**Rozhodnuti:** Dedicated skill. Duvody:
- Testovatelny pres /self-evolve
- Volatelny i mimo orchestrate (napr. po rucnim debuggingu)
- Jasny output-contract: `"failure learnings → YAML → learnings/"`

### 3. Storage: state.md vs dedicated failure log

Failure trajectories mohou byt:
a) V state.md (existujici soubor, riziko bloat)
b) V `.claude/memory/failures/` (dedicated, grep-friendly)

**Rozhodnuti:** Dedicated `.claude/memory/failures/` directory. Duvody:
- state.md se preplnuje (uz ma subtasks, waves, agents)
- Failures maji vlastni lifecycle (analysis → learning → archive)
- Grep-first retrieval per failure_class

### 4. Topology: emergentni vs designed

HERA topology emerguje z failures. STOPA muze:
a) Nechat emergovat (tracking + analysis)
b) Navrhovat explicitne per task_class

**Rozhodnuti:** Oba. Tracking od Phase 5, navrhy po 20+ datapointech.

---

## Metriky uspechu

| Metrika | Baseline (odhad) | Cil po Phase 5 |
|---|---|---|
| Opakujici se failure na stejnem failure_class | ~30% orchestraci | <10% |
| Prumerna failure rate per orchestrace | ~20% subtasku | <10% |
| Cas na root-cause identifikaci | Manual (minuty) | Automaticky s trajectory |
| Learning relevance (precision pri retrieval) | ~60% | >80% (diky task_context matching) |
| Agent selection accuracy | Rule-based | Data-informed (accountability table) |

---

## Rizika

| Riziko | Pravdepodobnost | Mitigace |
|---|---|---|
| Failure classification je prilis hruba | Stredni | Zacit se 7 tridy, rozsirir az po data |
| Mental replay je nepresnny | Vysoka | Plny replay pro kriticke failures |
| Memory bloat (failures + trajectories) | Stredni | Max 50 failure records, pak archivace |
| Attribution je spatna (blame wrong agent) | Stredni | Heuristiky + human override |
| Token overhead pro failure analysis | Nizka | Haiku pro klasifikaci, Sonnet pro analysis |

---

## Appendix A: HERA Ablation Results (reference)

| Component Removed | Impact |
|---|---|
| Without Experience Library | -6% to -15% |
| Without Prompt Evolution | Up to -30% (2WikiQA) |
| Full HERA | Non-additive synergy |

Prompt Evolution je nejsilnejsi single component. Experience Library zesiluje jeho efekt.
V STOPA kontextu: Phase 4 (RoPE-lite) je nejdulezitejsi, ale vyzaduje Phase 1-2 jako zaklad.

## Appendix B: HERA vs STOPA Terminology Mapping

| HERA Term | STOPA Equivalent |
|---|---|
| Orchestrator | `/orchestrate` skill |
| Execution Agent N_i | Sub-agent (haiku/sonnet worker) |
| Experience Library E | `learnings/` + `critical-patterns.md` |
| Query type c | `task_class` + `complexity` |
| Insight z | Learning content (YAML body) |
| Utility u | `utility = successful_uses / uses` |
| RoPE | `/learn-from-failure` skill |
| Operational rules | Learnings (concrete, per-failure) |
| Behavioral principles | Critical patterns (general, cross-failure) |
| Topology Gamma | (tier, skills, wave_structure, model_assignment) |
| GRPO group rollout | Mental GRPO (plan comparison without execution) |
| Trajectory tau | Failure trajectory in `failures/` |

## Appendix C: New Files Created

| File | Purpose | Phase |
|---|---|---|
| `.claude/memory/failures/` | Per-failure YAML records | Phase 1 |
| `.claude/memory/agent-accountability.md` | Per-agent failure counters | Phase 2 |
| `.claude/memory/topology-evolution.md` | Per-orchestration topology snapshots | Phase 5 |
| `.claude/skills/learn-from-failure/SKILL.md` | Dedicated failure analysis skill | Phase 4 |
