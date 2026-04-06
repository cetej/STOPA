---
name: learn-from-failure
description: Use when 2+ failures of the same failure_class occur for the same agent, or when user wants systematic failure analysis. Trigger on 'learn from failure', 'analyze failures', 'why does this keep failing'. Do NOT use for one-off debugging (/systematic-debugging) or incident response (/incident-runbook).
argument-hint: "[failure_class] [failure_agent] or 'all' for full analysis"
tags: [memory, debugging, orchestration]
phase: meta
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Agent
model: sonnet
effort: medium
maxTurns: 15
output-contract: "failure learnings → YAML → .claude/memory/learnings/<date>-<desc>.md"
handoffs:
  - skill: /scribe
    when: "After extracting operational rules and behavioral principles"
    prompt: "Record failure learning: <extracted rules>"
  - skill: /evolve
    when: "Behavioral principle is general enough for critical-patterns"
    prompt: "Consider promoting: <principle>"
---

# Learn From Failure — RoPE-lite (HERA-inspired)

Systematická analýza opakujících se selhání s extrakcí operational rules a behavioral principles.
Adaptace HERA Role-aware Prompt Evolution (arXiv:2604.00901) pro STOPA — mental replay místo full trajectory replay.

## When to trigger

- **Auto-trigger**: Orchestrator detekuje 2+ failures se stejným `failure_class` + `failure_agent`
- **Manual**: Uživatel říká "proč to pořád selhává" / "analyze failures"
- **From /eval --failures**: Report identifikuje knowledge gap

## Phase 0: Collect Failure Data

1. Parse arguments — extract `failure_class` and `failure_agent` (or 'all')
2. Read matching failures: `Grep failure_class: <class> .claude/memory/failures/`
3. If `failure_agent` specified: filter further by `Grep failure_agent: <agent>`
4. Read each matched failure file — extract trajectory, root_cause, reflexion
5. Also check learnings: `Grep failure_class: <class> .claude/memory/learnings/` — are there existing learnings that didn't prevent recurrence?

**Minimum data**: Need at least 2 failure records to proceed. If <2, report "insufficient data" and suggest recording more failures via orchestrate.

## Phase 1: Pattern Extraction

Analyze the collected failure trajectories:

1. **Common decision points**: Where in the trajectories does the path diverge from success? Look for the step where the wrong choice was made.
2. **Common assumptions**: What did the failing agent assume that turned out to be wrong?
3. **Common context**: What task_class, complexity, tier were these failures in? Is there a pattern?
4. **Existing learning effectiveness**: If learnings exist for this pattern, why didn't they prevent recurrence?
   - Learning too vague → needs to be more specific
   - Learning not retrieved → tags/component don't match query
   - Learning retrieved but ignored → needs higher severity or different framing

## Phase 2: Mental Replay (RoPE-lite)

For each failure trajectory, simulate 3 alternative approaches:

### Variant A — Efficiency axis
"If the agent had been instructed to minimize steps and take the most direct path, what would have happened differently at the decision point?"

### Variant B — Thoroughness axis
"If the agent had been instructed to check all preconditions, read all related files, and verify assumptions before acting, what would have happened?"

### Variant C — Risk sensitivity axis
"If the agent had been instructed to flag any uncertainty and ask before making assumptions, what would have happened?"

For each variant, answer:
- Would the failure have been avoided? (yes/no/maybe)
- What specific action would have been different?
- What's the trade-off? (e.g., thoroughness costs more tokens but prevents assumption errors)

**Cost**: ~$0.05-0.15 per analysis (vs $9-15 for full replay). Acceptable for routine use.

### Full Replay Escalation

If mental replay is inconclusive (all 3 variants = "maybe"), AND this is the 3rd+ occurrence:
- Escalate to user: "Mental replay inconclusive. Run full replay? (costs ~$3-5 per variant)"
- If approved: spawn 3 sub-agents with variant prompts, execute the actual task, compare results

## Phase 3: Rule Extraction

From the mental replay results, extract two types of improvements:

### Operational Rules (short-term, specific)

Concrete instructions that fix the immediate failure pattern:

```
Format: "When <situation>, always <action> before <risky step>"
Example: "When editing auth code, always read existing tests in tests/auth/ before modifying"
```

