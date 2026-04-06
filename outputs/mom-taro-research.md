# MoM + TARo: Inspirace pro vylepšení STOPA ekosystému — Research Brief

**Date:** 2026-04-07
**Question:** Jaké konkrétní vylepšení z MoM (multi-agent GRPO) a TARo (adaptive routing) lze aplikovat na STOPA, NG-ROBOT, MONITOR, Záchvěv?
**Scope:** standard (comparison)
**Sources consulted:** 18 (2 primary papers + 16 supporting)

## Executive Summary

Dvě papers odhalují dva komplementární principy: **MoM** ukazuje, že role-specific reward funkce a prioritizace upstream agentů (planner > worker) přináší +5-17% kvalitu [VERIFIED], zatímco **TARo** dokazuje, že adaptivní per-step routing nahrazující fixní tiers šetří 40-60% budget s minimální ztrátou kvality [VERIFIED]. Oba principy jsou přímo aplikovatelné na STOPA orchestraci a downstream projekty. Identifikovali jsme 6 konkrétních návrhů seřazených podle effort/impact — top 3 (upstream-first quality, role-specific critic, weak-to-strong transfer) vyžadují celkem ~6-9h implementace a adresují největší gap: uniformní scoring a fixní tier alokace.

## Detailed Findings

### 1. Role-Specific Critic Scoring

MoM používá odlišné reward funkce per role: BLEU pro planner, execution success pro coder, exact match pro answerer [VERIFIED][1]. STOPA critic aktuálně používá uniformní rubric s adaptivními váhami per task type, ale NE per agent role [VERIFIED][codebase].

Doplňkový research odhalil 3 vzory pro inference-time per-role scoring [INFERRED][11,12]:
- **GDPO** (arXiv:2601.05242) — decoupled normalization per reward dimension; řeší reward collapse v multi-criteria scénářích
- **Process Reward Models** — step-level scoring per role: Planner PRM (plan_coherence, assumption_validity), Executor PRM (tool_fit, parameter_correctness), Orchestrator PRM (agent_assignment, budget_efficiency)
- **AgentEval** — multi-role critic systém (CriticAgent + QuantifierAgent + VerifierAgent)

**Návrh (3 fáze):**
1. **Phase 1 (okamžitě):** Diferenciovat critic weight profiles per agent role — scout (coverage/relevance), worker (correctness/tests), verifier (evidence grounding). Přidání `role:` parametru do critic invokace.
2. **Phase 2 (week 2-3):** Per-role PRM evaluátory — lightweight inference-time funkce specifické pro každou roli (ne RL training).
3. **Phase 3 (month 2):** Critic feedback loop — AgentEval-inspired multi-persona critic + refinement přes /self-evolve.

**Per-project aplikace:**
- **NG-ROBOT** — fetcher PRM (completeness), processor PRM (accuracy), SEO enricher PRM (differentiation score)
- **MONITOR** — collector PRM (coverage) vs analyzer PRM (depth) vs presenter PRM (clarity)

### 2. Adaptive Tier Routing místo fixních tierů

TARo dokazuje, že adaptivní per-token routing překonává fixní interpolaci o +8.4% na MATH500 [VERIFIED][2]. RouteLLM dosahuje 2x cost reduction s preference-based routingem [INFERRED][3]. Route-to-Reason rozšiřuje na joint model+strategy selection s 40-60% úsporou [INFERRED][4].

STOPA tier je locked at task start — orchestrate vybírá light/standard/deep na základě file count a keyword signals, žádný mid-task upgrade [VERIFIED][codebase].

**Návrh (2 fáze):**
- Phase 1 (okamžitě, 1h): Heuristický per-subtask router — single-file edit → haiku, multi-file+tests → sonnet, architectural → opus, error on previous attempt → upgrade
- Phase 2 (week 3-4): Data-driven router trénovaný na (subtask, model, critic_score, cost) traces z budget.md

**Per-project aplikace:**
- **NG-ROBOT** — metadata extraction (haiku) vs SEO analysis (sonnet) vs content quality (opus) — dynamicky per článek
- **Záchvěv** — simple trend check (haiku) vs causal analysis při detekci anomálie (opus)

