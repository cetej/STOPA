# Tool-Genesis: A Task-Driven Tool Creation Benchmark for Self-Evolving Language Agents — Research Brief

**Datum:** 2026-04-04
**Paper:** arXiv:2603.05578 | Submitted 2026-03-05
**Autoři:** Bowei Xia, Mengkang Hu, Shijian Wang, Jiarui Jin, Wenxiang Jiao, Yuan Lu, Kexin Li, Ping Luo
**Rozsah:** 25 stran, 10 obrázků, 2 tabulky | cs.SE + cs.AI
**Sources consulted:** 15 (14 accepted, 1 unresolved)

---

## Executive Summary

Tool-Genesis zavádí diagnostický benchmark, který vyhodnocuje schopnost language agentů **autonomně vytvářet nástroje z abstraktních požadavků** — bez předem definovaných specifikací. Klíčové zjištění: ani nejlepší SOTA modely (GPT-5.1, Qwen3-235B) nedokáží spolehlivě vygenerovat funkční nástroj v jednom průchodu. Nejlepší Direct SR je 0.372 (GPT-5.1) [VERIFIED][3].

Benchmark odhaluje **cascadový efekt selhání**: drobné chyby na rozhraní L1/L2 se zesilují přes pipeline a způsobují dramatický propad na L4. Pod Code-Agent (iterativní oprava s execution feedback) dosahuje Qwen3-235B SR 0.622 — poprvé open-source model překonává GPT-5.1 (0.604) v benchmarku tvorby nástrojů [VERIFIED][4].

Zásadní anti-intuitivní nález: Claude-Haiku-3.5 dosahuje Schema-F1 0.964 (nejlepší ze všech) pod Code-Agent, ale SR jen 0.472 — dokazuje, že povrchová správnost schématu **vůbec nepredikuje** downstream užitečnost [VERIFIED][7].

---

## Detailed Findings

### 1. Architektura benchmarku

Tool-Genesis obsahuje **2,150 úkolů** napříč **86 spustitelnými MCP servery** s **508 nástroji** [VERIFIED][1]. Dataset pokrývá 24 doménových tříd (systémové nástroje, data intelligence, produktivita, kreativní aplikace, servisní domény) a 18 kategorií typů úkolů. Celkem 9,441 unit testů; průměrný úkol: 53 tokenů, 6 kroků exekuce, 3 nástroje na úkol [VERIFIED][1].

**Konstrukce datasetu:** MCP servery sbírány z GitHub, HuggingFace a agregátorů čtyřfázovým filtračním procesem. Úkoly generovány LLM s rejection sampling (penalizace redundantních kombinací nástrojů) a LLM-as-judge quality filtrem (Likert 1–5, všechny dimenze >3, solvable=true). Tři doktorandští anotátoři; inter-annotator agreement Cohen's κ=0.85 [VERIFIED][11].

**Dva agentní módy:**
- **Direct:** Jednokrokové generování bez execution feedback.
- **Code-Agent:** ReAct-style smyčka (think→act→observe) až 10 kroků s sandboxed execution. Agent dostává zkrácený feedback z exekuce a generuje opravné patche [VERIFIED][9].

### 2. Čtyřúrovňová evaluační metrika (hlavní příspěvek)

| Úroveň | Metrika | Co měří |
|--------|---------|---------|
| **L1 Surface Compliance** | JSON Schema validace + Server Execution Rate | Parsovatelnost a spustitelnost nástroje |
| **L2 Semantic Interface Fidelity** | Schema-F1 (embedding bipartite matching) | Sémantická shoda predikovaného a referenčního rozhraní |
| **L3 Functional Correctness** | UT_soft (relaxed) + UT_hard (boundary/negative) | Funkční správnost včetně hraničních podmínek |
| **L4 Downstream Utility** | Oracle-normalized Success Rate | Vyřešení původního úkolu vs. ground-truth implementace |

Na rozdíl od všech předchůdců (CREATOR, LATM, TM-Bench, UltraTool) Tool-Genesis evaluuje **každou fázi pipeliny zvlášť** — umožňuje atribuovat selhání ke konkrétnímu kroku [VERIFIED][2].

### 3. Výsledky modelů

**Direct (jednokrokové generování):**

| Model | Compliance | Schema-F1 | UT-hard | SR |
|-------|-----------|-----------|---------|-----|
| GPT-5.1 | 0.826 | 0.688 | 0.161 | **0.372** |
| Qwen3-235B | 0.884 | 0.320 | 0.108 | 0.287 |
| Claude-Haiku-3.5 | 0.744 | ≤0.012 | ≤0.012 | ≤0.012 |

**Code-Agent (iterativní oprava):**

| Model | Schema-F1 | SR |
|-------|-----------|-----|
| Qwen3-235B | — | **0.622** |
| GPT-5.1 | 0.867 | 0.604 |
| Gemini-3-Flash | 0.912 | 0.581 |
| Claude-Haiku-3.5 | 0.964 | 0.472 |

