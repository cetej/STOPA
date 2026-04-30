---
name: dreams
description: "Use when running offline memory consolidation — cross-linking learnings, backward-updating contexts, surfacing cross-session patterns. Trigger on 'dreams', 'consolidate memory', 'dream cycle'. Do NOT use for numerical maintenance (that's autodream.py) or manual learning capture (/scribe)."
user-invocable: true
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash", "Agent", "TodoWrite"]
permission-tier: workspace-write
phase: meta
tags: [memory, session]
requires: []
max-depth: 1
effort: auto
discovery-keywords: [consolidate, integrate, reflect, cross-link, pattern detection, memory health, offline processing, sleep]
input-contract: "scheduled-task or user → no input required → reads memory state autonomously"
output-contract: "dream log → markdown → .claude/memory/dreams/YYYY-MM-DD.md"
preconditions: [".claude/memory/learnings/ directory exists"]
effects: ["related: fields updated in learnings", "dream log written", "concept-graph.json updated if new connections found", "merged learnings created from merge-candidates stubs (originals soft-sunset)", "7-day raw session window scanned for cross-session patterns (OpenClaw batch model)"]
---

# Dreams — Offline Memory Consolidation

You are the Dream Consolidator. While the user is away, you review recent memory activity, find hidden connections, and strengthen the knowledge base.

## Philosophy

Research validates this approach:
- Reflexion (91% vs 80% HumanEval) proves reflection is load-bearing
- Generative Agents degenerate in 48h without reflection
- A-MEM's backward-updating makes old memories evolve with new context
- MemMachine shows retrieval quality >> storage sophistication
- OpenClaw's dream cycle: collect → consolidate → evaluate with Smart Skip
- OpenClaw batch model (7-day window): immediate per-session summarization loses cross-session patterns; 7d batch with Smart Skip saves ~90% tokens on idle days while surfacing recurrence signals invisible to single-session reflection

## Process

### Phase 0: Smart Skip Check (OpenClaw 7-day batch model)

Before doing anything expensive, count signal across four sources:

1. **Last dream**: Read most recent `.claude/memory/dreams/YYYY-MM-DD*.md` — extract `date:` and `consolidated_through:` (if present) from frontmatter
2. **Autodream report**: Read `.claude/memory/intermediate/autodream-report.json` — last maintenance report
3. **New learnings**: `Glob("2026-*.md", path=".claude/memory/learnings/")` — count files mtime ≥ last dream date
4. **New outcomes**: `Glob("2026-*.md", path=".claude/memory/outcomes/")` — count files mtime ≥ last dream date
5. **Unconsolidated raw (7d window)**: `Glob("2026-*.md", path=".claude/memory/raw/")` (NOT `raw/processed/`) — count files dated within last 7 days. This is the OpenClaw signal — raw session captures that no dream has yet folded into pattern detection.
6. **Replay queue ready items**: Read `.claude/memory/replay-queue.md` — count rows with `Status: ready` (file may not exist; treat as 0)

Decision matrix (`L` = new learnings, `O` = new outcomes, `R` = unconsolidated raw in 7d, `Q` = replay-ready):

| L | O | R | Q | Action | Token target |
|---|---|---|---|--------|--------------|
| 0 | 0 | 0 | 0 | **Full skip** — write 1-line `YYYY-MM-DD-skip.md` and exit | ~2K |
| 0 | 0 | 1-2 | 0 | **Skip with raw note** — 1-line skip log mentioning raw count, exit | ~3K |
| 0 | 0 | ≥3 | 0 | **Raw-only abbreviated cycle** — Phase 1 (raw window only) → Phase 2c (cross-session patterns) → Phase 3 (minimal log) | ~10K |
| 1-2 | * | * | 0 | **Abbreviated cycle** — Phase 1 + 2a + 2b + 2e + 3 (skip 2c, 2d) | ~25K |
| ≥3 | * | * | * | **Full cycle** — all phases | ~50–150K |
| * | * | * | ≥1 | **Force full cycle** — replay-ready items override skip | ~50–150K |

If skipping, write a 1-line log: `.claude/memory/dreams/YYYY-MM-DD-skip.md` with the reason and the (L, O, R, Q) tuple.

**Why 7-day window**: OpenClaw's batch model retains raw traces for 7 days then consolidates. Immediate per-session summarization loses cross-session recurrence — a failure that appears once is noise, the same failure four times in a week is signal. 7d is the minimum window where pattern recurrence becomes statistically meaningful for typical agent workloads, while still being short enough that boost confidence reflects current behavior.

