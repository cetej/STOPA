---
name: scenario
description: Use when exploring edge cases and failure modes BEFORE implementation — prospective, hypothetical analysis. Trigger on 'what could go wrong', 'edge cases', 'explore scenarios'. Do NOT use for debugging an existing failure (/systematic-debugging or /incident-runbook).
argument-hint: <scenario description> [--domain software|product|business|security] [--depth shallow|standard|deep] [--format test-scenarios|use-cases|user-stories|threat-scenarios]
tags: [planning, testing]
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash, AskUserQuestion
model: sonnet
effort: high
maxTurns: 40
disallowedTools: Agent, Edit, Write
---

# Scenario Explorer — Edge Case & Failure Mode Discovery

Autonomous scenario exploration: take a seed scenario, decompose into 12 dimensions, iteratively generate concrete situations, classify, expand edge cases, log everything.

Inspired by autoresearch:scenario pattern — adapted for STOPA conventions.

## Core Idea

Seed scenario → Decompose into dimensions → Generate ONE situation per iteration → Classify (new/variant/duplicate) → Expand edge cases → Log → Repeat.

<!-- CACHE_BOUNDARY -->

## Phase 0: Setup

### Parse input

From `$ARGUMENTS`, extract:
- **scenario**: description of what to explore (required — ask if missing)
- **--domain**: software | product | business | security | marketing (auto-detect if not set)
- **--depth**: shallow (10 iter) | standard (25) | deep (50) (default: standard)
- **--format**: test-scenarios | use-cases | user-stories | threat-scenarios | mixed (default: based on domain)
- **--focus**: edge-cases | failures | security | scale | happy-path (optional)
- **--scope**: file glob to limit codebase analysis (optional)

If scenario is missing or vague (≤5 words, no actor/action), use `AskUserQuestion` to gather:
1. Scenario description
2. Domain context
3. Primary goal (find edge cases / generate tests / map failures / stress test)
4. Exploration depth

### Read shared memory

Read `.claude/memory/state.md` — check if related task is active.

## Phase 1: Seed Analysis

Parse the scenario and extract:
- Primary actor(s) and roles
- Goal/objective
- Preconditions (what must be true before)
- System components involved
- Data flows and transformations
- External dependencies

If `--scope` provided, read relevant source files to map technical implementation.

Output: `Phase 1 done: [N] actors, [M] components, [K] preconditions`

## Phase 2: Dimension Decomposition

Map scenario into 12 exploration dimensions:

| Dimension | Focus | Priority by domain |
|-----------|-------|-------------------|
| **Happy path** | Normal successful flow | product > all |
| **Error path** | Expected handled failures | software > all |
| **Edge case** | Boundary conditions (min/max/empty/unicode) | software > product |
| **Abuse/misuse** | Adversarial or unintended use | security > all |
| **Scale** | High volume/load | software > business |
| **Concurrent** | Race conditions, simultaneous operations | software |
| **Temporal** | Timeouts, expiry, timezone, scheduling | business > software |
| **Data variation** | Null, empty, special chars, max length | software > product |
| **Permission** | Access control, role escalation, delegation | security > business |
| **Integration** | External system failures, version mismatches | software |
| **Recovery** | Crash recovery, retry logic, data consistency | software > business |
| **State transition** | Invalid transitions, partial updates, rollback | software |

Prioritize dimensions based on domain. Start with happy path (baseline), then error paths, then domain-specific.

Output: `Phase 2 done: [N] dimensions active, [M] exploration vectors`

## Phase 3-7: Iteration Loop

For each iteration (1 to depth):

### Step 3: Generate ONE situation

Pick highest-priority unexplored dimension/combination. Generate:

```markdown
### [DIMENSION] Situation: <descriptive title>

**Actors:** <who>
**Precondition:** <what must be true>
**Trigger:** <what action initiates this>
**Flow:**
1. <step 1>
2. <step 2>
3. <step N>
**Expected outcome:** <what should happen>
**What could go wrong:** <failure points>
**Severity:** Critical | High | Medium | Low
```

