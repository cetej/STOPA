---
name: build-project
description: "Use when building a new project from requirements end-to-end. Trigger on 'build project', 'create project', 'postav projekt'. Do NOT use for single features or existing project modifications."
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
