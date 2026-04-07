---
name: NLAH (Natural-Language Agent Harness)
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [nlah-research]
tags: [orchestration, skill-design, context-engineering]
---

# NLAH (Natural-Language Agent Harness)

> Pan et al. (arXiv:2603.25723, Tsinghua + Harbin IT, 2026) — orchestrační logika jako explicitní přenositelný NL artefakt místo controller kódu. 6 komponent: Contracts, Roles, Stage structure, Adapters/scripts, State semantics, Failure taxonomy.

## Key Facts

- Migrace kódu na NLAH: 30.4% → 47.2% na OSWorld — topologický shift (file-backed state + artifact verifikace vs. screenshot-grounded repair) (ref: sources/nlah-research.md)
- 6 komponent: Contracts, Roles, Stage structure, Adapters/scripts, State semantics, Failure taxonomy
- 90% prompt tokenů a tool calls se děje v delegovaných child agentech — IHR je koordinátor
- STOPA SKILL.md soubory jsou v podstatě NLAHs — akademická validace empiricky vyvinutého přístupu
- Evaluace na subsetech: 125 SWE-bench, 36 OSWorld — ne plné suity
- Verifier modul způsobil -0.8% na SWE-bench — extra struktura může škodit

## Relevance to STOPA

Přímá akademická validace celého STOPA SKILL.md designu. NLAH komponenty korespondují: Contracts → allowed-tools/permission-tier, Roles → sub-agenti s explicit model choice, Stage structure → PLAN→WORK→ASSESS→COMPOUND, Failure taxonomy → 3-fix escalation + circuit breakers. Paper poskytuje "harness representation science" jazyk pro popis STOPA skillů.

## Mentioned In

- [NLAH Research Brief](../sources/nlah-research.md)