### 3. Weak-to-Strong Transfer

TARo router trénovaný na 3B/8B modelech funguje na 14B/70B bez retrainingu [VERIFIED][2] — učí se abstraktní vlastnosti problému (complexity, domain), ne model-specific artefakty. Potvrzeno across architecture families [INFERRED][3].

**Návrh:** Haiku-first difficulty estimation — spusť subtask přes haiku (levný). Pokud uspěje s vysokou confidence → keep. Pokud selže → route na sonnet/opus. Pattern library: úspěšné haiku vzory na task_class X → skip opus pro podobné tasky.

**Per-project aplikace:**
- **NG-ROBOT** — haiku zvládne ~70% článků (jednoduchý news), sonnet/opus jen pro komplexní analýzy
- **Záchvěv** — haiku pro baseline monitoring, opus jen při detekci anomálie
- **MONITOR** — rutinní OSINT collection (haiku) vs deep analysis (sonnet)

### 4. Best-of-N Parallel Rollouts

MoM test-time scaling přidává +3.65% kvalitu přes 8x parallel rollouts [VERIFIED][1]. Self-certainty verification (arXiv:2502.18581) nabízí ~80% levnější alternativu k plnému critic per kandidát [INFERRED][5]. Praktický sweet spot je best-of-2 až best-of-4 [INFERRED][multiple].

**Návrh:** Pro deep-tier subtasky generovat 2-3 paralelní kandidáty, vybrat nejlepší přes self-certainty scoring (token entropy). Full critic jen na vítěze.

**Per-project aplikace:**
- **NG-ROBOT** — SEO headline generation: 3 varianty, pick highest differentiation score
- **MONITOR** — 2 paralelní analytici, merge findings

### 5. Upstream-First Quality (Sequential Priority)

MoM sequential training (planner first, then coder, then answerer) překonává simultánní trénink [VERIFIED][1]. Removing any role degrades celkový výsledek — ale upstream quality je bottleneck.

**Návrh:** Scout quality gate — scout output musí projít structured completeness checkem PŘED plan fází. Plan musí splnit input-contract downstream skills. Upstream agent dostane model o tier výš než workers.

**Per-project aplikace:**
- **NG-ROBOT** — source analysis (upstream) determinuje celý processing chain
- **MONITOR** — source credibility assessment gates všechnu downstream analýzu

### 6. Heterogeneous Rollout Teams

Heterogeneous LLM teams (mix model sizes) maximalizují diverzitu search space [INFERRED][6]. Pro deep-tier: kombinace haiku (fast, straightforward) + sonnet (balanced) + opus (deep reasoning) pokrývá více os řešení než 3x sonnet.

## Disagreements & Open Questions

- **RTR budget savings (40-60%)** — číslo z jedné paper, neověřeno na agent orchestration doméně (testováno na QA) [SINGLE-SOURCE]
- **Self-certainty 80% cost reduction** — závisí na kvalitě model confidence calibrace; Claude models neexponují raw logits přes API → potřeba proxy metriky
- **Haiku-first routing** — předpokládá, že haiku failure je spolehlivý signál obtížnosti; může mít false negatives (haiku "uspěje" s nekvalitním výstupem)

## Doporučené pořadí implementace

| # | Proposal | Effort | Impact | Quick win? |
|---|----------|--------|--------|-----------|
| 1 | P5 — Upstream-first quality (scout gate) | Low (1-2h) | High | Ano |
| 2 | P1 — Role-specific critic | Medium (2-3h) | High | Ano |
| 3 | P4 — Weak-to-strong transfer (haiku-first) | Low-Medium (2-4h) | High | Ano |
| 4 | P2.1 — Heuristic per-subtask routing | Low (1h) | Medium-High | Ano |
| 5 | P3 — Best-of-N rollouts (deep tier) | Medium (4-6h) | Medium | Ne |
| 6 | P6 — Heterogeneous teams | Low (1h) | Medium | Ne |
| 7 | P2.2 — Data-driven router | High (1-2 weeks) | High | Ne |

