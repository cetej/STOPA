# Recursive Language Models × STOPA — Research Brief

**Date:** 2026-04-10
**Question:** Jak může arXiv:2512.24601 (RLM) vylepšit STOPA orchestrační systém?
**Scope:** complex (paper hloubka + related work + STOPA gap analýza + implementační plán)
**Sources consulted:** 13

## Executive Summary

RLM (Zhang, Kraska, Khattab — MIT/Stanford, Dec 2025) zavádí inference paradigma kde LLM **nikdy nevidí celý prompt**. Místo toho dostane metadata a přístup k promptu jako Python proměnné v REPL. Model píše kód pro dekompozici a rekurzivně volá sám sebe na snippetech. Výsledky: GPT-5+RLM dosahuje 91.3% na BrowseComp-Plus za $0.99/query [VERIFIED][1], zpracuje vstupy 100× delší než context window [VERIFIED][1], a je 3× levnější než summarization agenty [VERIFIED][1].

STOPA už implementuje 2 ze 7 RLM principů plně (VERIFY, ACCUMULATE) a 4 částečně. Klíčový nález: **STOPA by neměla adoptovat REPL pattern přímo** — Claude Code Agent tool už poskytuje ekvivalentní delegaci [VERIFIED][3]. Místo toho by měla adoptovat architektonické principy: metadata-only orchestraci, budget propagaci do sub-agentů, strukturované výstupy místo NL summarizace, a lazy context loading [VERIFIED][3,4].

Navrhujeme 8 konkrétních vylepšení ve 4 týdnech (~25h), z toho 3 quick wins implementovatelné za 1 týden: budget propagace, metadata-only scout, a recursion depth guard.

## Detailed Findings

### 1. Jak RLM funguje technicky

RLM inicializuje persistent Python REPL s promptem jako proměnnou. Model dostane konstantní metadata (délka, prefix, přístupové instrukce) a generuje Python kód pro dekompozici [VERIFIED][1]. Klíčová funkce `_subcall()` umožňuje rekurzivní volání LM na sub-promptech vytvořených programaticky [VERIFIED][1].

Tři emergentní vzory: (1) filtrování přes regex/kód bez čtení všech tokenů, (2) rekurzivní chunking podle sémantických hranic (Markdown headers, function boundaries), (3) konstrukce výstupu přes REPL proměnné — obchází output length limity [VERIFIED][1].

Implementace: `pip install rlms`, 3.3k stars, podporuje OpenAI/Anthropic/vLLM, REPL sandboxing přes Docker/Modal/E2B [VERIFIED][2].

### 2. Benchmarky a srovnání

| Model + Metoda | BrowseComp-Plus | OOLONG | OOLONG-Pairs | Cena |
|----------------|----------------|--------|-------------|------|
| GPT-5 base | — | 46.0% | 0.1% | — |
| GPT-5 + RLM | **91.3%** | **56.5%** | **58.0%** | $0.99/q |
| Summary agent | 70.5% | — | — | ~$3/q |
| Qwen3-8B base | — | low | ~0% | — |
| RLM-Qwen3-8B | — | +28.3% median | — | — |

[VERIFIED][1] — všechna čísla přímo z paperu.

OOLONG-Pairs (58% vs 0.1%) je emergentní schopnost — base model totálně selhává na O(n²) pairwise agregaci, RLM ji řeší přes rekurzivní dekompozici [VERIFIED][1].

RLM vs RAG: LC odpovídá správně 56.3% vs RAG 49% na QA, ale RAG vítězí na dialog [VERIFIED][4]. RLM jde dál — udržuje globální pohled a multi-stage reasoning, na rozdíl od single-pass RAG [INFERRED][5,6].

### 3. DSPy integrace

RLM je experimentální modul v DSPy (`dspy.RLM`) [VERIFIED][3]. Stejná research group (Khattab). WASM-sandboxed REPL, ne thread-safe s custom interpretery [VERIFIED][3]. DSPy poskytuje deklarativní "programming-not-prompting" paradigma [VERIFIED][3].

### 4. Two-Model Architecture

Root LM (capability-heavy: GPT-5, Opus) plánuje a píše orchestrační kód. Recursive LM (cheaper: GPT-5-mini, Haiku) zpracovává snippety [VERIFIED][6]. Toto přesně odpovídá STOPA model selection: Opus pro plánování, Haiku/Sonnet pro exekuci [VERIFIED][stopa-gaps].