Rules should be:
- Actionable (imperative verb)
- Specific (names files, patterns, or conditions)
- Testable (you can verify compliance)

### Behavioral Principles (long-term, general)

Strategic guidance that generalizes across future failures:

```
Format: "<Category>: <principle>"
Example: "Assumptions: Never assume stateless architecture without checking test fixtures"
```

Principles should be:
- General enough to apply beyond this specific failure
- Not so general they're useless ("be careful" is not a principle)
- Traceable to evidence (which failures support this principle?)

## Phase 4: Consolidation (HERA Algorithm 3)

Before writing new learnings, check for conflicts:

1. **Grep existing learnings** with same failure_class + failure_agent
2. For each match, classify relationship:
   - **ADD**: New insight, no overlap → write new file
   - **MERGE**: Complementary to existing → update existing file, add related: link
   - **PRUNE**: Contradicts low-utility existing → supersede old file
   - **KEEP**: Already captured → don't duplicate
3. Write via `/scribe` handoff with failure metadata fields

### Learning Output Format

Each learning gets enriched with failure context:

```yaml
failure_class: <from analysis>
failure_agent: <from analysis>
task_context:
  task_class: <common pattern>
  complexity: <common pattern>
  tier: <common pattern>
source: critic_finding  # or auto_pattern if from pattern detection
```

## Phase 5: Report

```
## Failure Analysis Report
Analyzed: N failures | Class: <failure_class> | Agent: <failure_agent>

### Pattern
<1-2 sentence description of the recurring failure pattern>

### Mental Replay Results
| Variant | Would Prevent? | Key Difference | Trade-off |
|---|---|---|---|
| Efficiency | yes/no/maybe | <action> | <cost> |
| Thoroughness | yes/no/maybe | <action> | <cost> |
| Risk Sensitivity | yes/no/maybe | <action> | <cost> |

### Extracted Rules
**Operational** (apply immediately):
1. <rule>

**Behavioral** (general principle):
1. <principle>

### Actions Taken
- [ ] Wrote learning: <filename>
- [ ] Updated existing: <filename> (MERGE)
- [ ] Superseded: <filename> (PRUNE)
- [ ] Updated agent-accountability.md
```

## Anti-Rationalization Defense

| Rationalization | Why Wrong | Do Instead |
|---|---|---|
| "Two failures isn't enough data to extract patterns" | Two identical failures IS a pattern — waiting for 5 wastes resources | Extract tentative rules from 2, strengthen confidence at 5+ |
| "The failures are in different contexts so they're unrelated" | Same failure_class + failure_agent IS a pattern regardless of context | Focus on the shared root cause, not the surface differences |
| "Mental replay is unreliable so I'll skip it" | Mental replay at $0.10 is 100x cheaper than the next real failure | Run it, mark confidence appropriately, escalate if inconclusive |
| "The existing learning should have prevented this, it just wasn't applied" | If a learning doesn't prevent recurrence, it's ineffective — fix it | Update the learning (better tags, higher severity, clearer action) |
| "I'll just record a generic learning" | Generic learnings have low utility and get pruned | Extract SPECIFIC operational rules with file paths and conditions |

## Red Flags

STOP and re-evaluate if any of these occur:
- Analyzing failures without reading the actual failure trajectory files
- Generating rules that don't reference specific code patterns or file paths
- Skipping the MERGE/PRUNE check against existing learnings
- Writing more than 3 learnings from a single analysis (probably too granular)
- Mental replay results are all "maybe" and you're not escalating

## Verification Checklist

- [ ] Read at least 2 failure records with full trajectories
- [ ] Mental replay completed for all 3 variants with clear yes/no/maybe
- [ ] At least 1 operational rule extracted (specific, actionable, testable)
- [ ] Consolidation check done (no duplicate learnings created)
- [ ] Learning files have all failure metadata fields (failure_class, failure_agent, task_context)
- [ ] Report includes actions taken with filenames

## Rules

1. **Mental replay first** — never skip to rule extraction without simulating alternatives
2. **Specific over general** — operational rules > behavioral principles in value per token
3. **Consolidate, don't accumulate** — MERGE with existing learnings when possible
4. **Cost-aware** — mental replay is default, full replay only on 3rd+ occurrence with user approval
5. **Backward compatible** — if failure records lack some fields, work with what's available
6. **Report in Czech** if user context is Czech
