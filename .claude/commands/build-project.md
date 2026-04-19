---
name: build-project
description: "Use when building a new project from requirements end-to-end with multi-session harness. Trigger on 'build project', 'create project', 'postav projekt'. Do NOT use for single features or existing project modifications. Orchestrates the full pipeline: requirements -> scaffold (with feature-list.json ground truth) -> per-feature implementation -> end-to-end verification per feature."
curriculum-hints:
  - "Analyze requirements and produce a feature list with end-to-end test steps before writing any code"
  - "Scaffold project with /project-init --harness (creates feature-list.json ground truth)"
  - "Implement ONE feature at a time; mark passes:true only after end-to-end verification"
  - "End every session with progress.md update and git commit"
  - "Wire up integration, run full smoke test, then declare project-level completion"
tags: [planning, orchestration]
phase: plan
user-invocable: true
model: opus
max-depth: 2
maxTurns: 60
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - Agent
  - Skill
  - TodoWrite
  - AskUserQuestion
  - WebSearch
  - WebFetch
output-contract: "built project → registered in projects.json, feature-list.json with all passes:true, README.md → target project root"
preconditions:
  - "user-provided requirements (natural language)"
  - "target directory writable or not yet existing"
effects:
  - "project scaffold created via /project-init --harness"
  - "feature-list.json populated from requirements"
  - "all features implemented with passes:true verified end-to-end"
  - "docs/progress.md has session log entries"
  - "project registered in ~/.claude/memory/projects.json"
---

# Build Project — Autonomous Project Builder with Harness

You build complete projects from natural language requirements, using the harness pattern: feature-list.json as ground truth, per-feature end-to-end verification, progress.md for multi-session continuity. You chain multiple skills autonomously, with human gates only at critical decision points.

## The Harness Discipline

Every project this skill builds MUST satisfy these invariants at completion:
1. `docs/feature-list.json` exists and every feature has `passes: true`
2. Every `passes: true` was set only AFTER end-to-end verification (not unit tests alone)
3. `docs/progress.md` contains a session log entry for every build session
4. Git history shows one commit per feature (or per coherent feature batch)
5. `./init.sh` runs cleanly from a fresh checkout and passes its smoke test

If any invariant fails, the project is NOT built — it is partially built.

## Pipeline

### Phase 1: Requirements Analysis -> Feature List Draft

1. Parse user requirements — what problem does this solve? Who is the user? What are the constraints?
2. If requirements are vague (< 3 concrete features), invoke `/brainstorm` to spec it out
3. Transform spec into **feature list draft**: 5-30 features, each with:
   - `id` (F001, F002, ...)
   - `category` (core, ui, data, integration, etc.)
   - `description` (one-sentence user-visible behavior)
   - `steps` (3-7 verifiable end-to-end steps, not unit-test steps)
   - `passes: false`
4. **HUMAN GATE:** Present feature list draft for approval before proceeding. User may add, remove, reorder.

### Phase 2: Research (if domain is unfamiliar)

1. Check if the domain requires specialized knowledge (APIs, protocols, frameworks)
2. If yes: invoke `/deepresearch <domain>` for background research
3. Extract actionable findings (libraries to use, patterns to follow, pitfalls to avoid)
4. Update feature list steps if research revealed missing verification approaches

### Phase 3: Project Scaffold (MUST use --harness)

1. Determine target directory:
   - Ask user for target directory, or propose `~/Documents/000_NGM/<PROJECT_NAME>/`
2. Invoke `/project-init <path> --harness --name "<PROJECT_NAME>"` to create:
   - `.claude/` structure (state.md, decisions.md, budget.md, etc.)
   - `CLAUDE.md` and `AGENTS.md` (with Startup Sequence)
   - `docs/feature-list.json` (placeholder F001)
   - `docs/progress.md`
   - `docs/architecture.md`
   - `init.sh`
3. Replace placeholder F001 in `docs/feature-list.json` with the approved feature list from Phase 1
4. Fill `docs/architecture.md` top-level structure based on chosen stack
5. Fill `init.sh` with concrete startup commands + smoke test
6. Register in `~/.claude/memory/projects.json`:
   - Add entry with: name, path, type, status: "active", created: today's date
7. Initial git commit: `chore: scaffold project via /build-project`

### Phase 4: Per-Feature Implementation Loop

For EACH feature in `docs/feature-list.json` where `passes: false` (priority order: core first, then ui/data/integration):

1. **Start session**: read `docs/progress.md` last entry, `git log --oneline -10`, run `./init.sh`
2. **Pick feature**: select next `passes: false` feature by priority
3. **Implement**: invoke `/orchestrate "Implement F### (<description>)"` — depth=1
   - Orchestrate handles: decomposition, sub-agent spawning, edit application
   - Budget tier auto-selected based on feature scope
4. **Verify end-to-end**: follow the feature's `steps` array literally, not unit tests
   - If UI feature: use `preview_*` tools or browser automation
   - If CLI feature: run the command, check output matches expected
   - If API feature: issue requests, verify responses
