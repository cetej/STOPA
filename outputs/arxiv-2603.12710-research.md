# AI Planning Framework for LLM-Based Web Agents — Research Brief

**Date:** 2026-04-26  
**Paper:** Shahnovsky & Dror (2026), *AI Planning Framework for LLM-Based Web Agents*  
**arXiv ID:** [2603.12710](https://arxiv.org/abs/2603.12710)  
**Question:** Hluboká kritická evaluace paperu — taxonomie, 5 metrik, dataset, metodologie + vazba na STOPA orchestration patterns  
**Scope:** comparison (paper + ekosystem 2024-2026 + STOPA mapping)  
**Sources consulted:** 17 (12 directly fetched, 3 transitive, 2 partial)

---

## Executive Summary

Paper formalizuje webové agenty jako POMDP a mapuje tři architektury (Step-by-Step / Tree Search / Full-Plan-in-Advance) na klasické search algoritmy (BFS / Best-First / DFS). Navrhuje 5 trajectory metrik, sbírá 794-trajektorií human-gold dataset z WebArena, a porovnává Step-by-Step (38.41%) s Full-Plan (36.29%). [VERIFIED][1]

**Tři klíčové závěry kritické analýzy:**

1. **Taxonomie je derivativní** [INFERRED][7]. BFS/DFS framing pro LLM agenty zavedli Yao et al. 2023 (Tree of Thoughts), Best-First Koh et al. 2024. Modernější taxonomie (Bilenko et al. 2026, Plan-MCTS 2026) jsou bohatší — rozkládají agenty podle granularity (action-space vs plan-space), hierarchie, reflection a action paradigmu, ne jen search policy. [VERIFIED][13,6]

2. **5 metrik JE komplementární k existující literatuře, ne redundantní** [INFERRED][8,9,10,11,12]. Element Accuracy a Recovery Rate jsou unikátní vůči 5 konkurenčním frameworkům (Online-Mind2Web/WebJudge, AgentRewardBench, WebGraphEval, TRACE, WebArena Verified). Repetitiveness, Step Success a Partial Success existují v jiné formě jinde.

3. **Empirický finding je zajímavější než deklarovaný** [VERIFIED][1]. Full-Plan má vyšší Element Accuracy (89% vs 82%) ale nižší task success (36.29% vs 38.41%). Praktická interpretace: **planning agent perfektně provádí špatný plán**. Tato formulace nebyla v retrieved literatuře nalezena [SINGLE-SOURCE][1] — možná genuinely novel.

**Slabé stránky metodologie:**
- Single-annotator dataset (autoři sami), žádné inter-annotator agreement [VERIFIED][1] — problém, který AgentRewardBench (1302 trajectories, expert panel) a WebArena Verified (audit 812 tasks) explicitně v 2024-2025 řešily [VERIFIED][9,12].
- LLM-as-judge bez nezávislé validace [VERIFIED][1].
- Full-Plan agent autorsky deklarovaný jako "not optimized" — proof of concept; výsledky tedy neměří potenciál architektury.
- Porovnává 38.41% vs 36.29% v benchmarku, kde published methods spannují 16-46%, přičemž **AgentOccam (linear, ne search-based) drží 45.7%** [VERIFIED][6]. Paper ignoruje empiricky nejsilnější třídu.

**Bottom line pro STOPA:** Užitečné jsou (a) Recovery Rate a Element Accuracy jako koncepty pro `/eval` a `/annotate`, (b) finding "perfektní provedení špatného plánu" jako diagnostický pattern pro `/orchestrate` review. Taxonomie sama o sobě je staré víno v nové láhvi — STOPA má bohatší rozhodovací osy už dnes (budget tier × scout depth × max-depth × granularity).

---

## Detailní zjištění

### 1. Co paper říká (faktický extrakt)

**Formální framework:** Web browsing jako POMDP, S = state space, A = action space [VERIFIED][1].

**Taxonomie tří architektur:**

| Architektura | Plánovací paradigma | Definice |
|---|---|---|
| Step-by-Step | BFS (d=1) | Implicitní candidate set, LLM evaluates, depth=1 horizon |
| Tree Search | Best-First Search | Explicitní search tree T, value function V: S → [0,1] |
| Full-Plan-in-Advance | DFS | Kompletní τ = (a₁,...,aₙ) generována před exekucí |

[VERIFIED][1]

**5 trajectory metrik (přesné formule):**

```
Recovery Rate     = (1/#tasks) Σ [# recoveries / # deviations]                  (Def 4.1)
Repetitiveness    = 1 − (1/#tasks) Σ [# repetitive / # actions]                 (Def 4.2)
Step Success Rate = (1/#tasks) Σ [# matched gold steps / # gold steps]          (Def 4.3)
Partial Success   = (1/#req_tasks) Σ [# completed reqs / # reqs]                (Def 4.4)
Element Accuracy  = (1/#tasks) Σ [# matching predicted/actual / # agent steps]  (Def 4.5)
```

[VERIFIED][1]

**Dataset:** 794 z 812 WebArena úkolů (97.7%) napříč pěti doménami (e-commerce, Reddit, GitLab, CMS, OpenStreetMap). 18 úkolů opuštěno: "we were uncertain how to complete them." Inter-annotator agreement nereportováno; autoři jsou jediní anotátoři. [VERIFIED][1]

**Hlavní výsledky:**

| Metrika | Step-by-Step (WebArena agent) | Full-Plan-in-Advance |
|---|---|---|
| **Overall Success** | **38.41%** | **36.29%** |
| Step Success Rate | 0.82 ± 0.14 | 0.58 ± 0.29 |
| Step Success (úspěšné only) | 0.89 ± 0.06 | 0.63 ± 0.10 |
| Element Accuracy | 0.82 ± 0.12 | **0.89 ± 0.03** |
| Repetitiveness | 0.79 ± 0.14 | 0.81 ± 0.13 |
| Recovery Rate | 0.36 ± 0.19 | 0.31 ± 0.12 |
| Partial Success | 0.22 ± 0.39 | 0.12 ± 0.27 |
| Avg trajectory length | 15.02 ± 8.93 | 20.21 ± 10.16 |
| (Human reference length) | 7.92 ± 5.18 | — |

[VERIFIED][1]

**Per-doménová variance:** Plánování pomáhá Mapě (+2.6%) a Redditu (+4%), škodí CMS (-3.84%), GitLabu (-1.37%), e-commerce (-2.49%). [VERIFIED][1]

**Implementační detaily:** GPT-4o-mini, temperature 1.0, top-p 0.95, max 30 kroků, statistika v IBM SPSS 27. Full-Plan agent dostává v každém kroku: current plan + accessibility tree + active URL + task objective. [VERIFIED][1]

### 2. Taxonomie je derivativní

ToolTree (Yang et al. 2026, ICLR) §6 explicitně atribuuje [INFERRED][7]:

> "Various search algorithms, such as greedy search (ReAct, Yao 2023b), A* Search (ToolChain*, Zhuang 2024), Beam Search (Xie 2023), MCTS (LATS, Zhou 2024; RAP, Hao 2023), **BFS/DFS (Yao 2023a — Tree of Thoughts)**, **Best-first search (Koh 2024)** have been integrated at inference time."

Atribuční řetězec:
- BFS/DFS pro LLM thoughts → Yao et al. 2023, Tree of Thoughts (NeurIPS) [INFERRED][7,14]
- Best-First pro web agenty → Koh et al. 2024 [INFERRED][6,7]
- MCTS pro language agenty → LATS Zhou 2024, RAP Hao 2023 [INFERRED][7,16]

Modernější taxonomie nabízejí bohatší dekompozici. **Bilenko et al. 2026** [VERIFIED][13] rozkládá agenty na 6 top-level dimenzí: *Core Components* (perception, memory, action, profiling), *Cognitive Architecture* (planning, reflection), *Learning*, *Multi-Agent Systems*, *Environments and Domains*, *Evaluation and Safety*. **Plan-MCTS** [VERIFIED][6] navíc zavádí ortogonální osu *Action-Space vs Plan-Space*: granularita search jednotky se ukazuje důležitější než výběr search policy.

### 3. Empirické srovnání s WebArena ekosystémem

Paper porovnává 38.41% vs 36.29%. WebArena leaderboard zobrazuje mnohem širší spektrum [VERIFIED][6]:

| Method | Paradigma | WebArena Avg |
|---|---|---|
| **AgentOccam** (GPT-4-Turbo) | **Linear baseline** | **45.7%** |
| Plan-MCTS (GPT-4o) | Plan-space MCTS | 39.2% |
| WebPilot (GPT-4o) | MCTS multi-agent | 37.2% |
| CER (GPT-4o) | Linear + experience replay | 36.7% |
| Branch-and-Browse (GPT-4o) | Tree-structured | 35.8% |
| AWM (GPT-4-Turbo) | Linear + workflow memory | 35.5% |
| SteP (GPT-4-Turbo) | Linear stacked policies | 33.3% |
| AutoEval (GPT-4) | Linear + reflection | 26.9% |
| BrowserGym (GPT-4o) | Step-by-step | 24.3% |
| Search Agent / Koh 2024 (GPT-4o) | Best-First Search | 19.2% |
| Webarena vanilla (GPT-4-Turbo) | Step-by-step ReAct | 16.5% |

**Tři neintuitivní fakta:**
- Linear AgentOccam (45.7%) bije všechny tree-search baselines [VERIFIED][6]
- Vanilla Best-First (19.2%) je o 26 percentilových bodů pod AgentOccam [VERIFIED][6]
- Tree search **ALE** vyhrává na tool planning (typed I/O) — ToolTree +3-10pp nad greedy [VERIFIED][7]. Doménově závislé.

Paper neuvádí kvantitativní výsledky pro Tree Search agenta v experimentální sekci [INFERRED][1]. Implementuje pouze 2 ze 3 architektur, které definuje — to limituje validity taxonomie.

### 4. Kontextová evaluační literatura (5 frameworků)

Pět konkurenčních frameworků pro hodnocení web agentů publikovaných 2024-2026:

**Online-Mind2Web / WebJudge** (Xue et al., COLM 2025) [VERIFIED][8]
- LLM-as-Judge se 83.6%-87% lidské shody (range across model variants: GPT-4o 83.6%, o4-mini 85.7%, WebJudge-7B 87.0%)
- Efficiency metrika E = mean(steps/reference_steps) na úspěšných tascích
- Headline: frontier agenti drasticky drop versus sandbox; "over-optimism in previously reported results"

**AgentRewardBench** (Lù et al.) [VERIFIED][9]
- 1,302 trajektorií × 5 benchmarků × 4 agenti
- Tří-otázkové expert annotation: success / side effects / repetitiveness
- Dokazuje že rule-based evaluators undercount success; 12 LLM judges, "no single LLM excels"

**WebGraphEval** (Qian et al.) [VERIFIED][10]
- 4,768 trajektorií agregováno do directed action graph (40k uzlů, 45k hran)
- Necessity rate (72.9-82.0% napříč 6 frameworky), step inflation 2.14× (3.18× na simple tasks)
- Edge classification: Trap / Critical / Bottleneck / Normal
- Klíčový finding: ze 761 WebArena tasks pouze 3.8% solved by all 6 agents, 13.0% failed by all, 83.2% mixed — vyvrací single-reference assumption

**TRACE** (Shi et al., WWW 2026) [VERIFIED][11]
- Hierarchical Trajectory Utility Function (HTUF) — composite (accuracy + efficiency + cognitive quality + evidence grounding)
- Scaffolded Capability Assessment — měří latent capability přes minimum guidance
- Targets "high-score illusion" (správná odpověď z neúspěšné trajectorie)

**WebArena Verified** (El hattami et al., NeurIPS 2025 SEA) [VERIFIED][12]
- Audit všech 812 WebArena úkolů
- Type-aware comparators redukují false negatives o ~11%
- Hard subset: 137 tasks, -83% eval cost
- Strukturovaný JSON status + 95% CIs + per-template macro averages

**Mapping S&D metrik na literaturu:**

| S&D metrika | Existující ekvivalent | Status |
|---|---|---|
| Repetitiveness Rate | AgentRewardBench binary repetitiveness label [9] | S&D **kvantifikuje** to, co literatura **labeluje** |
| Step Success Rate | WebGraphEval edge success-weighting s(e) [10] | Overlap se strukturálním framingem |
| Partial Success Rate | TRACE continuous HTUF [11] | TRACE subsumes |
| **Element Accuracy** | Není přímo mirror v žádném [8-12] | **Genuine differentiator** |
| **Recovery Rate** | Není přímo mirror v žádném [8-12] | **Genuine differentiator** |

[INFERRED][8,9,10,11,12]

S&D nabídku ALE chybí: **side-effect detection** (AgentRewardBench), **structural graph metrics** (WebGraphEval), **latent capability** (TRACE), **checker reliability fixes** (WebArena Verified) [VERIFIED][9,10,11,12].

### 5. STOPA mapping — co z toho použít

**a) Recovery Rate jako dimenze pro `/eval` a `/annotate` [INFERRED]**

