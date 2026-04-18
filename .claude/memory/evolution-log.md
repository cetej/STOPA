# Evolution Log

Record of /evolve audit proposals and outcomes.

---

## Evolution Run — 2026-04-18 (#15, 100-session audit, autonomous)

### Signals
- 14 corrections (mostly singletons — no new clusters, 4 real frustrations, 10 article-capture quotes)
- 200 violations / 26 unique runs (latest run 22:08, active violations already resolving)
- 100 sessions (all clean: 0 corrections/violations/frustrations today per counters)
- 20 panic episodes (all yellow, dominant `edit_velocity:3 + scope_creep:1`, 0 failures, task_style:unknown)
- 186 learning files scanned, 173 active
- 0 graduation-ready, 0 decay warnings, 0 maturity transitions ready
- 138/173 learnings missing maturity field (pre-field era legacy)
- 0/173 learnings with impact_score > 0 (impact tracking dormant)
- Replay queue empty, generated-skills sandbox empty
- skill-usage.jsonl not present (usage tracking not active)

### Proposals
- 6 proposed, 3 applied (autonomous), 2 flagged for follow-up, 1 recommended

### Applied
- **DEMOTE**: critical-patterns #7 (Sonnet 4.6 Thinking/Effort) — challenge condition triggered (current model Opus 4.7). Content preserved in standalone learning `2026-04-01-sonnet46-thinking-effort-breaking-change.md` (model_gate: sonnet-4.6). Critical-patterns renumbered: 10→9/10. #8→#7 (Anti-Hallucination), #9→#8 (Evolve/Maintenance), #10→#9 (Heartbeat).
- **UPDATE (no-op — already fixed)**: `2026-04-18-autogenesis-protocol.md` verify_check — file already contained `Glob('.claude/rules/sepl-operators.md')` from prior session. Old violations referred to stale Grep pattern.
- **BULK MATURITY TAG**: 131 legacy learnings missing `maturity` field → tagged as `draft`. New distribution: 164 draft, 4 validated, 3 core, 8 non-frontmatter. All graduation logic (draft → validated → core) now applicable to 80% larger pool.

### Flagged (spawned tasks / recommendations)
- **INVESTIGATE**: impact_score never populated (0/173 learnings). Helpfulness-driven retrieval boost defined in rules/memory-files.md has no data source. Check `.claude/hooks/outcome-credit.py` or equivalent.
- **INVESTIGATE**: panic-detector task_style detection. Recent episodes still log `task_style: unknown` despite commit 113993f adding task-style gating. 20 yellow false-positives in past 24h.
- **RECOMMEND**: `/compile` — 435 unprocessed raw captures (wiki synthesis stale).

### Rejected / Skipped
- **Hook import path**: violations log showed 9 broken paths, but verify regex `parent.parent / .scripts.` is overly greedy (matches correct `parent.parent.parent`). File's verify_check already `manual` with smoke-test note. Only remaining "broken" file is `archive/file-read-dedup.py` (unused, in archive/ dir).
- **BIGMAS + Toolgenesis verify violations**: verify_check strings updated in prior sessions between 22:08 and now. Current state passes (N-Plan Selection → 1 match, Schema-Utility Decoupling → 3 matches).

### Metrics change
- critical-patterns: 10/10 → 9/10 (1 free slot after DEMOTE)
- maturity coverage: 20% → 96% (138 untagged → tagged as draft)
- graduation pool eligible: unchanged (highest untagged uses = 4, still below ≥5 threshold)

---

## Evolution Run — 2026-04-18 (#14, deep signal-pipeline audit)

