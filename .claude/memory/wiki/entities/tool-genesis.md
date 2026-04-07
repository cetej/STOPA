---
name: Tool-Genesis
type: paper
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [toolgenesis-research]
tags: [testing, orchestration, tool-creation, benchmarks]
---

# Tool-Genesis

> Xia et al. 2026 (arXiv:2603.05578) — diagnostický benchmark pro autonomní tvorbu nástrojů z abstraktních požadavků: 2,150 úkolů, 86 MCP serverů, čtyřúrovňové metriky L1–L4.

## Key Facts

- 2,150 úkolů, 86 spustitelných MCP serverů, 508 nástrojů, 24 doménových tříd, 9,441 unit testů (ref: sources/toolgenesis-research.md)
- Čtyřúrovňová evaluace: L1 Surface Compliance, L2 Semantic Interface Fidelity, L3 Functional Correctness, L4 Downstream Utility — první benchmark evaluující každou fázi pipeliny zvlášť
- Nejlepší Direct SR: GPT-5.1 0.372; Code-Agent SR: Qwen3-235B 0.622 (open-source vede)
- Schema-utility decoupling: Claude-Haiku-3.5 Schema-F1 0.964 ale SR jen 0.472 — povrchová správnost schématu nepredikuje downstream úspěch
- Scale reversal: větší modely lépe exploitují execution feedback, ale nejsou nutně lepší v one-shot generování
- 5.7× větší než TM-Bench (nejbližší předchůdce)

## Relevance to STOPA

Validuje STOPA 3-fix escalation pattern (Code-Agent = ReAct repair loop). Potvrzuje pravidlo v CLAUDE.md: iterativní úlohy → silnější model. Schema-utility decoupling varuje před spoléháním na syntaktické metriky v /critic. Cascadový efekt L1→L4 odpovídá STOPA scout quality gate designu.

## Mentioned In

- [Tool-Genesis Research Brief](../sources/toolgenesis-research.md)
