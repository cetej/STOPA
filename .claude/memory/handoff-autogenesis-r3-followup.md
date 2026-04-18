---
created: 2026-04-18
topic: Autogenesis R3 follow-up — graduation loop + uses counter
prerequisite_commit: 2097d35
status: ready-to-start
supersedes: handoff-autogenesis-r3.md
---

# Handoff: R3 follow-up — Graduation loop

## Context for the new session

Autogenesis protocol adoption is complete for R1-R4 (commits `1c7f31b`, `8e2b4d1`, `2097d35`):

- **R1 done**: per-resource version lineage + `scripts/resource-ledger.py` CLI
- **R2 done**: `.claude/rules/sepl-operators.md` formalizes ρσιεκ for iterative skills
- **R3 core done**: `/tool-synth` skill synthesizes drafts in `.claude/skills/_generated/<slug>/SKILL.md` with 13 invariants at synthesis time (commit `8e2b4d1`). Orchestrate Phase 3 step 3 has skill-miss hook invoking `/tool-synth`.
- **R3 lifecycle end done**: sweep Step 8 cleanup removes expired drafts (commit `2097d35`). Drive-by fixed sweep's own YAML frontmatter bug.
- **R4 done**: `commit-invariants.md` + self-evolve Critic gate.

**R3 lifecycle is half-done**: drafts are created (tool-synth) and destroyed-on-expiry (sweep Step 8). The **middle** — promotion from draft to top-level skill — has NO automation yet. This handoff specifies it.

Full paper context: `.claude/memory/learnings/2026-04-18-autogenesis-protocol.md`.

## Task: Close the generated-skill promotion loop

Two pieces, best done together because #2 is useless without #3:

### Piece #2: /evolve graduation step for sandbox drafts

Ref: [tool-synth/SKILL.md](.claude/skills/tool-synth/SKILL.md) "Promotion Path" section — the spec is already written there, just unimplemented in `/evolve`.

**Where:** Add new step in [.claude/skills/evolve/SKILL.md](.claude/skills/evolve/SKILL.md) — likely Step 3f or 3g depending on current numbering. Read evolve first; find existing graduation step for learnings (`validated → core`) and mirror its shape.

**Spec:**