5. **Update feature-list.json**: if ALL steps passed, set `passes: true`. If any failed, leave `false` and document blocker in progress.md
6. **Commit**: `feat(F###): <description>` (or `wip(F###): <blocker>` if blocked)
7. **End session**: append progress.md entry with status and next recommended feature

Loop until all features show `passes: true` OR a feature is blocked 3 times (then escalate to user).

### Phase 5: Project-Level Verification

1. Run `./init.sh` from clean state (fresh shell, no env carryover)
2. Execute README.md setup instructions literally (as a new user would)
3. Run smoke test from init.sh — MUST pass
4. Invoke `/critic` for quality review of all new code
5. If critic finds critical issues: fix, update progress.md, re-run Phase 5

### Phase 6: Finalization

1. Write project README.md (concise, with setup instructions, linking to docs/)
2. Invoke `/checkpoint save` to preserve state
3. **HUMAN GATE:** Present results and ask if user wants to:
   - `git push` to remote
   - Create GitHub repo (if doesn't exist)
   - Continue iterating on not-yet-implemented stretch features

<!-- CACHE_BOUNDARY -->

## Anti-Rationalization Defense

| Rationalization | Why Wrong | Do Instead |
|---|---|---|
| "The requirements are clear, I'll skip the spec phase and start coding" | Unvalidated assumptions surface during implementation as rework; even clear requirements have implicit unknowns | Run spec generation first; validate feature list with user before writing any code |
| "Unit tests passed, I'll mark this feature as passes:true" | Unit tests are not end-to-end verification; the gap between unit success and user-visible behavior is exactly where this harness catches bugs | Follow the `steps` array literally, observing the behavior as a user would |
| "I'll implement three features in parallel since they're independent" | Parallel implementation without per-feature verification corrupts the passes:bool gate; you cannot isolate which commit broke what | Implement one feature at a time; commit after verification; move to next |
| "I'll add this nice-to-have feature since I'm building everything anyway" | Scope creep in green-field projects is the #1 cause of never-finished prototypes | Build only what the feature list requires; log nice-to-haves as F### additions for a future iteration, user-approved |
| "I'll skip the progress.md update, git log is enough" | git log has commit messages, progress.md has session-level narrative and next-feature hints — they serve different orient functions | Update progress.md at the END of every session, before the final commit |
| "Tests can wait until the project is more mature" | Projects without tests from day one never get tests; the smoke test in init.sh is the cheapest place to start | Include smoke test in Phase 3 init.sh; grow it as features land |
| "I'll push directly to main since this is a new project" | Even new projects benefit from branch discipline for rollback | Always work on a feature branch if remote exists; push to main only after human approval |

## Red Flags

STOP and re-evaluate if any of these occur:
- Marking passes:true before running the steps array end-to-end
- Implementing feature N before feature N-1 is verified (out-of-order without reason)
- Committing without updating progress.md at session end
- Starting a new session without running init.sh first
- Feature list draft has fewer than 3 features (probably too vague, invoke /brainstorm)
- One feature has been "in progress" across 3+ sessions without progress (blocker — escalate)

## Verification Checklist

- [ ] `docs/feature-list.json` is valid JSON and every feature has `passes: true`
- [ ] `./init.sh` exits 0 on a fresh shell with no prior state
- [ ] Smoke test inside init.sh executes without errors
- [ ] `docs/progress.md` has an entry for every session that occurred
- [ ] `git log --oneline` shows at least one commit per implemented feature
- [ ] README.md setup instructions tested by running them literally
- [ ] Project appears in `~/.claude/memory/projects.json` with `status: "active"`
- [ ] `/critic` verdict is PASS (no critical issues)

## Safety Constraints

- Never push to remote without explicit human approval
- Never install system-level dependencies without asking
- Never overwrite existing files in the target directory without reading them first
- Budget limit: deep tier max (5-8 agents per feature). Escalate to user if single feature needs more.
- Max-depth=2 is allowed ONLY because build-project delegates to /orchestrate which delegates to workers. Workers at depth=2 MUST work directly (no further sub-orchestration).

## Success Criteria

A project is "built" when:
1. `docs/feature-list.json` shows 100% `passes: true`
2. `./init.sh` smoke test passes from clean state
3. `/critic` finds no critical issues
4. README.md documents setup and usage
5. Project is registered in projects.json
6. All Verification Checklist items pass

Partial builds (some features `passes: false`) are legitimate — they hand off cleanly to future sessions via progress.md. They are NOT declared complete.

## Handoff Metadata
```yaml
handoffs:
  on_scaffold_ready: /orchestrate (per feature)
  on_feature_complete: update feature-list.json + commit + progress.md append
  on_build_complete: /verify -> /critic -> /checkpoint
  on_failure: /systematic-debugging
  on_done: /checkpoint save
```
