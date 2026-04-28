---
name: WebArena
type: tool
first_seen: 2026-04-26
last_updated: 2026-04-26
sources: [ai-planning-framework-web-agents]
tags: [benchmark, evaluation, web-agents]
---

# WebArena

> Zhou et al. (2023, ICLR 2024) — benchmark 812 tasks pro autonomní web agenty napříč 5 doménami (e-commerce, Reddit, GitLab, CMS, OpenStreetMap); de facto standard pro web agent evaluaci.

## Key Facts

- 812 tasks, 5 domén: OneStopShop, Reddit, GitLab, CMS, OpenStreetMap (ref: sources/ai-planning-framework-web-agents.md)
- Progress: 14.41% (2023 baseline) → 61.7% SOTA 2026; agresivní saturace (ref: sources/ai-planning-framework-web-agents.md)
- Kritiky: brittle substring checkers (→WebArena Verified), sandbox-over-reporting (→Online-Mind2Web), no safety eval (→ST-WebAgentBench) (ref: sources/ai-planning-framework-web-agents.md)
- 83.2% tasks mají mixed outcomes across 6 agents — single-reference assumption invalid (ref: sources/ai-planning-framework-web-agents.md)
- ~161 tasks "inherently unachievable by design" — baseline interpretation problematic (ref: sources/ai-planning-framework-web-agents.md)

## Relevance to STOPA

Standard benchmark pro porovnání web orchestration approaches. Výsledky interpretovat opatrně: sandbox-over-reporting, brittle evaluators, mixed-outcome problem. Použít WebArena Verified Hard subset (137 tasks, -83% cost) pro rychlé iterace.

## Mentioned In

- [AI Planning Framework for LLM-Based Web Agents Research Brief](../sources/ai-planning-framework-web-agents.md)
