---
saved: "2026-04-07T20:15"
session_id: "s-20260407-mom-taro-phase2"
task_ref: "mom-taro-phase2"
branch: main
progress:
  completed: ["p3-best-of-n-rollouts", "p6-heterogeneous-teams", "p1.2-per-role-prms", "sync", "commit-push"]
  in_progress: []
  blocked: []
artifacts_modified:
  - .claude/commands/orchestrate.md
  - .claude/commands/critic.md
keywords:
  - MoM
  - TARo
  - best-of-N
  - heterogeneous-teams
  - PRM
  - GDPO
  - orchestrate
  - critic
resume:
  next_action: "Phase 2 complete. Remaining: P2.2 data-driven router (1-2 weeks, needs trace data)"
  blockers: []
  decisions_pending: []
  failed_approaches: []
---

# Session Checkpoint

**Saved**: 2026-04-07 ~20:15
**Task**: MoM + TARo → orchestration upgrades (Phase 2 done)
**Branch**: main
**Progress**: Phase 2 complete (3/3 proposals implemented)

## Co je hotovo

### Phase 1 (commit 97d8512)
- **P5 Scout Quality Gate** — orchestrate.md Phase 2: tier-scaled completeness checks
- **P1 Role-Specific Critic** — critic.md Phase 4: weight profiles per role
- **P2.1 Per-Subtask Adaptive Routing** — orchestrate.md Phase 4: heuristic router
- **P4 Haiku-First Difficulty Estimation** — orchestrate.md Phase 4: cheap probe + escalation

### Phase 2 (this session)
- **P3 Best-of-N Parallel Rollouts** — orchestrate.md Phase 4: spawn 2-3 agents per deep-tier subtask, rank via critic score (not self-certainty), select best. Includes N selection table, execution protocol, merge-vs-select rules, budget guards.
- **P6 Heterogeneous Rollout Teams** — integrated into P3: mix haiku+sonnet+opus within rollout waves for maximum search space diversity. Team composition tables for N=2 and N=3.
- **P1.2 Per-Role PRMs** — critic.md: GDPO-inspired lightweight inference-time scoring functions per role (plan_coherence, impl_correctness, evidence_depth, source_quality). Fast pre-filter at ~10% cost of full critic. GDPO normalization for cross-role comparison.
- Sync commands/ ↔ skills/ ↔ stopa-orchestration/ — verified identical

## Co zbývá

| # | Proposal | Effort | Impact | Notes |
|---|----------|--------|--------|-------|
| P2.2 | Data-driven router | 1-2 weeks | High | Scheduled task `p22-router-trace-check` (po+čt 10:00) sleduje akumulaci traces. Notifikuje při 50+ záznamech. |

## Co NEdělat

- Neměnit Phase 1 nebo Phase 2 implementace — ověřeny
- Self-certainty BoN závisí na raw logits — Claude API je nemá, proto critic-based selection
- Nearchivovat research files v `outputs/.research/`

## Resume Prompt

> MoM+TARo orchestration upgrades complete (Phase 1 + Phase 2). All 7 proposals implemented except P2.2 (data-driven router — needs trace data, 1-2 weeks effort). Files: orchestrate.md (Best-of-N, heterogeneous teams, adaptive routing, haiku-first), critic.md (role-specific weights, per-role PRMs). Next: collect traces from budget.md to train P2.2 router.

---
## Session Detail Log

### Changes Made
- orchestrate.md: +45 lines (Best-of-N Parallel Rollouts section with heterogeneous teams)
- critic.md: +30 lines (Per-Role PRM section with GDPO normalization)
- Synced to 4 locations (commands/, skills/, stopa-orchestration/)
