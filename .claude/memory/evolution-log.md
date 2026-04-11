# Evolution Log

Record of /evolve audit proposals and outcomes.

---

## Evolution Run — 2026-04-11 (#6, post-dreams)

### Signals
- 12 corrections (0 new since evolve #5)
- 2 violations (0 new)
- ~97 learnings scanned (+2 meta-patterns created by this run)
- /dreams ran first: 8 cross-links, 1 backward update, 3 emerging patterns
- 1 model_gate learning (sonnet-4.6, correctly scoped)
- Wiki 3 days stale (2026-04-08), ~22 new learnings since build
- Sessions: 100/100 healthy (0 corrections, 0 frustrations)

### Proposals
- 5 proposed, 5 approved, 0 rejected

### Applied
- CREATE: `2026-04-11-iteration-paradox-meta-pattern.md` — consolidates 5 learnings about iteration strategy into coherent protocol (skill_scope: autoloop, autoresearch, self-evolve)
- CREATE: `2026-04-11-verification-shift-meta-pattern.md` — consolidates 4 learnings about verification being the new bottleneck (skill_scope: critic, verify, harness, eval)
- UPDATE: Renamed 7 legacy learning files with date prefix (git mv, 2026-03-23/24)
- UPDATE: Fixed `related:` pointers in 2 files referencing renamed legacy files
- DEFER: heartbeat/BIGMAS graduation — still at 0% utility ratio (per evolve #5 decision)
- RECOMMEND: Run /compile (wiki 3 days stale, ~22 new learnings since 2026-04-08)

### Rejected
- (none)

### Notes
- Hook corruption incident: PostToolUse hooks ran from wrong cwd after `cd` in Bash, zeroed 2 files. Restored from git. Root cause: hooks use relative paths, `cd` changes cwd for the shell session.

---

## Evolution Run — 2026-04-11 (#5)

### Signals
- 12 corrections (0 new since evolve #4)
- 2 violations (0 new since 2026-03-29)
- 109 learnings scanned, 2 borderline graduation candidates (deferred — low utility ratio)
- 2 model_gate learnings: sonnet-4.6 (kept), triattention null (fixed)
- 0 panic episodes, 0 critic-accuracy entries, 0 skill-usage data
- Wiki 3 days stale, 28 new learnings since last build
- Sessions: all healthy (0 corrections, 0 frustrations across 20 recent sessions)

### Proposals
- 5 proposed, 5 approved, 0 rejected

### Applied
- FIX_DATA: Removed `model_gate: null` from triattention-pre-rope-kv-compression.md
- DEFER: Graduation of heartbeat + shared-public-state (uses:7 but utility 14% — wait for >30%)
- UPDATE_VERIFY: Analysis-Paralysis Guard (#6) verify changed to `manual`
- UPDATE_CONFIRMED: All 9 critical-patterns last_confirmed → 2026-04-11
- RECOMMEND: Run /compile (wiki 3 days stale, 28 new learnings since 2026-04-08 build)

### Rejected
- (none)

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

---

## Evolution Run — 2026-04-08 (#4)

### Signals
- 12 corrections (0 new since evolve #3)
- 2 violations (0 new since 2026-03-29)
- 81 learnings scanned, 0 graduation-ready (system 16 days old, uses still low)
- 2 model_gate learnings: sonnet-4.6 (correct), skill-retrieval-bottleneck (empty string — fixed)
- 0 panic episodes, 0 critic-accuracy entries, 0 skill-usage data, 0 discovered-patterns
- Wiki built 2026-04-08, 2 new learnings since (LH-Deception)
- Sessions: all healthy (0 corrections, 0 frustrations)

### Proposals
- 3 proposed, 3 approved, 0 rejected

### Applied
- FIX_DATA: Removed empty `model_gate: ""` from skill-retrieval-bottleneck.md
- RECOMMEND: /compile (2 new LH-Deception learnings since last build)
- AUTOMATE: Created scheduled task `weekly-evolve` (Monday 9:23, auto-run /evolve)