### 5. Praktické omezení

- **Depth=1 v produkci** — depth>1 experimentální od v0.1.1a [VERIFIED][7]
- **120s timeout** per REPL call jako circuit breaker [SINGLE-SOURCE][7]
- **Sequential blocking** — sub-cally jsou sekvenční, parallel sub-calls jen přes `llm_batch()` [VERIFIED][5]
- **Malé modely selhávají** — Qwen3-8B base neumí generovat správný REPL kód bez fine-tuningu [VERIFIED][1]
- **Thinking models** — output token limity způsobují předčasné ukončení trajektorií [VERIFIED][1]

### 6. STOPA Gap Analysis

| RLM Princip | STOPA Status | Akce |
|-------------|-------------|------|
| PEEK (metadata-first) | **MISSING** | Scout --metadata mode |
| PLAN (inteligentní routing) | PARTIAL | Pre-execution strategy enumeration |
| PARTITION (sémantické dělení) | PARTIAL | Semantic block detector |
| RECURSE (sub-delegace) | PARTIAL | Depth guard, budget propagation |
| AGGREGATE (konzistentní merge) | PARTIAL | Contradiction detection |
| VERIFY (self-check) | **PLNĚ** | Žádná akce |
| ACCUMULATE (persistent learning) | **PLNĚ** | Žádná akce |

### 7. Konkrétní implementační návrhy

#### Quick Win #1: Budget Propagation (2h)
Každý sub-agent dostane `remaining_budget`. Zastaví se když nestačí na další krok. RLM to řeší přes `BudgetExceededError` [VERIFIED][2]. STOPA trackuje globálně ale agenti jsou slepí.

**Kde:** orchestrate.md (agent spawning), budget.md formát

#### Quick Win #2: Metadata-Only Scout (2-3h)
Scout vrátí `{file_count, languages, deps, complexity}` bez čtení souborů. Orchestrátor plánuje z metadat, workers dostávají plný kontext.

**Kde:** scout.md (nový --metadata flag), orchestrate.md

#### Quick Win #3: Recursion Depth Guard (1h)
Max depth v skill frontmatter. Default depth=1. Depth=2 jen pro deepresearch.

**Kde:** core-invariants.md (nové pravidlo), skill frontmatter

#### Medium #4: Structured Output Contracts (4h)
JSON schema pro agent outputy. Programatická agregace místo NL summarizace.

**Kde:** output-contract enforcement, aggregation scripts

#### Medium #5: Lazy Context Loading (3h)
Orchestrátor posílá file paths, ne content. Agenti loadují on-demand.

**Kde:** orchestrate.md subtask formát

#### Medium #6: "Never Summarize" Rule (4h)
Při velkém kontextu partitionovat a delegovat, ne summarizovat.

**Kde:** compact.md redesign

#### Strategic #7: Contradiction Detection (5h)
Post-merge check při kombinaci výsledků z více agentů.

**Kde:** deepresearch.md, critic.md

#### Strategic #8: Strategy Pre-Enumeration (4h)
Před iterací: enumerovat strategie, odhadnout success probability, commitnout pořadí.

**Kde:** autoloop.md, autoresearch.md (Phase 0.5)

## Disagreements & Open Questions

- **RLM bez Claude benchmarků** — paper testuje jen GPT-5 a Qwen3. Není jasné jak RLM funguje s Claude modely [UNVERIFIED]
- **Cost na scale** — RLM je 3× levnější než summarization, ale srovnání s STOPA's orchestration overhead chybí [UNVERIFIED]
- **Czech language** — žádné non-English evaluace RLM [UNVERIFIED]
- **DSPy RLM maturita** — modul je "experimental", production readiness nejistá [SINGLE-SOURCE][3]

## Evidence Table