### Phase 1: Collect (read-only scan)

Gather raw material for consolidation. The 7-day raw window is the OpenClaw addition — distilled artefacts (learnings, outcomes) keep their existing 14-day window.

1. **Recent learnings** (last 14 days): Read all `.claude/memory/learnings/2026-*.md` files from the last 14 days
2. **Recent outcomes** (last 14 days): Read `.claude/memory/outcomes/2026-*.md` if directory exists
3. **Current checkpoint**: Read `.claude/memory/checkpoint.md` — what was the user working on?
4. **Autodream report**: Read `.claude/memory/intermediate/autodream-report.json` — what's stale, what's graduating?
5. **Concept graph**: Read `.claude/memory/concept-graph.json` — existing knowledge connections
6. **Raw 7-day session window** (OpenClaw batch): `Glob("2026-*.md", path=".claude/memory/raw/")` (NOT `raw/processed/` — those are already consolidated). Filter to files dated within last 7 days. Read frontmatter only (date, timestamp, type, writes, agents, skills_count) plus the `## Files Touched`, `## Agent Activity`, and `## Key Decisions & Outputs` sections — skip body if size > 5 KB. **Cap**: at most 50 raw files per cycle, most-recent-first. Record actual count read in `raw_traces_scanned` and total in `raw_traces_in_window` for the dream log.
7. **Farm ledgers** (optional): `Glob("farm-ledger-*.md", path=".claude/memory/intermediate/")` — read any archived farm ledger frontmatter from the 7-day window. Skip the live `farm-ledger.md` if it is still at sweep 0 (template). Each archived ledger contributes a `## Discovered Patterns` section worth scanning for cross-cutting techniques.

Build a mental model: What themes keep appearing? What's connected but not linked? Which raw sessions touched the same files / spawned the same agents / hit the same errors? Distilled learnings tell you the conclusions; raw traces show recurrence.

### Phase 2: Consolidate (the actual dreaming)

#### 2a: Cross-link Discovery

For each recent learning, check:
- Does it share themes/component with other learnings that don't have `related:` connections?
- Would adding `related:` links improve retrieval for common queries?

**Rules:**
- Max 3 `related:` entries per learning (already in memory-files.md rules)
- Only link genuinely related learnings, not just same-component
- Prefer linking across components (cross-cutting insights are most valuable)

#### 2a1: Merge Synthesis (Hippo-inspired)

Read merge candidate stubs from `.claude/memory/intermediate/merge-candidates/*.json`. Each stub was written by `autodream.py` for a pair with `summary_jaccard >= 0.5` AND both confidence > 0.5 AND 3+ shared tags. The stub contains both summaries, counters, and shared tags.

For EACH stub:

1. Read both source learning files in full (frontmatter + body)
2. Synthesize a unified merged learning:
   - **Filename**: `merged-YYYY-MM-DD-<short-topic>.md`
   - **Summary**: 1-2 sentences capturing the union of both insights — NOT concatenation
   - **Tags**: union of both tag sets
   - **Confidence**: max(a.confidence, b.confidence)
   - **uses, successful_uses, harmful_uses**: sum of both (preserves earned credit)
   - **source**: keep the more authoritative one (`user_correction` > `critic_finding` > `auto_pattern` > `external_research` > `agent_generated`)
   - **maturity**: max(a.maturity, b.maturity) using ordering draft < validated < core
   - **supersedes**: filename of the OLDER source (max 1 entry; if both, use most-recent date)
   - **related**: union of both `related:` minus the two filenames being merged
   - **body**: blend the two bodies — preserve any post-mortem / Reflexion notes verbatim, dedupe identical lines, keep most concrete examples
3. Write the merged learning via Edit/Write
4. Soft-sunset both originals: set `valid_until: <today>` on both source files (skip retrieval, keep audit trail; do NOT delete files)
5. Move the consumed stub to `.claude/memory/intermediate/merge-candidates/processed/<stub>.json`

**Per-cycle limits:**
- Max 3 merges per dream cycle (avoid mass restructuring)
- If stub count > 3: process top 3 by `summary_jaccard` desc, leave rest for next cycle
- If a stub references a missing source file (already archived/deleted): move stub to `processed/` with a `skipped: source_missing` note

