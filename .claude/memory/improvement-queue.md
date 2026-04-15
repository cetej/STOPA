# Improvement Queue

Generated: 2026-04-15 03:23

## Dedup Clusters for next /evolve (2026-04-15)

Autodream identified 24 dedup pairs across 4 clusters. Requires human judgment to merge — present to user for approval.

| Cluster | Size | Files | Action |
|---------|------|-------|--------|
| Deception/trust | 5 pairs | agent-deception-pressure-trigger, long-horizon-deception-eval, model-size-negatively-correlated-honesty, sycophancy-not-hallucination, fresh-session-self-report-verification | Merge into 1-2 deception learnings |
| AutoLoop iteration | 4 pairs | autoagent-overfitting-guard, iteration-paradox-meta-pattern, experience-replay-outcomes-reuse, generate-then-discard-suboptimal | Keep 1-2, archive rest |
| Context-sharing | 3 pairs | compression-regime-maps-to-tiers, speculative-reasoning-degrades-workers, task-guided-context-beats-raw-sharing | Review overlap, possibly merge 2 |
| Latent space | 1 pair | latent-deterministic-boundary, latent-deterministic-extraction | High-probability merge candidate |

| Priority | Type | Pattern | Count | Action |
|----------|------|---------|-------|--------|
| 3 | violation | NEVER write API keys/tokens into JSON config files. Use environment variables or | 1 | fix rule or code |
| 3 | violation | 6. Analysis-Paralysis Guard | 1 | fix rule or code |
| 3 | violation | Setting CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=70 triggers context compaction earlier ( | 1 | fix rule or code |
| 3 | violation | AutoAgent's anti-overfitting guard: ask 'if this exact eval case disappeared, wo | 1 | fix rule or code |
| 3 | violation | Tool-Genesis (arXiv:2603.05578) prokázal cascade failure — drobné L1 chyby zesil | 1 | fix rule or code |
| 3 | violation | stale reference: .claude/memory/implementation-plan.md | 1 | fix rule or code |
| 3 | violation | stale reference: .claude/memory/intermediate/panic-episodes.jsonl | 1 | fix rule or code |
| 3 | violation | stale reference: .claude/memory/intermediate/scratchpad.md | 1 | fix rule or code |
| 3 | violation | stale reference: .claude/memory/wiki/.compile | 1 | fix rule or code |
| 3 | violation | stale reference: .claude/memory/briefings/orchestration.md | 1 | fix rule or code |
