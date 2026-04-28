---
name: trajectory-eval-metrics
type: concept
first_seen: 2026-04-26
last_updated: 2026-04-26
sources: [ai-planning-framework-web-agents]
tags: [evaluation, trajectory, orchestration, metrics]
---

# Trajectory Evaluation Metrics (beyond binary success)

> Cluster metrik pro hodnocení kvality agent trajektorie nad rámec binárního task success/fail — zahrnuje S&D (2026) sadu 5 metrik + komplementární přístupy z literatury.

## Key Facts

**S&D (2026) 5 metrik:**
- Recovery Rate = (1/#tasks) Σ [# recoveries / # deviations] — 5-step lookahead (ref: sources/ai-planning-framework-web-agents.md)
- Repetitiveness = 1 − (1/#tasks) Σ [# repetitive / # actions] (ref: sources/ai-planning-framework-web-agents.md)
- Step Success Rate = (1/#tasks) Σ [# matched gold steps / # gold steps] (ref: sources/ai-planning-framework-web-agents.md)
- Element Accuracy = (1/#tasks) Σ [# matching predicted/actual / # agent steps] (ref: sources/ai-planning-framework-web-agents.md)
- Partial Success = (1/#req_tasks) Σ [# completed reqs / # reqs] (ref: sources/ai-planning-framework-web-agents.md)

**Unique differentiators vs 2024-2026 frameworks:** Element Accuracy a Recovery Rate nemají ekvivalent v AgentRewardBench, WebGraphEval, TRACE, WebArena Verified, Online-Mind2Web (ref: sources/ai-planning-framework-web-agents.md)

**Efficiency metric (Online-Mind2Web):** E = mean(steps/reference_steps) na úspěšných tascích (ref: sources/ai-planning-framework-web-agents.md)

## Relevance to STOPA

Recovery Rate lze adaptovat pro STOPA eval traces: Recovery@n = (critic_FAIL_events recovered) / (critic_FAIL_events total). Adresuje gap z INDEX.md: "trajectory auditing" jako open gap v STOPA knowledge base.

## Mentioned In

- [AI Planning Framework for LLM-Based Web Agents Research Brief](../sources/ai-planning-framework-web-agents.md)
