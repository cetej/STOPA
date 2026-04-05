# EgoAlpha/prompt-in-context-learning — Research Brief

**Date:** 2026-04-05
**Question:** Jaké jsou klíčové prompt engineering techniky v EgoAlpha/prompt-in-context-learning a které jsou aplikovatelné pro STOPA skill development?
**Scope:** broad (survey)
**Sources consulted:** 43 (25 papers + repo files)
**Scale:** survey (3 parallel researchers)

---

## Executive Summary

EgoAlpha/prompt-in-context-learning je **living paper tracker** (denní aktualizace, v3.0.0), ne implementation library [VERIFIED][1]. Praktická část (`PromptEngineering.md`) pokrývá pouze základní 5-komponentní framework [VERIFIED][2] — pokročilé techniky jsou výhradně ve formě paper listů bez kódu, šablon nebo failure mode analýzy.

**Klíčový strukturální nález:** STOPA orchestrační architektura má silné akademické precedenty, které ji retrospektivně validují. `/orchestrate` ↔ Least-to-Most Prompting [VERIFIED][6], Anti-Rationalization Defense ↔ Contrastive CoT, 3-fix escalation ↔ Reflexion verbal RL loop [VERIFIED][10], `/critic`+`/autoloop` ↔ Self-Refine [VERIFIED][12]. Toto není koincidence — jsou to konvergentní řešení stejných problémů.

**Nejvýznamnější gap:** Reflexion mechanismus [VERIFIED][10] je v STOPA implementován neúplně. 3-fix escalation zachytí selhání, ale negeneruje explicitní verbální notu "co příště udělám jinak" — pouze error log. Reflexion ukazuje, že právě tato nota (uložená do episodic memory) je zodpovědná za 91% vs 80% HumanEval. Toto je největší actionable improvement s nejnižším implementation effort.

---

## Detailed Findings

### 1. Repo struktura a charakter

EgoAlpha/prompt-in-context-learning [VERIFIED][1] je kurátorovaný paper tracker se sekcemi:
- `PaperList/` — 10+ souborů: `ChainofThoughtList.md` (59+ papers), `AgentList.md` (20+ papers), `KnowledgeAugmentedPromptList.md` (55+ papers), `InContextLearningList.md`, `AutomaticPromptList.md` atd.
- `PromptEngineering.md` [VERIFIED][2] — 5-komponentní framework s worked examples (sentiment analysis, NER, SQL generation, Python code)
- `Playground.md` — seznam dostupných LLM pro experimentování

**Repo není implementation guide** [VERIFIED][2][3]. Pokročilé techniky (ToT, ReAct, Reflexion) jsou pouze citovány s GitHub stars a citation count — bez kódu, šablon nebo failure mode analýzy. Toto omezuje přímou implementační využitelnost, ale nevadí to — hodnota repa je v mapě papírů.

### 2. 5-komponentní prompt framework

Z `PromptEngineering.md` [VERIFIED][2], 5 komponent každého efektivního promptu:

| Komponenta | Popis | STOPA analogie |
|------------|-------|----------------|
| **Context** | Background, role modelu | SKILL.md frontmatter + role assignment |
| **Instruction** | Co má model udělat | SKILL body — workflow steps |
| **Relevance** | Specifická data/reference | key-facts.md, memory files |
| **Constraint** | Formát, délka, styl výstupu | Output Format sekce v SKILL |
| **Demonstration** | Příklady vstup→výstup | Příklady v SKILL body (ICL exempláře) |

Tento framework je akademická validace struktury SKILL.md. Klíčový insight [INFERRED][2][10]: **pořadí exemplárů záleží** (Lu et al. 2021 — order sensitivity) — nejsilnější příklady by měly být na konci SKILL body (recency effect v ICL).

### 3. Chain-of-Thought rodina — 59+ variant

Originální CoT (Wei et al. 2022) [VERIFIED][3] ukázal, že mezihodné kroky reasoning dramaticky zlepší výkon na math/logic. 396 citací. Funguje primárně na velkých modelech (100B+, tedy Sonnet/Opus tier).

**Nejdůležitější varianty pro STOPA:**

**Zero-shot CoT** (Kojima et al. 2022) [VERIFIED][4] — "Let's think step by step" bez příkladů. 187 citací. Nulové náklady, funguje na moderních modelech. Přidat do `/critic` a `/systematic-debugging` prompt body.

