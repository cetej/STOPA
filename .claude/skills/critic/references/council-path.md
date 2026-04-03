# COUNCIL Path (--council flag)

Inspired by Karpathy's LLM Council. Instead of a single sequential pipeline, spawn **3 independent reviewer agents** who cross-review each other anonymously.

## Council Step 1: Parallel Independent Reviews

Spawn **3 sub-agents** (model: haiku) in parallel. Each gets the diff/target and a different review persona:

| Agent | Persona | Focus |
|-------|---------|-------|
| R1 | **Correctness Hawk** | Logic bugs, edge cases, spec compliance. Asks: "Under what inputs does this break?" |
| R2 | **Security & Safety** | OWASP, regressions, side effects, data handling. Asks: "How can this be exploited or cause damage?" |
| R3 | **Simplicity Advocate** | Over-engineering, unnecessary complexity, AI slop, convention violations. Asks: "Is there a simpler way?" |

Each agent receives:
```
Review this code change:
{diff}

Your review persona: {PERSONA_DESCRIPTION}

For each issue found, output:
| Severity | Category | Description | Location |
|----------|----------|-------------|----------|
| high/medium/low | correctness/security/quality/... | specific issue | file:line |

Also provide:
- 1-5 confidence score for overall code quality
- Top 3 strengths of the change
- Top 3 concerns
```

## Council Step 2: Anonymous Cross-Review

Collect the 3 reviews. Label them **Review A, Review B, Review C** — strip persona names.

Spawn **2 sub-agents** (model: sonnet) as judges. Each sees ALL 3 anonymized reviews plus the original diff:

```
You are auditing 3 independent code reviews of the same change.

Original diff:
{diff}

Review A:
{review_1}

Review B:
{review_2}

Review C:
{review_3}

Your task:
1. For each review: what did it catch that others missed? What did it get wrong?
2. Are there issues ALL reviewers missed?
3. Where do reviewers disagree? Who is right?
4. Rank the reviews from most thorough to least.

FINAL RANKING:
1. Review X
2. Review Y
3. Review Z
```

## Council Step 3: Chairman Synthesis

As Chairman, read all 3 reviews (de-anonymized), both judge evaluations, and produce the standard Critic Report format (Impact Radius, Milestones, Scoring Rubric, Verdict).

Key additions for council output:

```markdown
### Council Cross-Review Summary

| Review | Persona | Avg Rank | Unique Finds | Agreed Issues |
|--------|---------|----------|-------------|---------------|
| Review A | Correctness Hawk | 1.5 | 2 | 4 |
| Review B | Security & Safety | 2.0 | 1 | 3 |
| Review C | Simplicity Advocate | 2.5 | 1 | 4 |

**Consensus issues** (flagged by 2+ reviewers):
- ...

**Disputed issues** (flagged by 1, questioned by judges):
- ...
```

Then proceed to standard Phase 4 (JUDGE) scoring and verdict.

**Cost:** 3 x haiku + 2 x sonnet + chairman = ~6 agent calls. More expensive than standard path but produces higher-confidence verdicts for critical code.
