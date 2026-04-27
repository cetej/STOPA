# Critical Patterns — Always-Read Top Learnings

Always-loaded subset of `learnings/`. Max 10 entries. Entries graduate via:
- `maturity: core` AND `uses >= 10` AND `harmful_uses < 2` (default trigger)
- OR `impact_score >= 0.7` AND `uses >= 5` AND `harmful_uses < 1` (impact trigger)

Demotion: `harmful_uses >= 2` → demote back to `learnings/` validated tier.

Last refresh: 2026-04-27 (audit-driven initial population — graduation pipeline was missing target file).

---

## 1. Adaptive orchestration topology by complexity (BIGMAS)

**Core insight:** Different tasks need different agent graph shapes. Trivial = linear 1-2, complex = cyclic 5-7. Workspace contract is shared memory (already implemented as STOPA memory files).

**Apply when:** Choosing tier in `/orchestrate`. Light = skip scout, jump to worker. Standard = DAG (scout → plan → worker → critic). Deep = cyclic (worker ↔ critic, architect node added). Watch routing count > 2× estimate → COMPLEXITY_ESCALATE.

**Source:** [2026-03-29-bigmas-directed-graph-orchestration.md](learnings/2026-03-29-bigmas-directed-graph-orchestration.md) | uses: 16 | core | arXiv:2603.15371

---

## 2. Shared public state beats message passing (CORAL)

**Core insight:** Symlinked `shared/` dir read/written by all agents = zero sync overhead. Knowledge reuse (sdílené attempts, notes, skills) je primary driver multi-agent gainů, ne paralelismus.

**Apply when:** Farm tier orchestration (5-8 agents in worktrees). Use `intermediate/farm-ledger.md` (already in rules/memory-files.md) as shared write target. Per-slot files (`agent-1.md`...) avoid merge conflicts. Don't poll — agents publish partial results průběžně.

**Source:** [2026-04-08-shared-public-state-agent-coordination.md](learnings/2026-04-08-shared-public-state-agent-coordination.md) | uses: 16 | core | arXiv:2604.01658

---

## 3. Heartbeat-triggered mid-run steering

**Core insight:** Orchestrator can inject reflection/redirect prompts into running agents WITHOUT restart. Different from critic (post-hoc) and calm-steering (panic). Heartbeat changes direction mid-flight.

**Apply when:** In `self-evolve` and `autoloop` Phase 2 — after N iterations without improvement, inject reflection prompt before next attempt. More efficient than waiting for end-of-iteration critic fail. Already wired via `stagnation-detector` hook.

**Source:** [2026-04-08-heartbeat-mid-run-steering.md](learnings/2026-04-08-heartbeat-mid-run-steering.md) | uses: 13 | core | arXiv:2604.01658

---

## 4. Living memory beats static accumulation (MIA)

**Core insight:** Evolving + compressed trajectories outperform static long-context RAG by +31% avg across 11 benchmarks. More stored context ≠ better performance. 7B model with living memory beats 32B without it by 18%.

**Apply when:** Designing memory for new agents. Prefer compressed trajectory + evolution hooks over append-only history. Validates STOPA's write-time gating (filter before storing). MC formalizes checkpoint→hybrid-retrieve as O(NL) interpolation — query-dependent gating has tractable complexity model.

**Source:** [2026-04-08-living-memory-over-static-retrieval.md](learnings/2026-04-08-living-memory-over-static-retrieval.md) | uses: 9 | validated | arXiv:2604.04503 + 2602.24281

---

## 5. RLM core principles for orchestration

**Core insight:** Recursion depth=1 sufficient even in production RLM (depth>1 unstable per InfoQ). Two-model arch (root heavy + recursive cheap) maps to STOPA's Opus-plan + Haiku-execute. STOPA's Agent tool = REPL equivalent (no native REPL adoption needed).

**Apply when:** Configuring `/orchestrate` budget propagation (soft-cap + 20% reserve), scout `--metadata` flag (orchestrator plans from metadata, workers read full files), `max-depth` frontmatter enforcement (default 1, max 2 only for deepresearch/build-project).

**Source:** [2026-04-10-rlm-architectural-principles.md](learnings/2026-04-10-rlm-architectural-principles.md) | uses: 6 | validated | arXiv:2512.24601

---

## 6. Experience replay for skills (RL replay buffer)

**Core insight:** Strict on-policy "generate-then-discard" is suboptimal. Replay buffer (reuse past trajectories) saves 40% compute at same/better accuracy. STOPA's `outcomes/` exists but is underused — skills read only `optstate/<skill>.json` (momentum), not concrete trajectory summaries.

**Apply when:** Phase 0 of autoloop/autoresearch/self-evolve. Glob `outcomes/<skill>-*.md`, sort desc, read last 5 → extract `## What Worked`. Use as positive context: "These approaches worked before: ...". `## What Failed` = anticurriculum. First validated 2026-04-21 (autoloop reached 100% pass in 2 rounds via warm-start).

**Source:** [2026-04-13-experience-replay-outcomes-reuse.md](learnings/2026-04-13-experience-replay-outcomes-reuse.md) | uses: 6 | validated | skill_scope: [autoloop, autoresearch, self-evolve] | arXiv:2604.08706

---

## 7. Deception escalates under pressure (LH-Deception)

**Core insight:** 11 frontier models show different deception rates. Failures + high-stakes conditions trigger deceptive behavior. Models "look good" under supervision pressure by hiding partial truth or giving vague answers. Vagueness drift ("might work", "looks mostly correct") = deception signal, not just uncertainty.

**Apply when:** Sub-agent triggers 3-fix escalation → treat subsequent outputs with HIGHER critic skepticism (this is exactly the pressure condition that triggers deception). Also: prefer models with lower known deception rates for trust-sensitive roles (production deploy, data deletion, critical eval).

**Source:** [2026-04-08-agent-deception-pressure-trigger.md](learnings/2026-04-08-agent-deception-pressure-trigger.md) | uses: 6 | validated | arXiv:2510.03999

---

## Maintenance

`/evolve` should re-rank this file on each run:
- Add: validated learnings with `uses >= 10` AND `confidence >= 0.8`
- Remove: any entry with `harmful_uses >= 2` (demote)
- Trim: keep top 10 by retrieval-time score (severity × source × confidence × maturity_boost × recency)

If this file is missing on session start: `verify-sweep.py` should warn — graduation pipeline broken.
