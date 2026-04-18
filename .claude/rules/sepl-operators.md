---
globs: ".claude/skills/{self-evolve,autoloop,autoresearch,autoreason,evolve}/SKILL.md,.claude/commands/{self-evolve,autoloop,autoresearch,autoreason,evolve}.md"
---

# SEPL Operator Algebra — Shared Pattern for Iterative Skills

Ref: Autogenesis Protocol (arXiv:2604.15034), Algorithm 1.

Every iterative improvement skill in STOPA (self-evolve, autoloop, autoresearch, autoreason) should map its phases to the 5 canonical SEPL operators. This formalization enables `/eval` trace analysis, consistent debugging, and shared circuit breakers.

## The five operators

| Op | Signature | Role | Czech |
|----|-----------|------|-------|
| **ρ** Reflect | `Z × V → H` | Trace → hypotheses about failures | Diagnóza |
| **σ** Select | `V × H → D` | Hypotheses → modification proposals | Návrh |
| **ι** Improve | `V × D → Ṽ` | Apply proposed changes to produce candidate | Mutace |
| **ε** Evaluate | `Ṽ × G → S` | Score candidate + check safety invariants | Hodnocení |
| **κ** Commit | `Ṽ × S → V` | Gate: accept if S passes, else rollback | Schválení / rollback |

Where: `V` = evolvable variables (skill/file/prompt), `Z` = execution trace, `H` = hypotheses, `D` = modifications, `G` = goal spec, `S` = eval scores + safety flags.

## Mapping existing STOPA skills

| Skill | ρ Reflect | σ Select | ι Improve | ε Evaluate | κ Commit |
|-------|-----------|----------|-----------|------------|----------|
| **self-evolve** | Read failed eval cases, diagnose root cause | Curriculum agent proposes strategy + case | Executor edits SKILL.md | Run evals, measure pass_rate | Critic gate every 2 rounds + commit-invariants; revert if regression |
| **autoloop** | Review previous iteration's verify output | Propose 1 atomic change | Edit target file | `verify:<cmd>` scalar output | Keep iff score improved; plateau → escalation phase |
| **autoresearch** | Analyze eval output vs hypothesis | Generate next hypothesis (possibly PIVOT) | Implement hypothesis in code | Run locked eval command | Keep iff score improved; batch ASSESS every budget/3 |
| **autoreason** | Critic finds 3-5 problems in text | Rewriter proposes fixes | Synthesizer merges into new draft | Judge panel scores vs rubric | Keep best draft; convergence = N rounds no improvement |

## Required invariants for every iterative skill

1. **Atomicity of ι** — Apply ONE modification per iteration. Batching hides credit assignment.
2. **Safety in ε** — Evaluate MUST include safety checks, not just the primary metric. See `commit-invariants.md`.
3. **Rollback on κ=reject** — The skill MUST restore prior state via Edit (or git), not leave partial mutation.
4. **Trace Z is mandatory** — Every iteration writes a log line (TSV/JSONL) with timestamp, score, kept/discarded, brief rationale.
5. **Convergence check after κ** — Check before next ρ whether to exit (budget, plateau, ceiling).

## Writing the skill

When authoring or editing an iterative skill, explicitly label phases in Workflow section:

```markdown
### Phase 2: Reflect (ρ) — Diagnose failures
<instructions>

### Phase 3: Select (σ) — Propose modifications
<instructions>

### Phase 4: Improve (ι) — Apply change
<instructions>

### Phase 5: Evaluate (ε) — Score + invariants
<instructions>

### Phase 6: Commit (κ) — Gate and log
<instructions>
```

This labeling makes trace replay (`/eval`) and cross-skill comparison possible.

## Non-iterative skills

Skills like `/evolve` (learning audit) and `/scribe` (capture) are NOT iterative — they produce a single decision, not a sequence of candidate states. Do not force ρσιεκ on them.

## Why this matters

Autogenesis's empirical wins (GAIA Level 3 +33pp, AIME24 +71%) came from disciplined operator separation with safety-gated commit. STOPA already does most of this ad-hoc; formalizing it prevents regression when skills are edited.
