---
name: build-project
description: "Use when building a new project from requirements end-to-end. Trigger on 'build project', 'create project', 'postav projekt'. Do NOT use for single features or existing project modifications."
curriculum-hints:
  - "Analyze requirements and identify tech stack before writing any code"
  - "Create project structure and config files first"
  - "Implement core functionality in dependency order"
  - "Add tests and verify each module works"
  - "Wire up integration, run full build, and deploy"
tags: [planning, orchestration]
phase: plan
user-invocable: true
model: opus
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
---

# Build Project — Autonomous Project Builder

You build complete projects from natural language requirements. You chain multiple skills autonomously, with human gates only at critical decision points.

## Pipeline

### Phase 1: Requirements Analysis
1. Parse user requirements — what problem does this solve? Who is the user? What are the constraints?
2. If requirements are vague (< 3 concrete features), invoke `/brainstorm` to spec it out
3. **HUMAN GATE:** Present the spec for approval before proceeding

### Phase 2: Research (if domain is unfamiliar)
1. Check if the domain requires specialized knowledge (APIs, protocols, frameworks)
2. If yes: invoke `/deepresearch <domain>` for background research
3. Extract actionable findings (libraries to use, patterns to follow, pitfalls to avoid)

### Phase 3: Project Setup
1. Determine optimal project location:
   - Ask user for target directory, or propose `~/Documents/000_NGM/<PROJECT_NAME>/`
2. Invoke `/project-init <path>` to create `.claude/` structure
3. Register in `~/.claude/memory/projects.json`:
   - Add entry with: name, path, type, status: "active", created: today's date
4. Create initial `CLAUDE.md` with project-specific instructions derived from the spec

### Phase 4: Implementation
1. Invoke `/orchestrate <implementation plan>` with the full spec
   - Orchestrate handles: decomposition, sub-agent spawning, wave execution
   - Budget tier auto-selected based on scope
2. Monitor orchestrate output for failures or blocks
3. If orchestrate hits a circuit breaker: diagnose, adjust plan, retry once

### Phase 5: Verification
1. Invoke `/verify <project core features>` to prove it works end-to-end
2. If verify fails: use `/systematic-debugging` to find root cause, fix, re-verify
3. Run `/critic` for quality review of all new code

### Phase 6: Finalization
1. Write project README.md (concise, with setup instructions)
2. Invoke `/checkpoint save` to preserve state
3. **HUMAN GATE:** Present results and ask if user wants to:
   - `git push` to remote
   - Create GitHub repo (if doesn't exist)
   - Continue iterating

<!-- CACHE_BOUNDARY -->

## Anti-Rationalization Defense

| Rationalization | Why Wrong | Do Instead |
|---|---|---|
| "The requirements are clear enough, I'll skip the spec phase and start coding" | Unvalidated assumptions surface during implementation as rework; even clear requirements have implicit unknowns | Run spec generation first; validate with user before writing any code |
| "I'll add this nice-to-have feature since I'm building everything anyway" | Scope creep in green-field projects is the #1 cause of never-finished prototypes | Build only what the spec requires; log nice-to-haves for a future iteration |
| "Tests can wait until the project is more mature" | Projects without tests from day one never get tests; the first commit is the cheapest place to add them | Include basic test infrastructure and at least smoke tests in Phase 3 |
| "I'll push directly to main since this is a new project" | Even new projects need branch discipline for rollback; pushing to main removes the safety net | Always work on a feature branch; push to main only after human approval |

## Safety Constraints
- Never push to remote without explicit human approval
- Never install system-level dependencies without asking
- Never overwrite existing files in the target directory without reading them first
- Budget limit: deep tier max (5-8 agents). Escalate to user if task seems to need more.

## Success Criteria
A project is "built" when:
1. Code exists and is syntactically valid
2. `/verify` passes on core features
3. `/critic` finds no critical issues
4. README.md documents setup and usage
5. Project is registered in projects.json

## Handoff Metadata
```yaml
handoffs:
  on_spec_ready: /orchestrate
  on_build_complete: /verify → /critic → /checkpoint
  on_failure: /systematic-debugging
  on_done: /checkpoint save
```