### Signals
- 12 corrections (0 new since #13 — but pipeline broken, see findings)
- 28 violations (unchanged from #13)
- 166 learnings scanned (+3 since #13)
- 3 graduation-ready: bigmas (uses=12), heartbeat (uses=13, already #10), shared-public-state (uses=14)
- 1 maturity draft→validated: msys-tmp-path-mismatch (uses=5)
- 0 prune candidates, 0 harmful_uses
- Sessions: 100% healthy (but signal stuck — see findings)
- Replay queue empty

### Critical Finding — Signal Pipeline Blockage (17 days)

User asked to investigate whether signals are blocked by broken loops. Investigation revealed:

**Commit `269ffdb` (2026-04-01) introduced `scripts/atomic_utils.py` and retrofitted 9 hooks to import it. Wrote WRONG sys.path (`.parent.parent` = `.claude/scripts/`) into 8 of them. Hooks died silently with `ModuleNotFoundError` for 17 days.**

Affected (all silent for 17 days):
- correction-tracker.py → corrections.jsonl frozen at 2026-04-01
- panic-detector.py → panic-state.json never created
- uses-tracker.py → uses counters frozen (explains 150+ learnings stuck at uses:0)
- auto-scribe.py → auto-learning broken
- verify-sweep.py → atomic_write path partial fail
- sidecar-queue.py → deferred suggestions broken
- auto-compound-agent.py → broken
- (correction-tracker.py duplicate of #1)

Plus separate bug:
- skill-usage-tracker.sh read only env var, not stdin → skill-usage.jsonl never created

### Proposals
- 5 proposed, 5 applied (autonomous — bug fixes, not behavior changes)

### Applied
- FIX_HOOKS: corrected sys.path in 7 hooks to `.parent.parent.parent / "scripts"`
- FIX_HOOK: skill-usage-tracker.sh — added stdin JSON fallback (matches skill-context-tracker.sh pattern)
- VERIFY: all 8 hooks now import cleanly + functional test passes
- UPGRADE_MATURITY: msys-tmp-path-mismatch.md draft → validated
- UPDATE_CONFIRMED: critical-patterns.md last_confirmed 2026-04-15 → 2026-04-18
- CREATE: 2026-04-18-hook-import-path-silent-blockage.md (meta-learning, severity=critical)

### Deferred
- DEFER_GRADUATION: bigmas + shared-public-state — utility ratio data may be unreliable until pipeline produces fresh signal. Re-evaluate at next /evolve when uses-tracker has been writing for 7+ days.

### Key Findings
- /evolve runs #5-#13 (9 runs) operated on frozen data, falsely reporting "system stable, 0 new corrections" while signal pipeline was completely broken.
- "Healthy" metrics from session-summary != actual signal flow. Trust file mtime + sample-payload tests over derived metrics.
- Path math is whitelist: `Path(__file__).resolve().parent` (file→dir) needs +1 parent vs. variable already holding dir.
- Need verify-sweep rule: each hook must be import-clean. Failed imports = critical violation.

---

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
- bigmas (uses=9) will graduate on next retrieval — slot now ready (9/10)
- Auto-graduation pipeline fully wired for future graduations without manual intervention

---

## Evolution Run — 2026-04-14 (#10)

### Signals
- 12 corrections (0 new since #9)
- 28 violations (unchanged, stale refs delegated to KODER in #9)
- 149 learnings scanned (+3 new token management learnings from vlog analysis)
- 2 graduation candidates: shared-public-state (12 uses), heartbeat (11 uses)
- 5 maturity upgrades pending (draft → validated/core)
- 0 prune candidates, 0 decay warnings
- 1 model_gate (sonnet-4.6, correctly scoped)
- 0 panic episodes, 0 replay queue items
- Sessions: 100% healthy (0 corrections, 0 frustrations)

### Proposals
- 6 proposed, 6 approved, 0 rejected

### Applied
- FIX: critical-patterns.md — removed 2 malformatted bullets (heartbeat, CORAL) that persisted from #9 (parallel session interference)
- MATURITY: shared-public-state → core (uses=12, conf=1.0)
- MATURITY: heartbeat → core (uses=11, conf=1.0)
- MATURITY: bigmas → validated (uses=8, conf=1.0)
- MATURITY: rlm-principles → validated (uses=5, conf=0.95)
- MATURITY: triattention → validated (uses=5, conf=0.95)

### Key Findings
- System stable — no new corrections for 2+ weeks
- First maturity tier updates applied (5 learnings promoted)
- critical-patterns at 10/10 capacity, no new promotions needed
- Token management learnings (compact 60%, cache TTL, MCP audit) compiled into wiki
- Next: monitor shared-public-state and heartbeat as first `core` maturity learnings

---

## Evolution Run — 2026-04-14 (#9)

### Signals
- 12 corrections (0 new since #8)
- 28 violations (deduplicated from 59 — repeated sweep runs on 2026-04-12)
- 154 learnings scanned, 0 new graduation candidates (2 already graduated in #8)
- 3 high-use approaching graduation: bigmas (8), triattention (5), rlm-principles (5)
- 0 prune candidates (no learnings below 0.3 confidence)
- 1 model_gate (sonnet-4.6) — correctly scoped with challenge condition
- 0 panic episodes, 0 replay queue items
- Sessions: 100% healthy (0 corrections, 0 frustrations)
- Skill usage: no data (skill-usage.jsonl doesn't exist)

### Proposals
- 5 proposed, 5 approved, 0 rejected

### Applied
- FIX: critical-patterns.md — removed 2 malformatted bullet items (heartbeat, CORAL) that overflowed from #8. These are already tracked in their graduated learning files.
- CLEAN: violations.jsonl deduplicated 59 → 28 entries (removed repeated sweep run duplicates)
- FIX_VERIFY: autoagent-overfitting-guard — verify_check path corrected from SKILL.md to references/
- DELEGATE: KODER task T-2026-04-14-002 — clean 29 stale file references across 12 skills
- UPDATE_CONFIRMED: All critical-patterns last_confirmed → 2026-04-14

### Key Findings
- System is stable — no new correction patterns, no new graduation candidates
- 154 learnings is still above 70 target but most are low-use external_research (decay will handle)
- Biggest actionable gap: 29 stale file refs in skills → delegated to KODER
- Next evolve: check bigmas/triattention/rlm-principles for graduation threshold

---

## Evolution Run — 2026-04-12 (#8)

### Signals
- 12 corrections (0 new since evolve #7)
- 60 violations (3 recurring + ~20 stale file refs in skills)
- 138 learnings scanned, 1 graduation ready (shared-public-state: uses=10, conf=1.0)
- 1 model_gate learning (sonnet-4.6, correctly scoped)
- Wiki EXISTS (INDEX.md + 100+ files) — previous evolve runs incorrectly reported missing (stale read bug)
- Sessions: 100% healthy (0 corrections, 0 frustrations)

### Proposals
- 5 proposed, 4 approved, 1 dropped (compile recommendation — wiki already existed)

### Applied
- PROMOTE: shared-public-state → critical-patterns #10 (proper entry, removed malformed bullet from #9)
- FIX_DATA: shared-public-state learning — removed duplicate confidence field, added graduated_to
- FIX_VERIFY: autocompact-threshold — verify_check changed to manual (was grepping wrong path)
- CREATE: `2026-04-12-evolve-must-verify-current-state.md` — evolve MUST Glob/Read before RECOMMEND
- CREATE: critical-patterns #10 — "Verify Current State, Don't Trust Own Log"
- UPDATE_CONFIRMED: All critical-patterns last_confirmed → 2026-04-12

### Dropped
- RECOMMEND /compile — wiki already exists (100+ files). This was the 7th false recommendation caused by stale read bug.

### Key Finding
User identified systemic issue: parallel sessions (manual + scheduled) modify state independently, causing stale reads. Evolve was reading its own log instead of checking filesystem state. Fixed by adding critical-pattern #10 + learning.

---

## Evolution Run — 2026-04-12 (#7)

### Signals
- 12 corrections (0 new since evolve #6)
- 2 violations (0 new since 2026-03-29)
- 113 learnings scanned, 0 graduation-ready (closest: shared-public-state 9 uses, heartbeat 8 uses)
- 0 model_gate learnings with mismatch
- Wiki still not built (INDEX.md missing)
- Sessions: 100/100 healthy (0 corrections, 0 frustrations in last 20)

### Proposals
- 6 proposed, 6 approved, 0 rejected

### Applied
- CREATE: evolution-log.md entry (this)
- UPDATE: stopa-worker.md — added analysis-paralysis guard (rule #6, fixes violations.jsonl verify)
- UPDATE: shared-public-state-agent-coordination.md — confidence: 0.75 (9 uses, near graduation)
- UPDATE: heartbeat-mid-run-steering.md — confidence: 0.75 (8 uses, near graduation)
- RECOMMEND: Run /compile --full (wiki not built, 113 learnings available)
- KEEP: 7 index-*.md files — legacy but still useful as browsable summaries

### Rejected
- (none)

### Notes
- System very healthy — 7th evolve run with 0 new corrections since March
- Graduation threshold not yet reached by any learning (closest: 9/10 uses)
- Previous DEFER decision on heartbeat/shared-public-state utility ratio still applies (evolve #5/#6)

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