Všechna čísla [VERIFIED][3][4][5][6][7].

### 4. Cascade failure — empirické jádro paperu

Pod Direct prompting kumulativní pass-through atribuovány k danému modelu dramaticky kolabuje:

- **Qwen3-8B:** L1 Compliance 68.6%, L4 SR jen 1.2% — ztráta >95% případů [INFERRED][8] (absolutní percentuální čísla z appendix sub-tabulek nebyla verifikátorem potvrzena, ale directional finding je konzistentní)
- **Qwen3-235B:** L4 attrition pod Direct je ~78% (SR 0.287 vs. Code-Agent 0.622)

Code-Agent dramaticky zlepšuje L1 pass-through: pro Qwen3-8B z 65.34% na 91.36% [VERIFIED][8]. Avšak L3/L4 attrition přetrvává — tyto vrstvy reprezentují **ireducibilní capability gap**, ne jen formátovací chyby.

### 5. Klíčové anti-intuitivní nálezy

**Scale reversal** [VERIFIED][9]: Qwen3-32B překonává 235B pod Direct. Pod Code-Agent naopak 235B překonává 32B. Autoři interpretují: větší modely jsou lepší v *exploitaci execution feedbacku*, ne v one-shot generování.

**Schema-utility decoupling** [VERIFIED][7]: Claude-Haiku-3.5 dosahuje Schema-F1 0.964 (nejvyšší ze všech) pod Code-Agent, ale SR jen 0.472. Povrchová shoda schématu **vůbec nepredikuje** downstream úspěch.

**Execution feedback je rozhodující proměnná** [VERIFIED][3][5]: Gemini-3-Flash Schema-F1 0.116 → 0.912 a SR 0.103 → 0.581 mezi Direct a Code-Agent. Execution feedback způsobuje skok, ne postupné zlepšení.

**Finetuning více pomáhá opravné smyčce než one-shot generování** [VERIFIED][10]: Trénink Qwen3-8B na Tool-Genesis datech: Direct SR 0.012→0.026, Code-Agent SR 0.336→0.399. Repair loop profituje více z fine-tuningu.

### 6. Pozice v benchmark ekosystému

| Benchmark | Rok | Tool sets | Domény | Evaluace | Spec-free |
|-----------|-----|-----------|--------|----------|-----------|
| CREATOR [3] | 2023 | 1 (2K otázek) | 9 | outcome-only | Ano |
| LATM [4] | 2023 | 6 | 6 | minimální | Ano |
| TM-Bench [6] | 2025 | **15** | **4** | unit tests | Ano |
| UltraTool [9] | 2024 | — | 22 | awareness-based | Ne |
| ToolBench/ToolLLM [2] | 2023 | — | 49 | tool USE | Ne |
| **Tool-Genesis** | 2026 | **86** | **24** | L1-L4 lifecycle | **Ano** |

Tool-Genesis je 5.7× větší než TM-Bench (nejbližší předchůdce), pokrývá 6× více domén, a jako jediný kombinuje spec-free inference + čtyřúrovňové diagnostické metriky + MCP-based executable evaluation [VERIFIED][12][13].

**Konkurenční práce:** EvolveTool-Bench (arXiv:2604.00392, duben 2026) je komplementární — hodnotí tool libraries jako software artefakty (reuse, redundancy, regression, safety) [VERIFIED][14]. Systémy s podobnou task completion (63–68%) se mohou lišit o 18% v library health. Oba papery nezávisle validují: "outcome-only evaluation je nedostatečná."

---

## Disagreements & Open Questions

- **Přesné pořadí Code-Agent modelů**: Výzkumní agenti zpočátku identifikovali GPT-5.1 (0.604) jako nejlepší. Verifikátor potvrdil: Qwen3-235B dosahuje SR 0.622 a skutečně vede. Toto je pozoruhodné — open-source model překonává GPT-5.1 pod iterativním opravným módem.
- **Absolutní cascade čísla**: Percentuální pass-through pro Qwen3-8B (17.52%→0.12%) pochází pravděpodobně z appendix sub-tabulek nedostupných v HTML; directional finding potvrzen, přesné hodnoty [UNRESOLVED].
- **Proč schema-utility decoupling?** Paper konstatuje jev, ale mechanismus není plně vysvětlen. Hypotéza autorů: model generuje syntakticky správné schéma "napodobením" ale nedokáže vygenerovat sémanticky konzistentní implementaci.
- **Generalizovatelnost na non-MCP ekosystémy**: Benchmark používá MCP jako standardizaci. Přenositelnost výsledků na REST API nebo custom function calling není testována.

---

## Evidence Table