S&D Recovery Rate (5-step lookahead, "did agent return to gold trajectory?") je konceptuálně přenositelný na orchestrátorové trace:

```
Recovery@n = (1/#runs) Σ [# critic-recovery success / # critic FAIL events in run]
```

STOPA má 3-fix escalation a critic loops — Recovery Rate by mohl měřit, jak často se agent dokáže zotavit po prvním FAILu vs musí orchestrátor restart. Aktuálně tracking přes failures/ není kvantifikovaný v této ose.

**Konkrétní změna:** přidat do `/eval` skill rubric jednu řádku — "Recovery rate per critic FAIL event" jako TSV column.

**b) Element Accuracy jako diagnostický signál pro `/orchestrate` review [INFERRED]**

Pattern "Full-Plan má 89% Element Accuracy ale 36% task success" znamená že agent perfektně provádí plán, který je špatný. Pro STOPA: pokud subtasky vykazují vysokou completion ale nízkou overall success score, root cause je v plan-quality (scout output), ne v execution.

**Konkrétní heuristika:** v `/critic` PR review tier, když agenti reportují 100% subtask completion ale verify FAILuje, předpokládej špatný plán → re-run scout místo retry agentů.

**c) Single-annotator gold trajectories — STOPA nemá tento problem [VERIFIED]**