**Refuse to merge** if either source has:
- `maturity: core` AND `harmful_uses == 0` (battle-tested rules don't get restructured silently)
- `model_gate:` field set (model-specific learnings stay separate)
- `valid_until:` already in the past (already invalidated; let normal lifecycle handle)

#### 2b: Backward-Update (A-MEM inspired)

When a new learning changes context for an older one:
- Update the older learning's body text with a brief note: `> Updated YYYY-MM-DD: <context from new learning>`
- Don't change the original content — append context
- Max 1 backward-update per old learning per dream cycle

#### 2c: Pattern Detection (raw + distilled)

Look for recurring patterns across learnings, outcomes, AND raw 7-day session window:
- Same `failure_class` appearing 3+ times → candidate for critical-patterns.md
- Same component failing repeatedly → systemic issue
- Techniques that work across different contexts → candidate for generalization
- Same file path appearing in `## Files Touched` of 4+ raw sessions → systemic hotspot (recommend in dream log)
- Same agent name appearing in `## Agent Activity` of 3+ raw sessions with no corresponding learning → silent overuse, flag for /discover

**Maturity-Aware Generalization:**
- When a pattern appears 3+ times across sessions (different dates in learnings): recommend `maturity: validated` upgrade
- Cross-session patterns carry stronger signal than single-session observations
- Check: grep same `failure_class` or `component` across learnings → count unique dates

**Cross-Session Confidence Boost (OpenClaw batch produce):**
- For each `maturity: draft` learning examined in this cycle: count distinct raw session dates within the 7-day window where the learning's `tags:` overlap with raw session metadata (skills_count list, files touched extensions, agent names).
- Threshold: overlap on ≥3 distinct session dates = "cross-session validated" candidate.
- Action: list these in dream log under `## Cross-Session Patterns` with format `<learning-file> | <N sessions> | <overlap evidence>`. Do NOT mutate the learning's confidence here — this is a recommendation surfaced for `/evolve` to apply on next maintenance pass (separation of concerns: dream surfaces, evolve mutates).
- Why: a draft learning that recurs across multiple independent sessions in a week carries stronger generalization signal than the single capture event that produced it. Cross-session corroboration is the OpenClaw "batch validated" signal.

#### Phase 2e: Replay Queue Check

Read `.claude/memory/replay-queue.md`:
- Items with status `pending` older than 14 days without matching second failure → flag in dream log as "stale draft — consider manual review or archival"
- Items with status `ready` → note in dream log: "N items ready for replay validation — trigger /evolve or /learn-from-failure"
- Update Smart Skip: if replay queue has `ready` items → do NOT skip dream cycle (consolidation needed)

If file doesn't exist, skip this step silently.

#### 2d: Concept Graph Update

If new connections were found in 2a-2c:
- Read current `concept-graph.json`
- Add new edges for discovered relationships
- Keep graph manageable: max 200 nodes, prune lowest-weight edges if needed

### Phase 3: Evaluate & Report

Write dream log to `.claude/memory/dreams/YYYY-MM-DD.md`:

```markdown
---
date: YYYY-MM-DD
cycle_type: full | abbreviated | raw-only-abbreviated
cycle_window_days: 7
learnings_scanned: N
outcomes_scanned: N
raw_traces_scanned: N
raw_traces_in_window: N
connections_found: N
backward_updates: N
patterns_detected: N
cross_session_patterns: N
consolidated_through: <ISO timestamp of newest raw file scanned>
duration_estimate: Nmin
---

# Dream Log — YYYY-MM-DD

## New Connections
- learning-A.md ↔ learning-B.md: <why they're related>
- ...

## Backward Updates
- Updated learning-X.md with context from learning-Y.md: <what changed>
- ...

## Emerging Patterns
- <pattern description>: seen in [learning-1, learning-2, learning-3]
- ...

## Cross-Session Patterns
<!-- New section. List draft learnings whose tags overlap with raw session metadata across ≥3 distinct dates in the 7-day window. Recommendation only — /evolve applies confidence boost. -->
- learning-X.md | 4 sessions (2026-04-25, 04-26, 04-28, 04-30) | overlap: shared tag `pipeline`, files touched include `phase16_glossary.py`
- ...

## Consolidation Health
- Total learnings: N
- Average confidence: N.NN
- Learnings with 0 uses (30+ days old): N
- Graduation candidates: N
- Suggested actions: ...
```

For abbreviated and raw-only-abbreviated cycles, omit sections that weren't run (e.g. raw-only-abbreviated has no `## New Connections` or `## Backward Updates`).

### Phase 4: Smart Skip Optimization

Track token usage and cycle type (set in Phase 0):
- **Full skip** (~2K tokens): 1-line log, exit immediately
- **Skip with raw note** (~3K tokens): 1-line log noting unconsolidated raw count
- **Raw-only abbreviated** (~10K tokens): Phase 1 (raw + checkpoint only) + Phase 2c (cross-session patterns) + Phase 3 (minimal log with `## Cross-Session Patterns` section)
- **Abbreviated** (~25K tokens): Phase 1 + 2a + 2b + 2e + 3 (skip 2c, 2d)
- **Full** (~50–150K tokens): all phases

If cycle finds nothing actionable, log "clean dream" and exit. Always set `cycle_type:` in dream log frontmatter so trace analysis can distinguish modes. Always record `consolidated_through:` as the timestamp of the newest raw file scanned — next dream can use it to compute the unconsolidated window without rescanning everything.

## Anti-Rationalization Defense

| Rationalization | Why Wrong | Do Instead |
|---|---|---|
| "I'll link everything to everything" | Over-linking dilutes retrieval signal | Max 3 related per learning, cross-component preferred |
| "This pattern is obvious, no need to log" | Obvious patterns still need measurement | Log it — if it's real, uses counter will validate |
| "I'll backward-update extensively" | Heavy updates change meaning of old learnings | Append-only context notes, max 1 per learning per cycle |
| "No new learnings, nothing to do" | Cross-linking existing learnings is always valuable | Check existing learnings for missing connections |
| "I'll merge anything similar — autodream flagged it" | autodream.py only detects shape, not whether merge is correct | Read both source files in full; refuse merge if either is `maturity: core` and harmless |
| "I'll merge by concatenating both bodies" | Concatenation duplicates content and loses synthesis value | Synthesize unified summary; preserve verbatim post-mortem/Reflexion notes; dedupe identical lines |
| "I'll delete the originals after merge" | Audit trail required — past confidence/uses earned matter | Set `valid_until: today` on originals (skip retrieval, keep on disk) |
| "Cross-session match — I'll bump confidence right here" | Dream surfaces, /evolve mutates. Bumping in dream collapses the audit trail and overrides the maturity ladder | List the candidate under `## Cross-Session Patterns`; let `/evolve` apply the boost on its next maintenance pass |
| "I'll read all 200+ raw files for completeness" | Most-recent-first cap of 50 keeps cycles bounded; cross-session signal is statistical, not exhaustive | Read at most 50 raw files in the 7-day window; record `raw_traces_scanned` vs `raw_traces_in_window` so the gap is auditable |

## Red Flags

STOP and re-evaluate if any of these occur:
- Linking more than 5 learnings in one cycle (probably over-connecting)
- Backward-updating more than 3 learnings in one cycle (too aggressive)
- Dream log exceeds 100 lines (too verbose, consolidate)
- Spending > 10 minutes on Phase 1 scan (too many files, narrow scope)
- Merging >3 learnings in one cycle (mass restructuring — let pile up for next cycle instead)
- Merge candidate stub references a `core` learning (refuse, stub should not have been written)
- Reading more than 50 raw session files in one cycle (cap exceeded — hit the most-recent-first limit)
- Cross-Session Patterns section lists more than 8 candidates (signal threshold too loose, raise threshold or split cycle)

## Verification Checklist

- [ ] Smart Skip correctly evaluated using (L, O, R, Q) tuple from Phase 0
- [ ] `cycle_type:` field set in dream log frontmatter (full | abbreviated | raw-only-abbreviated | skip)
- [ ] All new `related:` links are bidirectional (A→B and B→A)
- [ ] Backward updates are append-only (original content unchanged)
- [ ] Dream log written with accurate counts including `raw_traces_scanned` and `raw_traces_in_window`
- [ ] No fabricated connections (every link has stated reason)
- [ ] Each merged learning has `supersedes:` pointing at the older source
- [ ] Both originals soft-sunset (`valid_until: <today>`) — not deleted
- [ ] Consumed merge stubs moved to `intermediate/merge-candidates/processed/`
- [ ] `## Cross-Session Patterns` is recommendation-only (no learning confidence mutated by this dream)
- [ ] `consolidated_through:` set to newest raw file timestamp scanned (or omitted if no raw files read)

## Rules

- NEVER delete or modify the core content of existing learnings — only add `related:` fields and append context notes
- NEVER create new learnings — that's /scribe's job. Dreams consolidate, not create.
- NEVER skip Smart Skip check — it saves 90% of token budget on idle days
- Dream logs accumulate in `.claude/memory/dreams/` — archive after 30 days
- If concept-graph.json doesn't exist, skip Phase 2d (don't create from scratch here)
- Keep dream logs factual and brief — no speculation about "what the user might want"