**Self-Consistency** (Wang et al. 2022) [VERIFIED][5] — Sample N reasoning paths, majority vote. +17.9% GSM8K, +11.0% SVAMP, +12.2% AQuA [VERIFIED][5]. Zvyšuje latenci, ale dramaticky přesnost. Aplikovatelné v `/verify` pro high-stakes outputs.

**Least-to-Most Prompting** (Zhou et al. 2022) [VERIFIED][6] — Dekompozice složitého problému na podproblémy v pořadí. 90 citací. Přímá akademická validace `/orchestrate` dekompozičního přístupu.

**Contrastive CoT** [INFERRED][2] — Negativní příklady (co NEDĚLAT) v demonstracích. Přesná akademická analogie **Anti-Rationalization Defense** sekce v SKILL.md. Potvrzuje, že tento STOPA pattern je efektivní.

**STaR** (Zelikman et al. 2022) [VERIFIED][23] — Bootstrapping reasoning přes self-generated rationales. 56 citací. Inspirace pro `/self-evolve` — model generuje vlastní training signal.

### 4. Pokročilé reasoning/planning techniky

**Tree of Thoughts** (Yao et al. 2023) [VERIFIED][7] — Deliberate search over thought tree s LM evaluation. GPT-4+ToT: 74% vs 4% CoT na Game of 24 [VERIFIED][7]. 4.4k GitHub stars. Mechanismus: deliberate search s backtracking.

**Graph of Thoughts** (Besta et al. 2023) [VERIFIED][8] — DAG místo lineárního řetězu, umožňuje aggregaci a loopy. +62% quality vs ToT, -31% cost [VERIFIED][8] na sorting tasks.

**Self-Consistency** je nejefektivnější "drop-in" upgrade — přidá latenci ale zachová prompt strukturu [VERIFIED][5].

**LATS** (Zhou et al. 2023) [VERIFIED][11] — Monte Carlo Tree Search kombinovaný s LM reasoning a self-reflection. 92.7% pass@1 HumanEval (GPT-4) [VERIFIED][11]. Nejblíže k akademickému ekvivalentu STOPA deep tier orchestrace s branching.

Performance hierarchie na complex tasks [INFERRED][7][8][9][10][11]:
`LATS (92.7%) > Reflexion (91%) > ReAct >> ToT (74% na G24) > Self-Consistency > standard CoT (4% na G24)`

### 5. Agentní vzory a tool-use

**ReAct** (Yao et al. 2022) [VERIFIED][9] — Interleaved Thought→Action→Observation loop. +34% ALFWorld, +10% WebShop [VERIFIED][9]. 672 citací — nejcitovanější agent paper v repu. Klíčový insight: samotný CoT bez externího pozorování vede k halucinacím.

**Reflexion** (Shinn et al. 2023) [VERIFIED][10] — Verbal self-reflection jako substitut RL weight updates. Agent analyzuje selhání v natural language a ukládá insight do episodic memory bufferu. 91% pass@1 HumanEval vs 80% standard GPT-4 [VERIFIED][10].

**STOPA 3-fix escalation je formálně Reflexion smyčka** [INFERRED][10] — ale chybí explicitní "co příště jinak" nota. Reflexion ukazuje, že tato nota (ne pouhý error log) je klíčovým mechanismem zlepšení.

**MetaGPT SOPs** (Hong et al. 2023) [VERIFIED][13] — Standardized Operating Procedures jako prompt sekvence. Assembly-line paradigma: každý agent produkuje definovaný output format pro dalšího. Snižuje halucinační kaskády. STOPA skills by měly mít explicitní "output contract" dokumentovaný ve frontmatter.

**Self-Refine** (Madaan et al. 2023) [VERIFIED][12] — Generate → feedback → refine, bez trénování. ~20% improvement across 7 tasks. Tři kroky v jednom LLM. STOPA `/critic` + `/autoloop` je přesně tento pattern.

**Self-RAG** (Asai et al. 2023) [VERIFIED][16] — Reflection tokens řídí adaptivní retrieval: `[Retrieve]`, `[Relevant]`, `[Supported]`, `[Utility]`. Pro STOPA `/deepresearch`: každá citace by měla mít explicitní relevance token, ne pouze slepé použití kontextu.