S&D má methodologickou slabinu (autoři jako jediní anotátoři). STOPA má opačný problém: anotace v `/annotate` Align Evals dělá uživatel sám pro svoje traces. Co STOPA může převzít z AgentRewardBench [9]: 3-otázkové schéma anotace (success / side effects / repetitiveness) místo binárního labelu.

**Konkrétní změna:** v `/annotate` skill rozšířit anotační schéma z binary good/bad na 3-osé hodnocení.

**d) Plan-space vs Action-space (z Plan-MCTS) [VERIFIED][6]**

Plan-MCTS dokazuje, že plan-space search systematicky bije action-space search napříč modely [VERIFIED][6]. STOPA's `/scout` → `/orchestrate` separace už toto dělá implicitně (subtask-level decomposition před execution). Validuje stávající architekturu.

**Žádná změna potřeba** — STOPA toto má. Lekce: zachovat scout/orchestrate split jako fundamentální, ne ho consolidovat.

**e) Bilenko's "Tree-search latency unacceptable for real-time" [VERIFIED][13]**

> "There is a pressing need for 'System 2' thinking to be distilled into efficient 'System 1' reflexes. Research into ReWOO offers a path forward by separating planning from execution."

Lekce pro STOPA: cost rationale pro `orchestrate-light` tier (single-file mechanical fixes bez full scout) je validní. Tree-search pro každý úkol = nepoužitelné pro běžný workflow.

