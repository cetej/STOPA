---
created: 2026-04-18
topic: Autogenesis protocol adoption — Phase 2 (R3 tool-synth spike)
prerequisite_commit: 1c7f31b
status: ready-to-start
---

# Handoff: Autogenesis Protocol — Phase 2

## Context for the new session

In previous session (commit `1c7f31b`, 2026-04-18) STOPA adopted three of four recommendations from Autogenesis paper (arXiv:2604.15034):

- **R1 done**: Per-resource version lineage via `version:` field + `.claude/memory/resource-ledger.jsonl` + `scripts/resource-ledger.py` CLI. Self-evolve bootstrapped at v1.1.0.
- **R2 done**: `.claude/rules/sepl-operators.md` formalizes ρ/σ/ι/ε/κ for iterative skills.
- **R4 done**: `.claude/rules/commit-invariants.md` + Step 4b in self-evolve enforces 6 safety invariants with rollback precedence.
- **R3 PENDING** — this session.

Full paper summary: `.claude/memory/learnings/2026-04-18-autogenesis-protocol.md`
Full paper text (gitignored): `.claude/memory/intermediate/autogenesis-paper.txt`

## Task: R3 — Tool Generator (dynamic skill synthesis)

### Motivation

Autogenesis GAIA experiments showed **Level 3 +33.3 pp absolute** when the agent dynamically synthesizes tools on subtask miss. STOPA currently has 60+ static skills; novel subtasks fall between their descriptions. Dynamic skill synthesis closes this long-tail gap.

### Spec

New skill: `/tool-synth` (Tier 2, phase: build). When `/orchestrate` encounters a subtask where all existing skills score < threshold:

1. Semantic search over `.claude/skills/` (reuse existing `/triage` logic or `memory-search.py`)
2. If top match score < 0.4 → invoke `/tool-synth` with subtask description
3. Generate a skill in sandbox `.claude/skills/_generated/<slug>/SKILL.md`:
   - `maturity: draft`
   - `valid_until: <today+7>`
   - `version: "0.1.0"`
   - `tags: [generated]` (for filtering)
   - Log creation to `resource-ledger.jsonl` with `trigger: "tool-synth created"`
4. Register via resource-ledger; orchestrate uses it for the current subtask
5. Promotion path: if the generated skill is retrieved and used successfully 3+ times (track via `uses:` counter), `/evolve` proposes graduation to top-level `.claude/skills/<name>/`

### Required guardrails (lessons from Phase 1)

- **Invariants apply**: Generated skill MUST pass all `commit-invariants.md` checks before registration. Enforce at synthesis time, not after.
- **Sandbox isolation**: `_generated/` directory — gitignore by default; only graduated skills enter tracked state.
- **Expiration**: Auto-cleanup of expired drafts in `/sweep`.
- **Description rule**: Generated skills MUST have `Use when...` descriptions. Add generation-time validation.
- **No recursion**: `/tool-synth` itself cannot call `/tool-synth` (core-invariants #8, max-depth: 1).

### Risk areas

- **Slop risk**: Auto-generated skills may be low quality. Mitigation: Critic agent reviews before registration (reuse /critic pattern).
- **Skill explosion**: Could generate N duplicates of similar skills. Mitigation: pre-synthesis semantic search with high threshold; reject if similar generated skill exists.
- **Trigger conflicts**: New generated skill's `description:` might overlap with existing skill. Mitigation: /triage-style dry-run to check for ambiguity.

## Concrete next steps for this session

1. Read: `.claude/memory/learnings/2026-04-18-autogenesis-protocol.md` (gap analysis table at end)
2. Read: `.claude/skills/skill-generator/SKILL.md` (existing skill creation logic — reuse where possible)
3. Read: `.claude/skills/orchestrate/SKILL.md` (integration point — where to add the `/tool-synth` invocation)
4. Read: `.claude/skills/triage/SKILL.md` (semantic search pattern)
5. Check if `.claude/skills/_generated/` should go to gitignore
6. Design: write `/tool-synth` skill (keep under 300 lines — this is a spike)
7. Integration: add invocation hook in `/orchestrate` Phase 1 (scout/triage step)
8. Test: construct a fake novel subtask, run orchestrate with `--dry-run`, inspect generated skill
9. Commit only if tests pass

## Verification checklist

- [ ] `/tool-synth` skill exists in both `.claude/skills/tool-synth/SKILL.md` and `.claude/commands/tool-synth.md`
- [ ] Frontmatter has `Use when...` description (per core-invariants #3)
- [ ] SEPL operators labeled in workflow (per sepl-operators.md rule)
- [ ] Invariants enforced at synthesis (per commit-invariants.md)
- [ ] `_generated/` path is handled (gitignore or sandbox rule)
- [ ] Smoke test: generate a dummy skill, verify it passes invariants, verify ledger entry
- [ ] Diff check: `diff .claude/commands/tool-synth.md .claude/skills/tool-synth/SKILL.md` shows identical

## Budget

Tier: **standard** (2-4 agents if needed). Max 4 iterations of skill + 1 smoke test. Estimate: 1-2h wall time, 5-8 USD.

## What NOT to do

- Do not implement RSPL 5-type unification (rejected in Phase 1 analysis — massive refactor, low value)
- Do not implement Agent Bus (R5, rejected — wrong fit for CLI context)
- Do not rewrite existing skills to fit new pattern — only new skills get `version:` initially
- Do not modify `scripts/resource-ledger.py` without a failing case — the API is deliberately minimal