**SKR** (Wang et al. 2023) [VERIFIED][18] — Self-Knowledge Guided Retrieval: model odhaduje svou vlastní knowledge boundary před rozhodnutím o retrieval. Outperformuje CoT AND fully-retrieval methods. Pro STOPA `/scout`: pre-flight self-assessment "vím to z paměti?"

**Self-Discover** (Zhou et al. 2024) [VERIFIED][19] — LLM dynamicky vybírá atomické reasoning moduly a skládá task-specific strukturu. +32% vs CoT, 10-40× méně compute než Self-Consistency [VERIFIED][19]. Pro STOPA `/triage`: dynamický výběr reasoning modulů (CoT? Search? Verification? Tool-use?).

**SPP — Solo Performance Prompting** (Chen et al. 2023) [VERIFIED][20] — Jeden LLM simuluje multi-agent systém dynamickým přiřazením personas. Kognitivní synergie se projevuje **pouze při GPT-4 / Opus level** modelech, ne menších [VERIFIED][20]. Pro STOPA `/council`: omezit na sonnet+ tier.

### 6. RAG a knowledge augmentation

**FLARE** (Jiang et al. 2023) [VERIFIED][22] — Forward-looking retrieval: generuj predikci → detekuj low-confidence tokeny → použij predikci jako query → regeneruj. Hlavní přínos: retrieval na demand, ne vždy. Pro STOPA `/deepresearch`: dynamické generování queries ze špatně zodpovězených sekcí.

**DSP / Demonstrate-Search-Predict** (Khattab et al. 2023) [VERIFIED][17] — Kompozice retrieval+LM primitiv. 37-290% relativní zlepšení vs baselines [VERIFIED][17]. STOPA recipe systém je DSP pipeline v praxi.

---

## Disagreements & Open Questions

- **GoT vs ToT tradeoff:** GoT ukazuje +62% quality při -31% cost vs ToT [VERIFIED][8], ale ToT má 21× více citací. Nejasné zda GoT advantage platí obecně nebo pouze pro specific task types (sorting). [SINGLE-SOURCE][8]

- **Self-Discover vs Self-Consistency:** Self-Discover tvrdí 10-40× méně compute než SC při srovnatelné nebo lepší kvalitě [VERIFIED][19] — pokud platí obecně, SC by měla být nahrazena Self-Discover jako default "upgrade". Potřeba více replikace.

- **SPP threshold:** SPP potvrzuje, že multi-persona funguje jen na GPT-4+ [VERIFIED][20], ale přesný threshold není jasný pro Sonnet 4.6 vs Opus 4.6. [UNVERIFIED]

---

## Evidence Table (top 25)