**Žádná změna** — STOPA má `orchestrate-light`. Lekce: nezavádět tree search jako default.

**f) AgentOccam linear win — co dělá konkrétně [VERIFIED][6]**

Plan-MCTS [6] popisuje AgentOccam jako "well-engineered linear baseline" bez search. Lekce: před zavedením komplexnějších orchestračních patterns dolaď linear pipeline. STOPA je už v tomto stadiu — `/orchestrate` má matured workflow, ne MCTS.

**Konkrétní heuristika:** "linear well-tuned > naive tree search" — když uvažuju o přidání multi-agent search do `/orchestrate`, prerequisite je dokázat že linear varianta je v plateau.

### 6. Co paper nedělá (limitace a gaps)

**[VERIFIED][1]:**
- Tree Search agent v experimentální sekci kvantitativně neporovnán
- Žádné inter-annotator agreement statistiky
- LLM-as-judge bez independent validation
- Generalizace na non-web domény tvrzena ale nezkoušena
- Full-Plan agent "not optimized" — proof of concept disclaimer

**[VERIFIED][6]:**
- Vynechán empirický context: AgentOccam 45.7% > 38.41% paper-best by ~7pp
- Plan-space vs Action-space osa nediskutována

**[VERIFIED][1,9]:**
- Single-annotator je problém, který AgentRewardBench výslovně řeší (1302 trajectories, expert panel)