Generation strategies (rotate):
1. **Dimension walk** — pick next unexplored dimension
2. **Combination** — combine 2 dimensions (edge case + concurrent)
3. **Negation** — take happy path step, negate it
4. **Amplification** — take existing situation, push one parameter to extreme
5. **Persona shift** — same scenario, different actor
6. **Temporal shift** — same scenario at different time (peak load, maintenance)
7. **Semi-formal reasoning** (arXiv:2603.01896) — construct explicit premises from preconditions, then derive implications:
8. **Leverage point shift** (Meadows) — identify which leverage level the scenario touches, then generate scenarios at adjacent levels:
   - Current scenario affects a parameter (#12)? Generate a scenario where the same failure propagates to an information flow (#6) — who stops seeing critical data?
   - Current scenario affects rules (#5)? Generate a scenario where the rule change reshapes the system goal (#3)
   - Use leverage hierarchy: 12-Parameters → 9-Delays → 6-Information → 5-Rules → 3-Goals → 2-Paradigm
   - This catches cascading failures that single-level analysis misses
   - List known premises (P1: "user is authenticated", P2: "cart has items", P3: "payment gateway is reachable")
   - Negate one premise and trace the logical consequence through the flow
   - This catches failures that intuitive generation misses because it forces explicit reasoning about invariants

### Step 4: Classify

| Classification | Criteria | Action |
|---|---|---|
| **New** | Not covered by existing | KEEP |
| **Variant** | Similar but meaningfully different | KEEP as sub-scenario |
| **Duplicate** | Already covered | DISCARD — log reason |
| **Out of scope** | Doesn't match seed | DISCARD |
| **Low value** | Technically possible but unrealistic | DISCARD |

### Step 5: Expand edge cases

For each KEPT situation, derive 1-3 additional scenarios using:
- **What-if** — change one variable
- **Boundary** — push values to limits
- **Interruption** — inject failure mid-flow
- **Missing data** — remove expected input
- **Stale data** — use outdated information

### Step 6: Log to TSV

Append to `scenario-results.tsv`:
```tsv
iteration	dimension	classification	severity	title	description	parent
1	happy_path	new	-	Successful checkout	Standard flow	-
2	error_path	new	HIGH	Payment declined	Card rejected	-
3	edge_case	new	MEDIUM	Empty cart	0 items checkout	-
```

### Step 7: Progress check

Every 5 iterations, print:
```
=== Scenario Progress (iteration 15) ===
Generated: 12 (8 new, 3 variants, 1 discarded)
Dimensions covered: 7/12 (58%)
Severity: 2 Critical, 4 High, 8 Medium, 4 Low
Gaps: scale, temporal, recovery — unexplored
```

**When stuck** (5 iterations with no new unique situations): print diminishing returns warning.

**Force dimension rotation**: after 3 consecutive same-dimension iterations, switch to least-explored dimension.

## Phase 8: Output

Print all output to stdout in clearly delimited sections (this skill has no Write permission):

### Scenarios
All situations grouped by dimension, full format.

### Edge Cases
Edge cases and failure modes with severity rating.

### Iteration Log (TSV)
Full iteration log in TSV format.

### Summary
Coverage matrix, dimension heatmap, recommendations.

### Output format by domain

| Domain | Default format |
|--------|---------------|
| software | test-scenarios (Given/When/Then) |
| product | user-stories (As a... I want... So that...) |
| business | use-cases (formal) |
| security | threat-scenarios (attacker goal → vector → impact) |
| marketing | user-stories |

## Anti-Patterns

| Anti-Pattern | Why it fails |
|---|---|
| Generate 50 happy paths | No value — one baseline, then explore what breaks |
| Stay in one dimension | Missing coverage — force rotation after 3 consecutive |
| Vague situations | "Something bad happens" is not a scenario — name trigger + flow + impact |
| Skip classification | Duplicates waste iterations |
| Abstract without concrete | "User might experience issues" — name the specific issue |

## Chaining with other skills

After scenario exploration:
- `/systematic-debugging --scope <area>` — hunt bugs in discovered edge cases
- `/security-review` — audit discovered threat scenarios
- `/tdd` — write tests for discovered test scenarios
- `/critic` — review implementation against discovered edge cases

## Rules

1. **ONE situation per iteration** — atomic, evaluate before generating more
2. **Concrete and specific** — every situation must have actor, trigger, flow, outcome
3. **Read-only** — this skill does NOT modify code, only generates analysis
4. **Log everything** — kept AND discarded situations (failures are informative)
5. **Dimension coverage** — aim for breadth first, depth second
6. **Domain-aware** — prioritize dimensions based on domain context

## Error Handling

- If no edge cases found: expand scope or challenge assumptions
- Log discovered anti-patterns to `.claude/memory/learnings/<date>-<desc>.md` with YAML frontmatter