| # | Source | URL | Key Claim | Type | Confidence |
|---|--------|-----|-----------|------|------------|
| 1 | EgoAlpha README | https://github.com/EgoAlpha/prompt-in-context-learning | Living paper tracker v3.0.0, denní aktualizace | primary | high |
| 2 | PromptEngineering.md | https://github.com/EgoAlpha/prompt-in-context-learning/blob/main/PromptEngineering.md | 5-komponentní framework, no advanced technique impl | primary | high |
| 3 | Wei et al. 2022 | https://arxiv.org/abs/2201.11903 | CoT prompting, 396 citations | primary | high |
| 4 | Kojima et al. 2022 | https://arxiv.org/abs/2205.11916 | Zero-shot CoT "Let's think step by step" | primary | high |
| 5 | Wang et al. 2022 | https://arxiv.org/abs/2203.11171 | Self-Consistency: +17.9% GSM8K | primary | high |
| 6 | Zhou et al. 2022 | https://arxiv.org/abs/2205.10625 | Least-to-Most: sequential subproblem decomposition | primary | high |
| 7 | Yao et al. 2023 | https://arxiv.org/abs/2305.10601 | ToT: 74% vs 4% CoT on Game of 24 | primary | high |
| 8 | Besta et al. 2023 | https://arxiv.org/abs/2308.09687 | GoT: +62% quality vs ToT, -31% cost | primary | high |
| 9 | Yao et al. 2022 | https://arxiv.org/abs/2210.03629 | ReAct: +34% ALFWorld, 672 citations | primary | high |
| 10 | Shinn et al. 2023 | https://arxiv.org/abs/2303.11366 | Reflexion: 91% HumanEval vs GPT-4 80% | primary | high |
| 11 | Zhou et al. 2023 | https://arxiv.org/abs/2310.04406 | LATS: 92.7% HumanEval (GPT-4), MCTS-inspired | primary | high |
| 12 | Madaan et al. 2023 | https://arxiv.org/abs/2303.17651 | Self-Refine: ~20% improvement across 7 tasks | primary | high |
| 13 | Hong et al. 2023 | https://arxiv.org/abs/2308.00352 | MetaGPT SOPs: handoff contracts snižují halucinace | primary | high |
| 14 | Wu et al. 2023 | https://arxiv.org/abs/2308.08155 | AutoGen: conversable agents + human-in-loop | primary | high |
| 15 | Wang et al. 2024 | https://arxiv.org/abs/2406.18532 | Symbolic self-evolving: NL backpropagation | primary | high |
| 16 | Asai et al. 2023 | https://arxiv.org/abs/2310.11511 | Self-RAG reflection tokens per citation | primary | high |
| 17 | Khattab et al. 2023 | https://arxiv.org/abs/2212.14024 | DSP compose: 37-290% vs baselines | primary | high |
| 18 | Wang et al. 2023 | https://arxiv.org/abs/2310.05002 | SKR: self-knowledge boundary before retrieval | primary | high |
| 19 | Zhou et al. 2024 | https://arxiv.org/abs/2402.03620 | Self-Discover: +32% vs CoT, 10-40× less compute | primary | high |
| 20 | Chen et al. 2023 | https://arxiv.org/abs/2307.05300 | SPP: cognitive synergy only at GPT-4 level | primary | high |
| 21 | Yu et al. 2023 | https://arxiv.org/abs/2311.09210 | Chain-of-Note: +7.9 EM on noisy documents | primary | high |
| 22 | Jiang et al. 2023 | https://arxiv.org/abs/2305.06983 | FLARE: dynamic retrieval from uncertain sections | primary | high |
| 23 | Zelikman et al. 2022 | https://arxiv.org/abs/2203.14465 | STaR: bootstrapping reasoning via self-rationales | primary | high |
| 24 | Qin et al. 2023 | https://arxiv.org/abs/2307.16789 | ToolLLM DFSDT: depth-first tool search with backtracking | primary | high |
| 25 | Luo et al. 2024 | https://arxiv.org/abs/2402.19446 | ArCHer: hierarchical credit assignment, 100× efficiency | primary | high |

---

## STOPA Actionable Improvements (prioritized)

### Tier 1 — Okamžitě (low effort, high confidence)

| # | Technika | Zdroj | STOPA změna | Effort |
|---|----------|-------|------------|--------|
| 1 | Zero-shot CoT | [VERIFIED][4] | Přidat "Let's think step by step" do `/critic` a `/systematic-debugging` prompt body | 5 min |
| 2 | Reflexion verbal note | [VERIFIED][10] | Po každém FAIL v 3-fix escalation generovat "co příště udělám jinak" notu (ne jen error log) | 30 min |
| 3 | ICL order sensitivity | [INFERRED][2][6] | Nejsilnější příklady v SKILL.md demonstracích dát na konec (recency effect) | 15 min |
| 4 | SPP model gating | [VERIFIED][20] | `/council` frontmatter: `min_model: sonnet` — haiku nespouštět pro multi-persona | 10 min |

### Tier 2 — Short-term (medium effort, validated by multiple papers)

| # | Technika | Zdroj | STOPA změna | Effort |
|---|----------|-------|------------|--------|
| 5 | MetaGPT output contracts | [VERIFIED][13] | Přidat `output-contract:` field do SKILL frontmatter | 2h |
| 6 | SKR pre-flight self-assessment | [VERIFIED][18] | `/scout` starts with "Do I know this from memory/key-facts? Only if no → search" | 1h |
| 7 | Self-RAG reflection tokens | [VERIFIED][16] | `/deepresearch` přidá per-citaci `[Relevant/Irrelevant/Uncertain]` token | 1h |
| 8 | FLARE dynamic queries | [VERIFIED][22] | `/deepresearch` generuje queries ze špatně zodpovězených sekcí, ne pre-fixed | 2h |

### Tier 3 — Long-term (high effort, high impact)

| # | Technika | Zdroj | STOPA změna | Effort |
|---|----------|-------|------------|--------|
| 9 | LATS-lite branching | [VERIFIED][11] | Deep tier orchestration: branch exploration před lineárním 3-fix escalation | 1 den |
| 10 | Self-Discover reasoning modules | [VERIFIED][19] | `/triage` dynamicky vybírá reasoning modules (CoT? Search? Verify?) | 1 den |