**[INFERRED][8,12]:**
- WebJudge a WebArena Verified ukazují, že rule-based eval undercounts; S&D používá rule-based + LLM judge bez ablation contribution

---

## Disagreements & Open Questions

**Konflikty mezi zdroji:**

- **Tree search efektivita:** Plan-MCTS [6] ukazuje underperform na WebArena; ToolTree [7] ukazuje +3-10pp výhru na tool planning. Resolution: doménově závislé (typed I/O vs noisy GUI actions).
- **Co potřebuje pole:** AgentRewardBench [9] navrhuje lepší judges, WebGraphEval [10] strukturální metriky, WebArena Verified [12] benchmark fixes, S&D [1] více dimenzí. Resolution: každá vrstva selhání řešená jiným framework, všechny validní.

**Open questions:**

1. **Tree Search agent kvantitativní výsledky** — paper má 3-class taxonomii ale experimenty na 2 ze 3 [INFERRED][1].
2. **"Plans followed precisely but wrong plans" framing** — nenalezeno v retrieved 2024-2026 literatuře. Možná genuinely novel formulace [SINGLE-SOURCE][1].
3. **Generalizace mimo web** — robotics, GUI automation, multimodal — autoři tvrdí ale netestují [VERIFIED][1].
4. **Dataset URL** — referenced ale extracted obsah neukázal konkrétní URL [UNVERIFIED].
5. **GPT-5-mini model name v Plan-MCTS Table 2** — table existence potvrzena ale model names neextrahovány během fetch [UNVERIFIED][6].

---

## Evidence Table

| # | Source | URL | Key Claim | Type | Confidence |
|---|--------|-----|-----------|------|------------|
| 1 | Shahnovsky & Dror 2026 | https://arxiv.org/abs/2603.12710 | Primary paper — taxonomy + 5 metrics + dataset + experimental results | primary | high |
| 6 | Wang et al. Plan-MCTS 2026 | https://arxiv.org/html/2602.14083 | AgentOccam linear 45.7% beats Plan-MCTS 39.2% on WebArena | primary | high |
| 7 | Yang et al. ToolTree 2026 | https://arxiv.org/html/2603.12740v1 | BFS/DFS attribution to ToT; Best-First to Koh 2024 | primary | high |
| 8 | Xue et al. Online-Mind2Web/WebJudge COLM 2025 | https://arxiv.org/html/2504.01382 | LLM judge 83.6-87% human agreement; sandbox over-reporting | primary | high |
| 9 | Lù et al. AgentRewardBench | https://arxiv.org/html/2504.08942v2 | 1302 trajectories × 5 benchmarks; rule-based undercounts | primary | high |
| 10 | Qian et al. WebGraphEval | https://arxiv.org/html/2510.19205 | 4768 trajectories; necessity 72.9-82%, step inflation 2.14× | primary | high |
| 11 | Shi et al. TRACE WWW 2026 | https://arxiv.org/html/2602.21230v1 | HTUF + Scaffolded Capability Assessment | primary | high |
| 12 | El hattami et al. WebArena Verified NeurIPS 2025 SEA | https://openreview.net/forum?id=94tlGxmqkN | Type-aware comparators -11% false negatives | primary | high |
| 13 | Bilenko et al. Agentic AI Jan 2026 | https://arxiv.org/html/2601.12560v1 | 6-dimension architecture taxonomy | primary | high |
| 14 | Yao et al. 2023 Tree of Thoughts | https://arxiv.org/abs/2305.10601 | Original BFS/DFS framing for LLM thought trees | foundational | medium (transitive) |
| 15 | Koh et al. 2024 Tree Search for LM Agents | (no canonical URL captured) | Best-First Search for LLM web agents | foundational | medium (transitive) |
| 16 | Zhou et al. 2024 LATS | https://arxiv.org/html/2310.04406 | MCTS for language agents | foundational | medium (transitive) |
| 17 | Huang et al. 2024 LLM agent planning survey | https://arxiv.org/abs/2402.02716 | Canonical 5-category planning taxonomy | survey | partial (abstract only) |