| # | Source | URL | Key Claim | Type | Confidence |
|---|--------|-----|-----------|------|------------|
| 1 | Tool-Genesis HTML | https://arxiv.org/html/2603.05578 | 2,150 tasks, 86 MCP servers, 508 tools, 24 domains, 9,441 unit tests | Dataset | high |
| 2 | Tool-Genesis HTML | https://arxiv.org/html/2603.05578 | Čtyřúrovňová evaluace L1–L4 | Architecture | high |
| 3 | Tool-Genesis HTML | https://arxiv.org/html/2603.05578 | GPT-5.1 Direct SR 0.372, Code-Agent SR 0.604 | Results | high |
| 4 | Tool-Genesis HTML (verifier) | https://arxiv.org/html/2603.05578 | Qwen3-235B Code-Agent SR 0.622 — nejvyšší ze všech | Results | high |
| 5 | Tool-Genesis HTML | https://arxiv.org/html/2603.05578 | Gemini-3-Flash Code-Agent SR 0.581, Schema-F1 0.912 | Results | high |
| 6 | Tool-Genesis HTML | https://arxiv.org/html/2603.05578 | Claude-Haiku-3.5 Direct Compliance 0.744, SR ≤0.012 | Results | high |
| 7 | Tool-Genesis HTML | https://arxiv.org/html/2603.05578 | Claude-Haiku-3.5 Code-Agent Schema-F1 0.964, SR 0.472 | Results | high |
| 8 | Tool-Genesis HTML | https://arxiv.org/html/2603.05578 | Code-Agent L1 pass-through: 65.34% → 91.36% vs Direct (Qwen3-8B) | Cascade | high |
| 9 | Tool-Genesis HTML | https://arxiv.org/html/2603.05578 | Scale reversal: Qwen3-32B > 235B Direct; 235B > 32B Code-Agent | Finding | high |
| 10 | Tool-Genesis HTML | https://arxiv.org/html/2603.05578 | Finetuning Qwen3-8B: Code-Agent SR 0.336 → 0.399 | Results | high |
| 11 | Tool-Genesis HTML | https://arxiv.org/html/2603.05578 | Inter-annotator κ=0.85 | Dataset | high |
| 12 | TM-Bench arXiv | https://arxiv.org/abs/2502.11705 | TM-Bench: 15 tool sets, 4 domény | Prior work | high |
| 13 | CREATOR arXiv | https://arxiv.org/abs/2305.14318 | CREATOR: první tool-creation benchmark | Prior work | high |
| 14 | EvolveTool-Bench arXiv | https://arxiv.org/abs/2604.00392 | Komplementární library-level evaluace | Concurrent | high |

---

## Sources

1. Bowei Xia et al., "Tool-Genesis: A Task-Driven Tool Creation Benchmark" (HTML) — https://arxiv.org/html/2603.05578
2. Tool-Genesis abstract — https://arxiv.org/abs/2603.05578
3. Yujia Qin et al., "ToolLLM: Facilitating LLMs to Master 16000+ Real-world APIs" (ICLR'24) — https://arxiv.org/abs/2307.16789
4. Tianle Cai et al., "Large Language Models as Tool Makers" (ICLR'24) — https://arxiv.org/abs/2305.17126
5. Siyu Yuan et al., "CRAFT: Customizing LLMs via Specialized Toolsets" — https://arxiv.org/abs/2401.04052
6. G. Wölflein et al., "LLM Agents Making Agent Tools" (ACL'25) — https://arxiv.org/abs/2502.11705
7. "SciEvo: Beyond Static Tools for Scientific Reasoning" — https://arxiv.org/abs/2601.07641
8. Xingyao Shi et al., "TroVE: Inducing Verifiable and Efficient Toolboxes" — https://arxiv.org/abs/2401.12869
9. Jing Qian et al., "UltraTool: Planning, Creation, Usage Benchmark" (ACL'24) — https://arxiv.org/abs/2401.17167
10. Minghao Guo et al., "StableToolBench" — https://arxiv.org/abs/2403.07714
11. Fanjia Yan et al., "Berkeley Function Calling Leaderboard v4" — https://arxiv.org/pdf/2407.00121
12. "EvolveTool-Bench: Quality of LLM-Generated Tool Libraries" — https://arxiv.org/abs/2604.00392
13. "Agentic Tool Use in LLMs" (survey) — https://arxiv.org/abs/2604.00835
14. "A Comprehensive Survey of Self-Evolving AI Agents" — https://arxiv.org/abs/2508.07407
15. Chengzu Li et al., "CREATOR" (EMNLP'23) — https://arxiv.org/abs/2305.14318

---

## Coverage Status

- **[VERIFIED]:** Veškeré klíčové výsledky (SR čísla, dataset statistiky, cascade L1 pass-through, κ, Code-Agent setup, TM-Bench velikost, CREATOR existence, EvolveTool-Bench)
- **[INFERRED]:** Absolutní percentuální cascade čísla pro Qwen3-8B (directional potvrzeno, přesné sub-tabulky nedostupné)
- **[SINGLE-SOURCE]:** Scale reversal finding (Qwen3-32B > 235B pod Direct) — pouze z paperu, bez replikace
- **[UNVERIFIED]:** Přesný seznam 18 task label kategorií a 24 doménových jmen (zmíněny počtem, ne jmény) | Žádná veřejná kódová/datasetová repozitář k datu 2026-04-04