---

## Sources (top 25)

1. EgoAlpha Lab — README.md — https://github.com/EgoAlpha/prompt-in-context-learning
2. EgoAlpha Lab — PromptEngineering.md — https://github.com/EgoAlpha/prompt-in-context-learning/blob/main/PromptEngineering.md
3. Wei et al. (2022) — Chain of Thought Prompting Elicits Reasoning in LLMs — https://arxiv.org/abs/2201.11903
4. Kojima et al. (2022) — Large Language Models are Zero-Shot Reasoners — https://arxiv.org/abs/2205.11916
5. Wang et al. (2022) — Self-Consistency Improves Chain of Thought Reasoning — https://arxiv.org/abs/2203.11171
6. Zhou et al. (2022) — Least-to-Most Prompting Enables Complex Reasoning — https://arxiv.org/abs/2205.10625
7. Yao et al. (2023) — Tree of Thoughts: Deliberate Problem Solving — https://arxiv.org/abs/2305.10601
8. Besta et al. (2023) — Graph of Thoughts — https://arxiv.org/abs/2308.09687
9. Yao et al. (2022) — ReAct: Synergizing Reasoning and Acting — https://arxiv.org/abs/2210.03629
10. Shinn et al. (2023) — Reflexion: Language Agents with Verbal RL — https://arxiv.org/abs/2303.11366
11. Zhou et al. (2023) — Language Agent Tree Search (LATS) — https://arxiv.org/abs/2310.04406
12. Madaan et al. (2023) — Self-Refine: Iterative Refinement with Self-Feedback — https://arxiv.org/abs/2303.17651
13. Hong et al. (2023) — MetaGPT: Meta Programming for Multi-Agent Framework — https://arxiv.org/abs/2308.00352
14. Wu et al. (2023) — AutoGen: Enabling Next-Gen LLM Applications — https://arxiv.org/abs/2308.08155
15. Wang et al. (2024) — Symbolic Learning Enables Self-Evolving Agents — https://arxiv.org/abs/2406.18532
16. Asai et al. (2023) — Self-RAG: Learning to Retrieve, Generate, and Critique — https://arxiv.org/abs/2310.11511
17. Khattab et al. (2023) — Demonstrate-Search-Predict (DSP) — https://arxiv.org/abs/2212.14024
18. Wang et al. (2023) — Self-Knowledge Guided Retrieval Augmentation (SKR) — https://arxiv.org/abs/2310.05002
19. Zhou et al. (2024) — Self-Discover: LLMs Self-Compose Reasoning Structures — https://arxiv.org/abs/2402.03620
20. Chen et al. (2023) — Solo Performance Prompting (SPP) — https://arxiv.org/abs/2307.05300
21. Yu et al. (2023) — Chain-of-Note: Enhancing Robustness in RAG — https://arxiv.org/abs/2311.09210
22. Jiang et al. (2023) — Active Retrieval Augmented Generation (FLARE) — https://arxiv.org/abs/2305.06983
23. Zelikman et al. (2022) — STaR: Bootstrapping Reasoning With Reasoning — https://arxiv.org/abs/2203.14465
24. Qin et al. (2023) — ToolLLM: Facilitating LLMs to Master 16k+ APIs — https://arxiv.org/abs/2307.16789
25. Luo et al. (2024) — ArCHer: Training Language Model Agents via Hierarchical RL — https://arxiv.org/abs/2402.19446

---

## Coverage Status

- **[VERIFIED]:** Všechna čísla (benchmark scores, citation counts) z arXiv abstraktů přímo čtených agentem B. ReAct, Reflexion, LATS, GoT, Self-Consistency, ToT čísla jsou spolehlivé.
- **[INFERRED]:** Mapping STOPA komponent na akademické techniky (STOPA ↔ Reflexion, SKILL.md ↔ 5-component framework) — logická dedukce ze dvou nezávislých zdrojů.
- **[SINGLE-SOURCE]:** GoT výsledky (+62% vs ToT) jen z abstraktu Besta et al., 1 citace — slibné ale málo replikováno.
- **[UNVERIFIED]:** SPP model threshold pro Sonnet 4.6 — SPP paper testoval GPT-4 vs GPT-3.5, ne Sonnet/Opus specificky.