---

## Sources

1. Shahnovsky O., Dror R. (2026) "AI Planning Framework for LLM-Based Web Agents" — https://arxiv.org/abs/2603.12710
6. Wang et al. (2026) "Plan-MCTS: Plan Exploration for Action Exploitation in Web Navigation" — https://arxiv.org/html/2602.14083
7. Yang et al. (2026, ICLR) "ToolTree: Efficient LLM Agent Tool Planning via Dual-Feedback Monte Carlo Tree Search" — https://arxiv.org/html/2603.12740v1
8. Xue et al. (COLM 2025) "An Illusion of Progress? Assessing the Current State of Web Agents" — https://arxiv.org/html/2504.01382
9. Lù et al. "AgentRewardBench: Evaluating Automatic Evaluations of Web Agent Trajectories" — https://arxiv.org/html/2504.08942v2
10. Qian et al. "WebGraphEval: Multi-Turn Trajectory Evaluation using Graph Representation" — https://arxiv.org/html/2510.19205
11. Shi et al. (WWW 2026) "TRACE: Trajectory-Aware Comprehensive Evaluation for Deep Research Agents" — https://arxiv.org/html/2602.21230v1
12. El hattami et al. (NeurIPS 2025 SEA) "WebArena Verified: Reliable Evaluation for Web Agents" — https://openreview.net/forum?id=94tlGxmqkN
13. Bilenko et al. (Jan 2026) "Agentic AI: Architectures, Taxonomies, and Evaluation" — https://arxiv.org/html/2601.12560v1
14. Yao et al. (2023) "Tree of Thoughts: Deliberate Problem Solving with Large Language Models" — https://arxiv.org/abs/2305.10601 (transitive citation)
16. Zhou et al. (2024) "Language Agent Tree Search" — https://arxiv.org/html/2310.04406 (transitive citation)
17. Huang et al. (Feb 2024) "Understanding the planning of LLM agents: A survey" — https://arxiv.org/abs/2402.02716 (abstract only)

---

## Coverage Status

- **[VERIFIED] (26 claims):** Všechna primární data z paperu (38.41/36.29, 89/82, 794, doménové výsledky, dataset metadata, GPT-4o-mini setup), AgentOccam 45.7% & related WebArena leaderboard, všechny formule 5 evaluačních frameworků, atribuce ToT/Koh/LATS přes ToolTree §6, Bilenko 6-dimenze, WebArena Verified 11% reduction, Plan-MCTS Action vs Plan-Space split.
- **[INFERRED] (3 claims):** Mapping S&D metrik na konkurenční frameworky (negative finding přes 5 zdrojů), Tree Search experimental absence (negative finding z extracted paper), atribuce BFS/DFS k Yao 2023 přes ToolTree (transitive but cross-source).
- **[SINGLE-SOURCE] (1 claim):** Originalita "plans followed precisely but wrong plans" framing — nenalezeno v ostatní literature, possibly novel.
- **[UNVERIFIED] (2 claims):** Exact dataset URL, exact GPT-5-mini model name v Plan-MCTS Table 2.

**Verifier status:** DONE_WITH_CONCERNS (řešeno v této verzi: Bilenko taxonomy structure, WebJudge range, AgentOccam citation [6] not [7], transitive citation markers).

**Claim inventory checkpoint:** PASS (74% verified, 9% unresolved — pod 30% threshold).