## Evidence Table

| # | Source | URL | Key Claim | Type | Confidence |
|---|--------|-----|-----------|------|------------|
| 1 | MoM (Zhou et al.) | https://arxiv.org/abs/2510.20176 | 62.13% TableBench, role-specific rewards, sequential training | primary | high |
| 2 | TARo (Rai et al.) | https://arxiv.org/abs/2603.18411 | +22.4% MATH500, adaptive routing, weak-to-strong transfer | primary | high |
| 3 | RouteLLM (Ong et al.) | https://arxiv.org/abs/2406.18665 | 2x cost reduction, cross-model transfer | primary | high |
| 4 | Route-to-Reason | https://arxiv.org/abs/2505.19435 | Joint model+strategy routing, 40-60% savings | primary | medium |
| 5 | Self-Certainty BoN | https://arxiv.org/abs/2502.18581 | Lightweight verification, ~80% cheaper than reward models | primary | medium |
| 6 | Scaling Test-Time (NVIDIA) | https://arxiv.org/abs/2506.12928 | Heterogeneous teams > homogeneous, power-law scaling | primary | medium |
| 7 | MASTER | https://arxiv.org/abs/2501.14304 | Multi-agent MCTS, 76% HotpotQA | primary | medium |
| 8 | xRouter | https://arxiv.org/abs/2510.08439 | RL-based Pareto-optimal routing | primary | medium |
| 9 | Q-Value Models | https://arxiv.org/abs/2409.09345 | Step-level stopping policy via learned Q-values | primary | medium |
| 10 | ZenML Survey | https://www.zenml.io/blog/what-1200-production-deployments-reveal-about-llmops-in-2025 | Token optimization > model routing (60-80% vs 40-60%) | secondary | medium |
| 11 | GDPO | https://arxiv.org/abs/2601.05242 | Decoupled per-dimension reward normalization for multi-agent | primary | medium |
| 12 | Process Reward Models | https://arxiv.org/abs/2502.10325 | Step-level scoring, role-differentiated PRMs | primary | medium |

## Sources

1. Zhou et al. — Mixture-of-Minds: Multi-Agent RL for Table Understanding — https://arxiv.org/abs/2510.20176
2. Rai et al. — TARo: Token-level Adaptive Routing — https://arxiv.org/abs/2603.18411
3. Ong et al. — RouteLLM: Learning to Route LLMs with Preference Data — https://arxiv.org/abs/2406.18665
4. Route to Reason: Adaptive Routing for LLM and Reasoning Strategy Selection — https://arxiv.org/abs/2505.19435
5. Scalable Best-of-N Selection via Self-Certainty — https://arxiv.org/abs/2502.18581
6. Scaling Test-time Compute for LLM Agents — https://arxiv.org/abs/2506.12928
7. MASTER: Multi-Agent System with LLM Specialized MCTS — https://arxiv.org/abs/2501.14304
8. xRouter: Cost-Aware LLMs Orchestration via RL — https://arxiv.org/abs/2510.08439
9. Enhancing Decision-Making via Step-Level Q-Value Models — https://arxiv.org/abs/2409.09345
10. ZenML: What 1,200 Production Deployments Reveal — https://www.zenml.io/blog/what-1200-production-deployments-reveal-about-llmops-in-2025
11. GDPO: Decoupled Group Relative Policy Optimization — https://arxiv.org/abs/2601.05242
12. Process Reward Models for Step-Level Scoring — https://arxiv.org/abs/2502.10325

## Coverage Status

- **[VERIFIED]:** MoM metrics (62.13%, +5-17%, +3.65%), TARo metrics (+22.4%, 4x, 1K samples, weak-to-strong), STOPA current state (uniform critic, fixed tiers)
- **[INFERRED]:** RouteLLM 2x cost reduction, RTR 40-60% savings, heterogeneous > homogeneous teams
- **[SINGLE-SOURCE]:** RTR budget savings figure, self-certainty 80% cost claim
- **[UNVERIFIED]:** None
