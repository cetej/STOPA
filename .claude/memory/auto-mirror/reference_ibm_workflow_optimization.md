---
name: IBM Workflow Optimization Survey
description: Survey paper mapping static-to-dynamic spectrum for LLM agent workflows — directly relevant to STOPA orchestrate design
type: reference
---

## Paper

- **Title:** From Static Templates to Dynamic Runtime Graphs: A Survey of Workflow Optimization for LLM Agents
- **Authors:** Ling Yue, Kushal Raj Bhandari, Ching-Yun Ko, Dhaval Patel et al. (IBM Research)
- **Link:** https://arxiv.org/abs/2603.22386
- **Date discovered:** 2026-03-28

## 3 organizační osy

1. **Kdy** se struktura určí — statické šablony vs. dynamické runtime grafy
2. **Co** se optimalizuje — které komponenty workflow
3. **Jaké signály** řídí optimalizaci — task metriky, verifier feedback, preference, trace-derived insights

## Klíčové koncepty

- **Reusable workflow templates** — generalizovatelné design patterns (= naše budget tiers)
- **Run-specific realized graphs** — deployed struktury pro konkrétní instanci
- **Execution traces** — skutečné runtime chování (= to co STOPA zatím nezachycuje)
- **Structure-aware evaluation** — hodnocení přes vlastnosti grafu, execution cost, robustnost, strukturální variaci

## Implikace pro STOPA

STOPA orchestrate sedí na statickém konci spektra. Paper identifikuje 3 mezery:
1. **Trace-based optimalizace** — analyzovat minulé orchestrace pro lepší budoucí výběr
2. **Verifier-guided restrukturalizace** — místo circuit breaker STOP → přestavba workflow
3. **Learned tier selection** — mapping task charakteristik → optimální tier (ne statický výběr)