1. Glob `.claude/skills/_generated/*/SKILL.md`.
2. For each draft, parse frontmatter and evaluate:
   - `uses >= 3` (from counter maintained by #3)
   - `valid_until > today` (not expired — expired ones die in /sweep Step 8)
   - No `harmful_uses` recorded (field optional; default 0)
   - Recent critic score is PASS — see "Critic score retrieval" below
3. For each promotable draft, present to user:
   ```
   Promotion candidate: /<slug>
     uses: N (threshold: 3)
     last critic: PASS on run <run-id> (<date>)
     created: <synthesized-at>, valid_until: <date>
     size: K lines
   Approve? [y/N]
   ```
4. On approval:
   - Move dir: `.claude/skills/_generated/<slug>/` → `.claude/skills/<slug>/`
   - Copy `SKILL.md` → `.claude/commands/<slug>.md` (sync invariant from core-invariants #2)
   - Edit frontmatter: `version: 0.x.y → 1.0.0`, `maturity: draft → validated`, remove `valid_until`, remove `synthesized-by`/`synthesized-at`/`synthesized-for-subtask`, set `user-invocable: true`, drop `generated` from `tags`
   - Append ledger entry: `trigger: "/evolve graduated <slug> from sandbox"`, `old_version: 0.x.y`, `new_version: 1.0.0`
   - Log to `decisions.md` via /scribe pattern
5. On rejection: no change; draft stays in `_generated/`, counter unchanged. User can retry later or let it expire.

**Critic score retrieval:** `/critic` currently writes results where? Grep evolve for "critic" to see how it reads prior critic outputs. Likely options: `.claude/memory/outcomes/*.md`, routing-traces JSONL, or critic report files. Use whatever shape /evolve already reads for learning graduation.

**Edge cases:**
- Draft with `uses >= 3` but never ran through critic (e.g., only used in light-tier where per-subtask critic skips): skip promotion, tell user "no critic signal available".
- Slug collision with existing top-level skill at promotion time: block, report which exists, don't overwrite.
- `harmful_uses >= 1`: skip, flag for pruning review instead.

### Piece #3: uses counter tracking

Generated skills have `uses: 0` implicit in frontmatter. Nothing increments it. Without this, #2 never triggers.

**Recommended: Option A — orchestrate Phase 4 increment** (simpler, sufficient because generated skills are `user-invocable: false` and only reachable via orchestrate's skill-miss hook).

**Where:** [.claude/skills/orchestrate/SKILL.md](.claude/skills/orchestrate/SKILL.md) Phase 4 "After each subtask" step list (currently goes 1-11). Add step 11a or 10b (pick whatever keeps numbering readable):

```
11a. If subtask's method was a generated skill (path matches `.claude/skills/_generated/`):
     - Read frontmatter of that SKILL.md
     - Parse current `uses:` integer (default 0 if missing)
     - Edit frontmatter: increment uses by 1
     - Also increment `successful_uses:` if subtask's critic score was PASS
     - Also increment `harmful_uses:` if critic FAIL
```

Rationale for Option A over PostToolUse hook:
- Generated skills are by design only invoked through orchestrate (frontmatter `user-invocable: false`)
- Reusing orchestrate's existing per-subtask edit cycle = zero new infrastructure
- No hook test harness complications

**Concurrency note:** orchestrate runs waves sequentially; within a wave, two agents won't use the same generated skill (Phase 3 step 3 hook synthesizes once and reuses for *one* subtask). No file contention in practice.

**If Option A proves insufficient** (manual invocations start happening later), upgrade to PostToolUse hook in a future session — but don't build that speculatively now.

## Integration order

1. **Do #3 first** (orchestrate edit) — even without #2, counter starts accumulating real data
2. **Then #2** (/evolve graduation) — can consume whatever counter data exists
3. **Smoke test both together** — need #3 output to trigger #2 meaningfully

## Required guardrails

- Promotion MUST require user approval (no --auto promotion)
- Slug collision check at promotion time (top-level AND sandbox) — same pattern as tool-synth Phase 4 invariants
- After promotion, `_generated/<slug>/` dir is fully removed (not left as stale copy)
- commit-invariants apply: promoted skill must pass I1-I4 before commit; any failure → rollback the move

## Verification checklist

- [ ] orchestrate Phase 4 edit is syncable (both `commands/orchestrate.md` and `skills/orchestrate/SKILL.md` identical)
- [ ] /evolve new step grafts into existing flow without breaking learning graduation (diff existing evolve, ensure no existing step broken)
- [ ] Smoke test #3: manually set `uses: 2` in extract-svg-to-sprite draft, run a dry orchestrate invocation that would hit it, verify `uses: 3` after
- [ ] Smoke test #2: with draft at uses=3 + fake critic PASS record, run /evolve, verify prompt appears, approve, verify:
  - File moved from `_generated/extract-svg-to-sprite/` to `.claude/skills/extract-svg-to-sprite/`
  - `.claude/commands/extract-svg-to-sprite.md` created and identical
  - Frontmatter: `version: 1.0.0`, `maturity: validated`, `valid_until` absent, `user-invocable: true`
  - Ledger entry with trigger `"/evolve graduated..."`
  - `_generated/extract-svg-to-sprite/` dir is gone
- [ ] Reject path test: decline promotion, verify counter stays, draft stays, no ledger entry

## Risk areas

- **Reading critic score from prior runs**: depends on how critic persists. Research this first — don't guess. `Grep` for "critic" in evolve's existing steps to find the pattern.
- **File move on Windows**: `shutil.move` handles it, but git doesn't see it as a rename if the file content changed (frontmatter edit). Either move-then-edit (clean rename in git) OR edit-then-move (git sees content change + move as one). Pick one; document in step for next person.
- **Empty `_generated/` after graduation**: fine to leave dir itself; gitignored.
- **successful_uses vs uses**: [core-invariants rules](.claude/rules/memory-files.md) distinguishes `uses` (retrieved) from `successful_uses` (retrieved and PASS). Generated skills should track both — mirror the learning counter semantics.

## What NOT to do

- Do not build PostToolUse hook for uses counting (speculative — Option A sufficient for now)
- Do not auto-promote without user approval (false positive promotions rot the skill catalog)
- Do not alter `tool-synth` skill — the spec it declares is what #2 must implement, not the other way around
- Do not add a new ledger schema for promotion — reuse existing log/history/rollback semantics
- Do not couple graduation to git commits — user may run /evolve with uncommitted state; promotion should work regardless

## Budget

Tier: **standard** (2-3 agents if needed). Estimate: 2-3h wall time. Two skill edits + two smoke tests.

## Concrete first steps for the new session

1. Read `.claude/skills/evolve/SKILL.md` fully — understand current graduation logic for learnings
2. Read `.claude/skills/orchestrate/SKILL.md` Phase 4 "After each subtask" list (approximately lines 880-970)
3. Grep for how critic scores are persisted: `Grep pattern="critic" path=".claude/skills/evolve" glob="*.md"` and `Grep pattern="routing-traces" path=".claude/skills" glob="*/SKILL.md"`
4. Decide move-then-edit vs edit-then-move based on what keeps git history cleanest
5. Implement #3 first (~30 min), then #2 (~60 min), then smoke tests (~30 min), then commit

Commit only if both smoke tests pass end-to-end (create → increment → graduate → verify top-level location).
