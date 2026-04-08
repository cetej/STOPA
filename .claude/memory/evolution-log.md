# Evolution Log

Record of /evolve audit proposals and outcomes.

---

## Evolution Run — 2026-04-01

First /evolve run (100 sessions accumulated).

### Signals
- 8 corrections in corrections.jsonl (2 clusters: verify-before-done, secrets)
- 2 violations (secrets false positive, analysis-paralysis verify mismatch)
- 25 learnings scanned, 0 graduation-ready (all uses: 0, system too new)
- No skill-usage.jsonl tracking yet

### Proposals
- 3 proposed, 2 approved, 0 rejected, 1 resolved (already fixed)

### Applied
- INVESTIGATE: API key matches in .claude/ — false positive (self-reference in violations.jsonl + backups/)
- FIX_VERIFY: Analysis-Paralysis Guard — already had `verify: manual`, no change needed
- CREATE: evolution-log.md — this file

### Deferred
- Skill-usage tracking hook — system too young, revisit when target projects actively use skills

---

## Evolution Run — 2026-04-05

Focused audit triggered by overlap detection between two skill-component learnings.

### Signals
- 12 corrections (no new clusters beyond already-covered patterns)
- 2 violations (both resolved in previous run)
- 55 learnings scanned, 0 graduation-ready (max uses: 1, system 13 days old)
- 1 model_gate learning (sonnet-4.6), correctly scoped
- Wiki 1 day fresh (2026-04-04), 1 new learning since

### Proposals
- 3 proposed, 2 approved, 1 rejected

### Applied
- UPDATE: Added `related:` pointer from anthropic-skill-creator-patterns → description-optimizer-plan
- UPDATE: Added `related:` pointer from description-optimizer-plan → anthropic-skill-creator-patterns (reciprocal)

### Rejected
- REVIEW: sonnet46-thinking model_gate — gate is correctly scoped to Sonnet, content also covered by critical-patterns #9 for universal access

---

## Evolution Run — 2026-04-08

### Signals
- 12 corrections (no new clusters since evolve #2 — mostly article ingestion + project frustrations)
- 2 violations (both resolved in previous runs, 0 new since 2026-03-29)
- 70 learnings scanned, 0 graduation-ready (max uses=1, system 16 days old)
- 1 model_gate learning (sonnet-4.6), correctly scoped
- 3 supersedes chains active and correct
- Wiki 1 day stale (2026-04-07), 4 new learnings since
- No panic-episodes, critic-accuracy, skill-usage, discovered-patterns data yet

### Proposals
- 5 proposed, 5 approved, 0 rejected

### Applied
- PRUNE: critical-patterns #8 (3-Fix Escalation) — redundant with core-invariants #7, freed 1 slot (now 9/10)
- ADD_VERIFY: critical-patterns #8 (formerly #9, Sonnet 4.6) — added machine-checkable verify: Grep("model_gate.*sonnet")
- RESOLVE: improvement-queue dedup budget-calibration — already handled by supersedes: field
- RESOLVE: improvement-queue dedup skill-creator — already linked via related: pointers (evolve #2)
- RECOMMEND: /compile (4 new learnings since wiki build 2026-04-07)

### Renumbering
- Old #8 (3-Fix Escalation): REMOVED
- Old #9 (Sonnet 4.6): → new #8
- Old #10 (Anti-Hallucination): → new #9
- critical-patterns now at 9/10 capacity (1 free slot)
