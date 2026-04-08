---
name: evolve
variant: compact
description: Condensed evolve for repeat invocations within session. Use full SKILL.md for first invocation.
---

# /evolve — Compact (Session Re-invocation)

Meta-engineer audit: load signals → analyze → propose changes → wait for approval → apply.

## Signal Sources

| File | Signal type |
|------|------------|
| `corrections.jsonl` | User corrections (most valuable, 2+ occurrences → PROMOTE) |
| `violations.jsonl` | Failed rule checks (3+ sessions same rule → ESCALATE_TO_CORE) |
| `sessions.jsonl` | Session scorecards (trend data) |
| `learnings/critical-patterns.md` | Current always-read patterns (max 10) |
| `learnings/` | All learning files (graduation/pruning candidates) |

## Analysis Passes

1. **Corrections** — group by semantic similarity → PROMOTE | CREATE | UPDATE | ALREADY_COVERED
2. **Violations** — group by rule source → ESCALATE_TO_CORE | ESCALATE_TO_HOOK | OK
3. **Confidence audit** — compute effective confidence for each learning:
   - Decay: `uses == 0` AND 60+ days old → -0.1 per 30 days (min 0.1)
   - Boost: `uses × 0.05` (max 1.0), minus `harmful_uses × 0.15`
   - Graduation: `uses >= 10` AND confidence >= 0.8 AND `harmful_uses < 2` → PROMOTE
   - Prune: effective confidence < 0.3 → PRUNE
4. **Model gate audit** — flag learnings with stale `model_gate:` for REVIEW
5. **Panic episodes** — if `panic-episodes.jsonl` exists, group recurring signals → ADD_TO_RUNBOOK
6. **Wiki freshness** — if wiki >7 days stale with new learnings → RECOMMEND /compile
7. **Session trends** — corrections/session trending up or down
8. **Skill usage audit** — stale skills (0 uses, 60+ days) → ARCHIVE candidate
9. **Critic alignment** — if `critic-accuracy.jsonl` < 80% aligned → PROPOSE_WEIGHT_CHANGE
10. **critical-patterns.md** — each entry: has verify: annotation? still accurate? redundant?

## Proposal Actions

| Action | Meaning |
|--------|---------|
| PROMOTE | Add to critical-patterns.md with verify: check |
| GRADUATE | Move critical-patterns.md → core-invariants.md |
| ADD_VERIFY | Add verify: annotation to pattern lacking one |
| PRUNE | Remove redundant/internalized pattern |
| UPDATE | Modify existing rule based on new evidence |
| CREATE | New learning file for uncaptured pattern |
| ESCALATE_TO_HOOK | Pattern violated so often it needs a hook |
| SYNTHESIZE_ARTIFACT | Convert pattern to executable artifact (max 5 per run) |

## Circuit Breakers (HARD STOPS)

- NEVER remove security rules (core-invariants items 4+)
- NEVER weaken the 3-Fix Escalation rule
- NEVER add rules contradicting CLAUDE.md or core-invariants.md
- NEVER re-propose a previously rejected change (check evolution-log.md)
- critical-patterns.md max 10 entries — must PRUNE before adding
- core-invariants.md max 7 entries — same

## Step 8: Approval Required

Present ALL proposals as numbered list → user approves/rejects/modifies → apply ONLY approved.
Append run summary to `.claude/memory/evolution-log.md` after applying.
