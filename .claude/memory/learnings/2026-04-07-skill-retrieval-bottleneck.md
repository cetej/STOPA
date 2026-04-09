---
date: 2026-04-07
type: best_practice
severity: high
component: skill
tags: [skill, retrieval, evaluation, self-evolve]
summary: "Skill description metadata alone is insufficient for agent self-discovery from large repositories. Two bottlenecks: (1) agents voluntarily load only 49% of relevant skills, (2) general-purpose skills can't be adapted without task context. Query-specific refinement (task-aware) recovers performance; offline refinement doesn't."
source: external_research
uses: 2
successful_uses: 0
harmful_uses: 0
confidence: 0.8
verify_check: manual
task_context: {task_class: research, complexity: low, tier: light}
---

## Detail

arXiv:2604.04323 benchmarks skill usage across 6 progressive realism conditions.
Claude Opus 4.6 drops from 55.4% (force-loaded) to 38.4% (realistic retrieval) — 3pp above no-skill baseline.

**Key finding**: the benefit of skills comes almost entirely from skill *loading*, not skill *content*.
When agents must choose which skills to load from metadata (description), they miss ~51% of relevant ones.

**Query-specific refinement** recovers this: agent explores task first, then evaluates and synthesizes retrieved skill.
Works when coverage score ≥3.83. Fails when score ≤3.49 (relevant skills absent from collection).

**STOPA implications**:
1. `description:` trigger routing is correct but insufficient for large-scale autodiscovery
2. `/self-evolve` pattern is empirically validated as the right refinement approach
3. For multi-project deployment: curated skill sets (stopa-orchestration plugin) outperform open retrieval — keep the plugin approach
4. Smaller models need simpler, more targeted skills than Opus
