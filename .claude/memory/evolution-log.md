# Evolution Log

- bigmas graduated to `core` maturity (uses=15, now core+); no further action needed
- Auto-graduation pipeline fully wired for future graduations without manual intervention

---

## Evolution Run — 2026-04-24 (#11)

### Signals
- 38 corrections (5 new since #10: daily-rebalancer whitelist 4×, evolve-skills describe-only 2× + 5 frustrations)
- 200 violations (4 clusters — 3 resolved post-hoc, annotations.jsonl stale ref 30+ still firing)
- 195 learnings scanned (+46 since #10)
- 0 prune candidates, 0 decay warnings (system very healthy)
- 5 draft→validated candidates, 0 val→core
- 2 model_gate (sonnet-4.6 stale, opus-4-7 current)
- 26 panic episodes (all yellow, bulk-edit noise, no action needed)
- 0 replay queue items, 0 generated skills
- Sessions: 100/100 healthy scorecards
- Skill usage: no data (tracking not active)

### Proposals
- 6 proposed, 5 approved (2+3 consolidated into single learning), 0 rejected

### Applied
- CREATE: `.claude/memory/annotations.jsonl` (empty placeholder) — resolves 30+ active violations
- CREATE: `2026-04-24-scheduled-task-discipline.md` — consolidates daily-rebalancer whitelist + evolve-skills describe-only patterns (draft, skill_scope: scheduled-tasks)
- MATURITY: 5 draft→validated (ecosystem-scan, agent-deception, living-memory, experience-replay, worldmonitor)
- MODIFY: sonnet46-thinking-effort — added `valid_until: 2026-10-31` (auto-expires, model_gate=sonnet-4.6 stale for opus-4-7)
- UPDATE_CONFIRMED: all 9 critical-patterns last_confirmed → 2026-04-24

### Key Findings
- Root cross-project issue: scheduled agents operating in autonomous mode violate both whitelist discipline AND execution mandate. Fix must land at scheduled-task SKILL source, not STOPA rules — captured as cross-project learning.
- System stable: 0 prune/decay across 195 learnings, healthy scorecards, corrections localized to scheduled-task-context only.
- Critical-patterns at 9/10 — slot #10 remains free; no universally-applicable candidate compelling enough.

### Follow-up — Source Fix + Regression Guard (2026-04-24)

Applied same day, post-commit:

- **Direct edit** `~/.claude/scheduled-tasks/daily-rebalancer/SKILL.md` — strengthened Phase 2.5 whitelist with explicit FORBIDDEN anti-examples (node_modules, __pycache__, .env, IDE dirs) + SILENT SKIP rule ("If it looks like local state but isn't one of the three → skip silently, don't propose")
- **Direct edit** `~/.claude/scheduled-tasks/auto-evolve-skills/SKILL.md` — replaced "Do NOT apply candidates automatically — only generate them for human review" with SAFE/RISKY classification: apply description/frontmatter/verify_check tweaks immediately via Edit, log workflow restructures to `evolve-candidates.md` for review
- **Regression guard** `.claude/hooks/verify-sweep.py` §5c — new check scans `~/.claude/scheduled-tasks/*/SKILL.md` for describe-only imperative regex. Tested: catches original bad text, zero false positives on 38 current SKILLs.

Note: `~/.claude/` is not under git — SKILL edits are local-only. Validator will flag regression if any future scheduled-task SKILL re-introduces describe-only imperatives.

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

---

## Evolution Run — 2026-04-26

First run since 2026-04-08 (#4) — 18 days of accumulated signals.

### Signals
- 43 corrections (33 new since #4) — clusters A (skill-evolution agent describe-only ×4) + B (daily-rebalancer whitelist ×2) both ALREADY_COVERED by 2026-04-24-scheduled-task-discipline.md
- 200 violations across 4 patterns — ALL stale (fixes e745ebc + 0e7692c deployed 2026-04-26 17:00, latest violation 16:50 = pre-fix)
- 100 sessions, last 10 healthy (corrections=0, errors=0, frustrations=0)
- 197 learnings scanned: 0 new graduation candidates (3 high-use already at maturity=core), 0 prune candidates (none < 0.3 confidence), 0 draft→validated upgrades
- 26 panic episodes (single-day burst 2026-04-18, all yellow, dominant `edit_velocity:3 + scope_creep:1`) — covered by calm-steering protocol
- replay-queue empty, annotations.jsonl empty, skill-usage.jsonl still missing (deferred again)
- critical-patterns.md healthy at 9/10, all last_confirmed 2026-04-24

### Proposals
- 3 proposed, 2 approved + applied, 1 self-rejected

### Applied
- ARCHIVE_LOG: Rotated violations.jsonl (200 stale entries) → violations-archive.jsonl, fresh empty log started
- ADD_AUTONOMY_MARKER: Added `<!-- AUTONOMOUS-EXECUTION v1 -->` block to ~/.claude/scheduled-tasks/tool-radar-scan/SKILL.md (38th task — was the only one missing the marker; cross-project edit, not in STOPA repo)

### Self-Rejected (post-approval, pre-application)
- BUMP_USES_COUNTER on 2026-04-24-scheduled-task-discipline.md (4→6): proposal was based on counting source-signal corrections (2026-04-19 to 2026-04-21) that PRE-DATED the learning's creation (2026-04-24). Source signals don't count as post-creation retrievals. Current `uses: 4` already correctly reflects actual applications.

### Deferred (again)
- Skill-usage tracking hook — sessions.jsonl shows skills=0 across all 100 sessions. Either tracking still inactive or the autonomous-mode work bypasses skill invocations. Revisit when skills appear in session scorecards.
