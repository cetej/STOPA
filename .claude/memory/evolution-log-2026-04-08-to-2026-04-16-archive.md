# Evolution Log

## Evolution Run — 2026-04-16 (#13)

### Signals
- 12 corrections (0 new since #11 — stable 15+ days)
- 28 violations (unchanged — 23 stale refs delegated as tech-debt, 5 historical)
- 163 learnings scanned (+1 since #12: cpmi-process-reward)
- 1 graduation candidate: bigmas (uses=10, validated, conf=1.0, harmful=0)
- 0 maturity draft→validated (all uses≥5 already validated)
- 0 prune candidates (0 learnings below 0.3 confidence)
- 0 harmful_uses ≥1 across all 163 learnings
- Sessions: 10/10 healthy today (0 corrections, 0 frustrations, 0 violations)
- Replay queue: empty
- Panic episodes file does not exist

### Proposals
- 2 proposed, 2 approved, 0 rejected, 2 deferred (CP promotion, /compile recommendation)

### Applied
- MATURITY: bigmas-directed-graph-orchestration.md → core (uses=10, conf=1.0, harmful=0)
- CLEANUP: improvement-queue.md — removed 5 stale references to runtime-created files (implementation-plan.md, scratchpad.md, panic-episodes.jsonl, wiki/.compile, briefings/*); kept 5 real violations with ALREADY_COVERED/stale notes

### Deferred
- CP promotion for bigmas — critical-patterns at 10/10 capacity, implementation already in orchestrate SKILL.md Phase 3.3, no need to duplicate
- /compile run — recommended as next step outside evolve scope (wiki 4 days stale, 373 raw captures unprocessed)

### Key Findings
- System extremely stable — 15+ days without new corrections
- Fourth learning graduated to `core` maturity (heartbeat, shared-public-state, cpmi-process-reward... + now bigmas)
- Near-graduation candidates: triattention (uses=6), rlm-principles (uses=6) — both validated, need ~4 more uses
- improvement-queue.md had persistent stale entries from unknown writer — root cause needs investigation

---

## Evolution Run — 2026-04-16 (#12)

### Signals
- 13 corrections (0 new since #11)
- 28 violations (unchanged — 23 stale file refs, 5 grep failures)
- 162 learnings scanned (+5 since #11)
- 2 graduation candidates: heartbeat (uses=12, core), shared-public-state (uses=13, core)
- 0 maturity upgrades (no draft with uses>=5)
- 0 decay/prune candidates (system 24 days old)
- 1 model_gate (sonnet-4.6, correctly scoped)
- 0 panic episodes, no replay queue, no skill-usage data
- Sessions: 100% healthy (5/5)
- Near-graduation: bigmas (uses=9, validated) — 1 use from threshold

### Proposals
- 4 proposed, 4 approved, 0 rejected

### Applied
- PROMOTE: heartbeat-mid-run-steering → critical-patterns #10 (uses=12, conf=1.0, core). Added graduated_to field. Critical-patterns now at 10/10 capacity.
- FIX_DATA: shared-public-state — removed stale `graduated_to: critical-patterns-10` (was never actually added as CP entry, heartbeat took the slot instead)
- DELEGATE: Spawned side-task to fix 23 stale file references across 12 skills (cleanup, not evolve scope)
- SKIP: autocompact verify_check — already fixed to "manual" in previous run

### Key Findings
- System stable — 18 days without new corrections
- First learning successfully graduated via full lifecycle: draft → validated → core → critical-patterns (#10)
- bigmas at uses=9 will auto-graduate when it hits 10 (auto-graduation pipeline active)
- 162 learnings — many low-use external_research (avg uses=1.4). Decay will handle over time.
- Stale file refs in skills are persistent tech debt — delegated as side-task

---

## Evolution Run — 2026-04-15 (#11)

### Signals
- 12 corrections (0 new since #10)
- 28 violations (0 new, same stale pool — field is `label:` not `rule:`, all known)
- 157 learnings scanned (+0 new since #10 yesterday)
- 0 graduation candidates (bigmas at uses=9, maturity=validated — 1 use from threshold)
- 0 maturity upgrades
- 1 decay warning: gap-cross-project-memory (conf=0.5, uses=0) → RESOLVED
- 0 prune candidates, 0 replay queue items
- 1 model_gate (sonnet-4.6, correctly scoped)
- Sessions: 100% healthy

### Proposals
- 3 proposed, 3 approved, 0 rejected

### Applied
- PRUNE: critical-patterns #7 (Tool Descriptions — Routing) — freed slot for bigmas graduation (uses=9→10 imminent); content preserved in rules/skill-files.md. Renumbered: #8→#7, #9→#8, #10→#9. Now 9/10 capacity.
- SUPERSEDE: gap-cross-project-memory.md — set valid_until: 2026-04-15, summary updated to RESOLVED. Gap addressed by auto-memory + /improve + behavioral-genome.md.
- UPDATE_CONFIRMED: All critical-patterns last_confirmed → 2026-04-15

### Infrastructure Changes (this session, pre-evolve)
- FIX: autodream.py — graduation check now skips maturity:core and graduated_to: learnings (prevented false re-flagging)
- CREATE: scripts/auto-graduation.py — auto-promotes eligible learnings to critical-patterns when capacity < 10
- UPDATE: autodream scheduled task — now runs auto-graduation.py after autodream.py
- UPDATE: weekly-evolve scheduled task — auto-applies objective graduation/maturity changes; judgment-required actions still go to user
- UPDATE: improvement-queue.md — 24 dedup pairs in 4 clusters logged for next /evolve

### Key Findings
- System stable — no new corrections or violations for 2+ weeks
