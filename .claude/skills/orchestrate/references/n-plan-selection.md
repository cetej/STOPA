# N-Plan Selection (deep tier only)

**Skip this section for light, standard, and farm tiers.** Only deep tier tasks warrant the cost of multi-plan evaluation.

Before committing to a single decomposition, generate and evaluate multiple attack vectors. This prevents the most common planning failure: choosing the first plausible approach without considering alternatives that may be simpler, more maintainable, or have smaller blast radius.

**Inspiration:** @systematicls harness design — "have N=5 different plans, have another agent pick the plan that results in easier maintenance and scores higher on clean-code principles."

## Step 1: Generate 3 Attack Vectors

Based on scout results and task context, describe 3 distinct approaches to solving the task. Each approach should differ in at least one of: architecture, entry point, scope, or abstraction level.

```markdown
### Attack Vector Analysis

| # | Approach | Key Idea | Blast Radius | Estimated Complexity |
|---|----------|----------|-------------|---------------------|
| A1 | <name> | <1-sentence description> | <N files> | <low/medium/high> |
| A2 | <name> | <1-sentence description> | <N files> | <low/medium/high> |
| A3 | <name> | <1-sentence description> | <N files> | <low/medium/high> |
```

**Rules for attack vectors:**
- At least one should be the "obvious" approach (what you'd pick without this analysis)
- At least one should optimize for minimal blast radius / simplicity
- At least one should optimize for long-term maintainability / extensibility
- Each must be genuinely viable — no strawmen

## Step 2: Evaluate with Selection Agent

Spawn a Sonnet agent to independently evaluate the 3 approaches:

```
Agent(model: "sonnet", prompt: "
  You are evaluating 3 implementation approaches for this task:

  Task: <task description>
  Success criteria: <criteria>
  Constraints: <constraints>
  Codebase context: <relevant scout findings>

  Approaches:
  <A1, A2, A3 descriptions>

  Score each approach (1-5) on these dimensions:

  | Dimension | A1 | A2 | A3 |
  |-----------|----|----|-----|
  | Blast radius (fewer files = higher) | | | |
  | Maintainability (easy to modify later) | | | |
  | Reversibility (easy to undo if wrong) | | | |
  | Alignment with existing patterns | | | |
  | Risk of cascading failures | | | |
  | Topology fitness (simpler graph = higher, ref: graph-topology.md) | | | |
  | **Total** | | | |

  IMPORTANT: Do NOT just pick the simplest. Pick the one with the best
  overall score. Sometimes the more complex approach is correct if it's
  significantly more maintainable or aligned with existing patterns.

  Output:
  1. Scoring table (filled)
  2. Recommended approach: A1/A2/A3
  3. Why (2-3 sentences)
  4. Risks of the selected approach (1-2 sentences)
")
```

## Step 3: Record Decision

Record the selection in `decisions.md` via scribe pattern:
```
N-Plan selection for <task>: chose A<N> (<approach name>).
Alternatives: A<X> (<reason rejected>), A<Y> (<reason rejected>).
Selection rationale: <agent's reasoning>.
```

If the selection agent's recommendation differs from your initial instinct, **follow the agent's recommendation** — that's the point of the independent evaluation.

**Cost:** 1 × Sonnet agent ≈ minimal overhead for deep tier. The cost of choosing the wrong approach and having to backtrack is 10-100x higher.
