# Competitive Analysis: GitHub Spec Kit

**Date:** 2026-03-23
**Repo:** https://github.com/github/spec-kit
**Stars:** 81,364 (7 months — fastest-growing dev tool category)
**Language:** Python | **License:** MIT

## What It Is

Spec-Driven Development (SDD) toolkit from GitHub (the company). CLI tool `specify` bootstraps projects with a structured pipeline where specs generate code, not the other way around.

## Pipeline: 8 Commands

| Command | Purpose | STOPA Equivalent |
|---------|---------|-----------------|
| `/speckit.constitution` | Project governance principles (immutable authority) | **GAP** — žádný ekvivalent |
| `/speckit.specify` | PRD from idea (user stories, acceptance criteria) | `/brainstorm` (partial) |
| `/speckit.clarify` | Reduce spec ambiguity (max 5 questions) | — (inline v brainstorm) |
| `/speckit.plan` | Technical implementation plan | `/orchestrate` planning phase |
| `/speckit.tasks` | Task breakdown with [P] parallel markers | `/orchestrate` task decomposition |
| `/speckit.analyze` | Cross-artifact consistency check (read-only) | `/critic` (partial) |
| `/speckit.checklist` | Requirements quality validation | **GAP** — requirements-level checks |
| `/speckit.implement` | Execute tasks phase by phase | `/orchestrate` execution |

## Key Differentiators vs STOPA

### Spec-Kit Strengths
1. **Spec-centric model** — documents are source of truth, code is generated output
2. **Constitution as authority** — non-negotiable project principles, violations = CRITICAL severity
3. **27 AI agent support** — Claude, Gemini, Copilot, Cursor, Codex, Windsurf, Kiro...
4. **Extension marketplace** — 22 community extensions (Jira, fleet, cognitive-squad, verify)
5. **Preset system** — domain-specific template overrides (healthcare, Spring Boot)
6. **"Checklists as unit tests for requirements"** — conceptual reframe that changes checklist quality
7. **GitHub brand** — institutional credibility, Copilot integration from day one
8. **Offline/enterprise support** — air-gapped wheel bundling (v0.4.0)

### STOPA Strengths
1. **Execution-centric** — optimized for getting work done, not generating documents
2. **Richer agent orchestration** — budget tiers, circuit breakers, 3-fix escalation, status codes
3. **Anti-rationalization tables** — explicit safeguards against AI self-deception
4. **Two-stage review** — `/critic --spec` + `--quality` with different focus
5. **Harness engine** — deterministic multi-phase pipelines with programmatic validation
6. **Shared memory system** — state, decisions, learnings, budget ledger, news
7. **Hook system** — 12 event-driven hooks for automated behaviors
8. **Deeper methodology** — RLM principles, compound engineering, skill tiers

### Neutral / Different Approach
- Spec-kit = document-first, STOPA = action-first
- Spec-kit groups tasks by user story, STOPA by execution phase
- Spec-kit has templates for spec docs, STOPA has templates for agent prompts
- Both support Claude Code as primary target

## Adoptable Patterns (ranked by value)

### P1: Constitution Concept ★★★
**What:** A `constitution.md` with immutable project principles that ALL other commands check against. Violations are auto-CRITICAL. Semantic versioning for amendments.
**Why valuable:** STOPA lacks a formal "project governance" layer. Constitution bridges the gap between CLAUDE.md (technical instructions) and project intent (what kind of software are we building).
**How to adopt:** New `/specify` skill that creates spec + constitution, or integrate constitution-check into `/orchestrate` planning phase.

### P2: Handoff Metadata in Skills ★★★
**What:** Each command has `handoffs` field suggesting next commands with pre-written prompts. Creates an explicit workflow graph.
**Why valuable:** STOPA skills are loosely coupled — user must know which skill to invoke next. Handoff metadata makes the pipeline self-documenting.
**How to adopt:** Add `handoffs:` field to skill YAML frontmatter. Example: `/brainstorm` → handoffs to `/orchestrate`, `/scout`.

### P3: Checklist-as-Requirements-Tests ★★☆
**What:** Checklists use "Are requirements defined/specified for X?" not "Verify X works". Traceability markers: `[Spec §X.Y]`, `[Gap]`, `[Ambiguity]`.
**Why valuable:** Strengthens `/critic` by adding a requirements-level check layer.
**How to adopt:** Add requirements-check phase to `/critic --spec` mode.

### P4: Hard Question Limits ★★☆
**What:** Max 3 `[NEEDS CLARIFICATION]` markers in spec, max 5 clarification questions. Forces informed guesses + documented assumptions.
**Why valuable:** Prevents AI from over-asking. Our `/brainstorm` could benefit from this constraint.
**How to adopt:** Add numeric limits to `/brainstorm` skill.

### P5: Incremental State Commits ★★☆
**What:** `/clarify` saves to disk after EACH answer, not at the end. P7 (Accumulate) pattern.
**Why valuable:** Prevents losing partial progress in long sessions.
**How to adopt:** Already partially implemented in STOPA memory system, but not consistently in all skills.

### P6: User-Story-First Task Organization ★☆☆
**What:** Tasks grouped by user story (US1, US2, US3) with independent testability checkpoints.
**Why valuable:** Enables MVP-first delivery. But conflicts with STOPA's execution-phase approach.
**How to adopt:** Optional flag for `/orchestrate` — not default.

## Not Worth Adopting

- **Multi-agent format rendering** (27 agents) — STOPA targets Claude Code only, not worth the complexity
- **Extension marketplace** — premature for STOPA's scale
- **Preset system** — plugin distribution already covers this
- **Offline bundling** — not needed for our use case

## Strategic Assessment

Spec-kit is a **documentation-generation tool** that happens to also trigger implementation. STOPA is an **orchestration system** that happens to also produce documentation. Different niches.

**Threat level: LOW.** Spec-kit is complementary, not competing. A user could use spec-kit for spec generation and STOPA for execution. The real competition remains Claude Code Flow (23.3k★) and Task Master (26.1k★) which are closer to STOPA's execution-centric model.

**Opportunity:** Adopt the 3 best patterns (constitution, handoffs, checklist reframe) to strengthen STOPA without changing its core identity.