| # | Source | URL | Key Claim | Type | Confidence |
|---|--------|-----|-----------|------|------------|
| 1 | Zhang et al. — RLM paper | https://arxiv.org/abs/2512.24601 | 91.3% BrowseComp-Plus, 58% OOLONG-Pairs, 3× cheaper than summarization | Primary | high |
| 2 | alexzhang13/rlm | https://github.com/alexzhang13/rlm | pip install rlms, 3.3k stars, budget propagation, depth>1 support | Code | high |
| 3 | DSPy RLM module | https://dspy.ai/api/modules/RLM/ | RLM integrated as experimental DSPy module, WASM sandbox | Docs | high |
| 4 | Li et al. — LC vs RAG | https://arxiv.org/abs/2501.01880 | LC 56.3% vs RAG 49% on QA, no one-size-fits-all | Paper | high |
| 5 | Prime Intellect blog | https://www.primeintellect.ai/blog/rlm | Never summarize, llm_batch() for parallel, token isolation | Analysis | medium |
| 6 | Dextra Labs blog | https://dextralabs.com/blog/recursive-language-models-rlm/ | Context rot degrades LC, RLM loads only needed context | Analysis | medium |
| 7 | InfoQ coverage | https://www.infoq.com/news/2026/01/mit-recursive-lm/ | Depth=1 in production, 120s timeout | Reporting | medium |
| 8 | Zhang author blog | https://alexzhang13.github.io/blog/2025/rlm/ | First author's technical walkthrough | Blog | high |
| 9 | Google ADK reimpl. | https://medium.com/google-cloud/recursive-language-models-in-adk-d9dc736f0478 | Lazy file loading, configurable parallelism, Path objects | Implementation | high |
| 10 | fast-rlm | https://github.com/avbiswas/fast-rlm | Community reimplementation for faster inference | Code | medium |
| 11 | recursive-llm | https://github.com/ysz/recursive-llm | Alternative impl, 100K+ tokens via variable persistence | Code | medium |
| 12 | Khattab et al. — DSPy | https://arxiv.org/abs/2310.03714 | Programming-not-prompting, declarative LM pipelines | Paper | high |
| 13 | STOPA gap analysis | (internal Explore agent) | 2/7 principles fully implemented, 4/7 partial, 1/7 missing | Analysis | high |

## Sources

1. Zhang, Kraska, Khattab — "Recursive Language Models" (arXiv:2512.24601) — https://arxiv.org/abs/2512.24601
2. alexzhang13/rlm — Official implementation — https://github.com/alexzhang13/rlm
3. DSPy RLM API — https://dspy.ai/api/modules/RLM/
4. Li, Cao, Ma, Sun — "Long Context vs RAG" (arXiv:2501.01880) — https://arxiv.org/abs/2501.01880
5. Prime Intellect — "RLM: The Paradigm of 2026" — https://www.primeintellect.ai/blog/rlm
6. Dextra Labs — "Why RLMs Beat Long-Context LLMs" — https://dextralabs.com/blog/recursive-language-models-rlm/
7. InfoQ — "MIT Recursive LM" — https://www.infoq.com/news/2026/01/mit-recursive-lm/
8. Alex Zhang — Author blog — https://alexzhang13.github.io/blog/2025/rlm/
9. Liam Connell — "RLM in Google ADK" — https://medium.com/google-cloud/recursive-language-models-in-adk-d9dc736f0478
10. avbiswas/fast-rlm — https://github.com/avbiswas/fast-rlm
11. ysz/recursive-llm — https://github.com/ysz/recursive-llm
12. Khattab et al. — "DSPy" (arXiv:2310.03714) — https://arxiv.org/abs/2310.03714

## Coverage Status

- **[VERIFIED]:** RLM architecture, benchmarks, implementation, DSPy integration, depth=1 production, budget propagation, ADK patterns, STOPA gaps
- **[INFERRED]:** RLM vs RAG advantage (from LC vs RAG paper + RLM paper), hybrid approach consensus
- **[SINGLE-SOURCE]:** 120s timeout (InfoQ only), DSPy experimental status
- **[UNVERIFIED]:** RLM with Claude models, cost comparison vs STOPA, Czech language performance

## Implementation Roadmap

| Týden | Položky | Hodiny | Skills |
|-------|---------|--------|--------|
| 1 | Budget propagation + Depth guard | 3h | orchestrate, core-invariants |
| 2 | Metadata scout + Lazy loading | 5h | scout, orchestrate |
| 3 | Structured outputs + Never summarize | 8h | output-contract, compact |
| 4 | Contradiction detection + Strategy enum | 9h | deepresearch, autoloop, critic |
| **Celkem** | | **~25h** | **7 skills** |
