---
name: autoreason
description: "Use when iteratively improving subjective text (prompts, arguments, copy, research) through adversarial debate. Trigger on 'autoreason', 'improve this text', 'debate this', 'make this more convincing'. Do NOT use for code optimization (/autoresearch) or code review (/critic)."
argument-hint: <file-path or inline text> [domain:text|argument|prompt|copy] [rounds:N] [judges:N]
tags: [code-quality, research, orchestration]
phase: review
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Agent, AskUserQuestion, TodoWrite
model: sonnet
effort: auto
maxTurns: 40
handoffs:
  - skill: /scribe
    when: "Debate produced reusable findings about writing or argumentation quality"
    prompt: "Record: <key finding from autoreason>"
  - skill: /critic
    when: "Final output needs technical quality gate beyond debate convergence"
    prompt: "Review: <output file path>"
---

# AutoReason — Adversarial Debate Loop for Subjective Text

Extends Karpathy's AutoResearch pattern to domains without numeric metrics.
Instead of optimizing a number, constructs a subjective fitness function through
independent blind evaluation — the same way a journal peer-review panel works.

Inspired by SHL0MS (March 2026), validated by academic debate literature:
Khan et al. ICML 2024 (debate → truthful answers), Liang et al. EMNLP 2024
(Degeneration-of-Thought — reflection alone fails, adversarial debate breaks through),
Feedback Descent (Stanford — structured critique > binary preference).

**When to use vs alternatives:**
- `/autoreason` — "Make this text better" (subjective quality, no numeric metric)
- `/autoresearch` — "Which approach works best?" (code experiments with measurable outcomes)
- `/critic` — "Is this good enough?" (single-pass review, no revision)
- `/council` — "Which option to pick?" (multi-perspective decision, no text iteration)
- `/self-evolve` — "Make this skill better" (eval-case-driven skill improvement)

**Anti-scope:** Do NOT use autoreason for:
- Code that can be tested (`/autoresearch` with eval script)
- Simple factual accuracy (just fact-check it)
- Texts shorter than 100 words (single-pass `/critic` is sufficient)
- Tasks where the user wants a specific voice/style (clarify style first, then maybe autoreason)

## Shared Memory

Read first:
- `.claude/memory/state.md` — current task context
- `.claude/memory/budget.md` — remaining budget
- Grep `.claude/memory/learnings/` for `autoreason` or `debate` tags (max 2 queries)

<!-- CACHE_BOUNDARY -->

## Phase 0: Setup

### Parse input

From `$ARGUMENTS`, extract:
- **target**: file path to improve OR inline text (required)
- **domain**: auto-detect or explicit — `text` | `argument` | `prompt` | `copy` (default: auto-detect)
- **rounds**: max debate rounds (default: 3, max: 5)
- **judges**: judge panel size (default: 3, must be odd)
- **goal**: optional user-stated quality goal (e.g., "more persuasive", "clearer structure")

If target is a file: read it, store as `original_text`.
If target is inline text: store directly as `original_text`.

### Auto-detect domain

| Signal | Domain | Judge Rubric Focus |
|--------|--------|-------------------|
| YAML frontmatter, instruction-like language | `prompt` | Clarity, completeness, no ambiguity, trigger precision |
| Persuasive structure, claims, evidence | `argument` | Logical soundness, evidence quality, counter-argument handling |
| Marketing language, CTA, benefits | `copy` | Hook strength, specificity, action clarity, brevity |
| Everything else | `text` | Coherence, completeness, readability, accuracy |

### Preconditions

1. Text must be ≥100 words (shorter texts don't benefit from debate — suggest `/critic` instead)
2. Check budget — autoreason costs ~5-8 sub-agent calls per round:
   - `rounds × (Writer + Critic + Rewriter + Synthesizer) + rounds × judges + 1 setup`
   - Budget 3 rounds × (4 agents + 3 judges) + 1 = ~22 sub-agent calls
   - If budget tight: reduce to 2 rounds, 3 judges

### Initialize

Create working directory: `outputs/autoreason-<slug>/`
Save original: `outputs/autoreason-<slug>/v0-original.md`
Initialize debate log: `outputs/autoreason-<slug>/debate-log.md`

```markdown
# AutoReason Debate Log

**Target:** <file path or "inline">
**Domain:** <domain>
**Goal:** <user goal or "general improvement">
**Date:** <YYYY-MM-DD>

| Round | Winner | Judge Votes | Delta Summary |
|-------|--------|-------------|---------------|
| 0 | — | — | Original text |
```

## Phase 1: Generate Domain Rubric

Before debate starts, generate a scoring rubric tailored to the domain.
This rubric is the "constitution" judges use — it prevents arbitrary preferences.

### Rubric structure (5 dimensions, domain-specific)

For each domain, generate 5 scoring dimensions. Each dimension:
- Name (2-3 words)
- Description (1 sentence — what it means)
- Weight (1-3, how much it matters for this domain)

**Example rubrics by domain:**

`prompt`:
| Dimension | Weight | Description |
|-----------|--------|-------------|
| Trigger Precision | 3 | Does the description clearly specify when to use AND when not to use? |
| Instruction Clarity | 3 | Can an LLM follow these instructions without ambiguity? |
| Scope Control | 2 | Does it prevent scope creep and stay focused? |
| Error Handling | 1 | Does it specify what to do when things go wrong? |
| Composability | 1 | Can this work alongside other skills without conflict? |

`argument`:
| Dimension | Weight | Description |
|-----------|--------|-------------|
| Logical Soundness | 3 | Are claims supported by valid reasoning chains? |
| Evidence Quality | 3 | Are claims backed by specific, verifiable evidence? |
| Counter-Arguments | 2 | Are opposing views acknowledged and addressed? |
| Persuasiveness | 2 | Would a skeptical reader be convinced? |
| Structure | 1 | Does the argument flow logically from premise to conclusion? |

`copy`:
| Dimension | Weight | Description |
|-----------|--------|-------------|
| Hook Strength | 3 | Does the first sentence compel reading further? |
| Specificity | 3 | Are claims concrete with numbers/examples, not vague? |
| Action Clarity | 2 | Is it clear what the reader should do next? |
| Brevity | 2 | Is every word pulling weight? No filler? |
| Voice Consistency | 1 | Does the tone stay consistent throughout? |

`text`:
| Dimension | Weight | Description |
|-----------|--------|-------------|
| Coherence | 3 | Does the text flow logically with clear transitions? |
| Completeness | 2 | Are all important points covered? |
| Accuracy | 2 | Are facts and claims correct? |
| Readability | 2 | Is it easy to parse on first read? |
| Conciseness | 1 | Is it as short as it can be without losing substance? |

Save rubric to `outputs/autoreason-<slug>/rubric.md`.

Present rubric to user:
> "Generated scoring rubric for domain '{domain}'. Does this capture what you care about, or should I adjust dimensions/weights?"

If user adjusts: update rubric. Then proceed.

## Phase 2: Debate Loop

`current_best = original_text` (v0)

For each round (1 to `rounds`):

**SEPL operator mapping** (ref: `rules/sepl-operators.md`): Step 1 Critic = ρ Reflect | Step 2 Rewriter = σ Select | Step 3 Synthesizer = ι Improve | Step 4 Judges = ε Evaluate | Step 5 Tally = κ Commit.

### Step 1 (ρ Reflect): Critic Agent (Sonnet sub-agent, cold-start)

Spawn a **fresh** sub-agent with adversarial system prompt. Critical: this agent sees ONLY the current_best text and rubric — NO debate history, NO prior critiques.

```
System: You are a ruthless but fair text critic. Your job is to find genuine
weaknesses — not nitpick, not praise. You identify the 3-5 most impactful
problems that, if fixed, would most improve the text.

Rules:
- Do not suggest fixes or rewrites — the adversary role is to stress-test, not to help; providing solutions biases the advocate toward the adversary's preferred fix
- Each problem must reference a specific passage or section
- Rate each problem: critical (must fix) / important (should fix) / minor
- Be honest: if the text is already strong on a dimension, say so
- Do NOT invent problems to fill a quota
```

Agent receives:
```
## Text to Critique

{current_best}

## Scoring Rubric

{rubric}

## Goal

{user goal or "general improvement"}

Identify the 3-5 most impactful weaknesses. For each:
1. Quote the problematic passage (max 15 words)
2. Explain the problem
3. Rate: critical / important / minor
4. Which rubric dimension it affects
```

Save critique to `outputs/autoreason-<slug>/round-{N}-critique.md`

**Early exit check:** If Critic finds 0 critical and ≤1 important problems → text has converged. Skip remaining steps, jump to Phase 3.

### Step 2 (σ Select): Rewriter Agent (Sonnet sub-agent, cold-start)

Spawn a **fresh** sub-agent. Sees: original text, current_best, critique, rubric. Does NOT see prior rounds or debate history.

```
System: You are a precision rewriter. Given a text and a critique, produce an
improved version that addresses the identified problems while preserving everything
that works well. Make surgical improvements, not wholesale rewrites.

Rules:
- Address EVERY critical and important problem from the critique
- Preserve the original voice, structure, and intent
- Do not add new content that wasn't prompted by the critique
- Mark your key changes with <!-- CHANGE: description --> comments (stripped later)
```

Agent receives:
```
## Original Text (for reference — preserve intent)

{original_text}

## Current Version (to improve)

{current_best}

## Critique to Address

{critique}

## Rubric

{rubric}

Produce an improved version. Address all critical and important problems.
```

Save rewrite to `outputs/autoreason-<slug>/round-{N}-rewrite.md`
Strip `<!-- CHANGE: ... -->` markers, log them to debate-log.

### Step 3 (ι Improve): Synthesizer Agent (Sonnet sub-agent, cold-start)

Spawn a **fresh** sub-agent. Sees: current_best AND rewrite. Does NOT see critique or debate history.

```
System: You are a text synthesizer. Given two versions of the same text, produce
the best possible combination. Take the strongest elements from each version.
Your output must be a complete, coherent text — not a diff or list of changes.

Rules:
- Default to the rewrite where it clearly improves on the original
- Keep the current_best's phrasing where the rewrite didn't meaningfully improve it
- Resolve any inconsistencies between merged sections
- The result must read as if written by one person in one pass
- Length should be within ±20% of current_best (no bloat)
```

Agent receives:
```
## Version A

{current_best}

## Version B

{rewrite}

## Rubric (for quality reference)

{rubric}

Synthesize the best version combining strengths of both.
```

Save synthesis to `outputs/autoreason-<slug>/round-{N}-synthesis.md`

### Step 4 (ε Evaluate): Blind Judge Panel (Haiku sub-agents, parallel, cold-start)

Spawn `judges` (default 3, recommended 5-7) **independent Haiku** sub-agents in parallel.
Each judge evaluates **all THREE candidates**: A (incumbent), B (rewrite), AB (synthesis) — with randomized labels.

**Why 3 candidates (autoreason, NousResearch 2026):** Ablation shows removing either B or AB alone collapses performance. All three roles are necessary. Including B prevents prompt bias — "do nothing" (A) always competes as a legitimate option.

Critical anti-bias measures:
- Labels are 3 random letters (e.g., P/Q/R — not sequential X/Y/Z)
- Order is randomized per judge (different permutation of candidates per judge)
- Judges do NOT see critique, rewrite, or debate history
- Judges do NOT know which version is "current best"
- Judges RANK all 3 (first/second/third), not just pick a winner

```
System: You are a blind text evaluator. You will see three versions of a text
labeled with random letters. Rank them from best to worst against the rubric.
Do NOT try to figure out which is "original" vs "improved" — evaluate purely on quality.
```

Each judge receives:
```
## Rubric

{rubric}

## Goal

{user goal}

## Version {LABEL_1}

{candidate_1 — order randomized}

## Version {LABEL_2}

{candidate_2 — order randomized}

## Version {LABEL_3}

{candidate_3 — order randomized}

For each rubric dimension, briefly note which version is strongest.
Then provide your ranking:
RANK 1 (best): {label}
RANK 2: {label}
RANK 3 (worst): {label}
Reason: <1-2 sentences summarizing why the top-ranked version wins>
```

### Step 5 (κ Commit): Tally and Decide (Borda Count)

De-randomize labels → map ranks back to A (incumbent), B (rewrite), AB (synthesis).

**Borda scoring** (3 candidates): RANK 1 = 2pts, RANK 2 = 1pt, RANK 3 = 0pts.
Sum across all judges. Candidate with highest total wins.

Example (3 judges):
```
Judge 1: AB(2) > A(1) > B(0)
Judge 2: B(2)  > AB(1) > A(0)
Judge 3: AB(2) > B(1)  > A(0)
Totals:  A=1,  B=3,  AB=5  →  AB wins
```

Decision:
- **AB wins**: `current_best = synthesis`, k_consecutive = 0 (improvement)
- **B wins**: `current_best = rewrite`, k_consecutive = 0 (improvement, adversarial was better)
- **A wins**: `current_best` unchanged, k_consecutive += 1 (no improvement — incumbent held)

Log to debate-log:
```
| Round | Winner | Borda Scores | Delta Summary |
| {N} | AB / B / A | A=1 B=3 AB=5 | Fixed hook weakness, tightened CTA |
```

Save judge scores and Borda totals to `outputs/autoreason-<slug>/round-{N}-judges.md`

### Step 6: Convergence Check

Track `k_consecutive` = number of consecutive rounds where **A (incumbent) won Borda vote**.

**Exit early if ANY:**
- k_consecutive ≥ 2 (incumbent held for 2 consecutive rounds — text has converged)
- Critic found 0 critical + ≤1 important problems (Step 1 early exit)
- Round limit reached
- All rubric dimensions scored ≥4 by all judges

**Continue if:**
- B or AB won Borda vote (k_consecutive = 0) and rounds remain
- Critic still finding critical problems

### Progress Display (every round)

```
=== AutoReason Round {N}/{max_rounds} ===
Domain: {domain}
Current champion: v{N} (since round {when_it_won})
This round: {winner} won {votes}
Critic findings: {N_critical} critical, {N_important} important
Rubric scores: {dimension}: {avg_score}, ...
```

## Phase 3: Synthesis Report

Write final output to `outputs/autoreason-<slug>/final.md`:

```markdown
# AutoReason Report: {target}

**Date:** {YYYY-MM-DD}
**Domain:** {domain}
**Rounds:** {used} / {max}
**Exit reason:** {convergence | round_limit | critic_clear | max_quality}

## Final Version

{current_best — the champion text}

## Debate Summary

| Round | Winner | Judge Votes | Key Improvements |
|-------|--------|-------------|-----------------|
{debate log rows}

## Rubric Scores (Final vs Original)

| Dimension | Weight | Original | Final | Delta |
|-----------|--------|----------|-------|-------|
{per-dimension comparison from first and last judge rounds}

## Key Improvements Made
- {bullet list of substantive changes, derived from critique→synthesis deltas}

## What the Debate Couldn't Resolve
- {any persistent critic findings that synthesis didn't fully address}
- {rubric dimensions that didn't improve despite attempts}
```

If target was a file: ask user "Replace original file with improved version?"
- Yes: overwrite the original file, keep backup in outputs/
- No: keep both, point user to outputs/ directory

## Phase 4: Handoff

1. Present summary in chat: round count, key improvements, rubric score deltas
2. If target was a skill prompt: remind user to sync commands/ ↔ skills/
3. Update `.claude/memory/budget.md` with debate costs
4. If significant writing insights emerged: suggest `/scribe`

## Cost Model

| Component | Model | Count per Round | Calls (3 rounds) |
|-----------|-------|----------------|-------------------|
| Critic | Sonnet | 1 | 3 |
| Rewriter (B) | Sonnet | 1 | 3 |
| Synthesizer (AB) | Sonnet | 1 | 3 |
| Judge × 5 (default) | Haiku | 5 | 15 |
| **Total per round** | | **8** | **24** |
| + Setup (rubric) | Sonnet | 1 | **1** |
| **Grand total (standard)** | | | **~25 calls** |

Note: judges now rank 3 candidates (A/B/AB) via Borda count — each judge call is slightly heavier than 2-way comparison. Budget scales with `judges` parameter.

Intensity levels (NOT orchestration tiers — these control debate rounds, not agent allocation):
- **light**: 1 round, 3 judges (~10 calls) — quick polish
- **standard**: 3 rounds, 5 judges (~25 calls) — default, good for most texts
- **deep**: 5 rounds, 7 judges (~42 calls) — important documents, research artifacts (7 judges = 3× faster convergence per autoreason ablations)

## Circuit Breakers

| Trigger | Action |
|---------|--------|
| 2 consecutive rounds where current_best wins | STOP — text has converged |
| Critic finds 0 critical problems | STOP — quality sufficient |
| All rubric dimensions ≥4 from all judges | STOP — max quality reached |
| Round limit reached | STOP — normal exit |
| Budget exceeded | STOP — synthesize with what you have |

## Anti-Patterns to Avoid

| Rationalization | Why Wrong | Do Instead |
|------------|-----------|------------|
| "Let me show the rewriter the previous debate history" | Context contamination → confirmation bias | Cold-start every agent |
| "The synthesis is clearly better, skip the judges" | Subjective assessment without blind evaluation | Always run judge panel |
| "Let me use Opus for judges" | Expensive overkill — judges need comparison skill, not deep reasoning | Haiku for judges, Sonnet for writers |
| "I'll run 10 rounds to perfect it" | Diminishing returns after 3-4 rounds; overfitting to rubric | Cap at 5, trust convergence signals |
| "Let me generate the rubric myself without user input" | Rubric is the fitness function — user must validate it | Always present rubric for approval |
| "The rewriter should see the synthesis too" | Role contamination — rewriter addresses critique, synthesizer merges | Keep roles strictly separate |
| "I'll skip B from the judge panel — synthesis already incorporates it" | Ablation (autoreason 2026): removing B alone collapses performance; A/B/AB as a triad is necessary | Always include all 3 candidates in Borda panel |
| "I'll use 3 judges to save tokens" | 3 judges converge 3× slower than 7; minimum practical is 5 for important texts | Use 5 judges for `standard`, 7 for `deep` |
| "Let me upgrade writers from Sonnet to Opus for better output" | Empirically Haiku 3.5 hit 42/42 with this loop — gain comes from A/B/AB structure, not model scale (Principle 10) | Keep Sonnet for writers, Haiku for judges; spend the budget on more rounds/judges instead |
| "I'll skip incumbent A — synthesis is always better" | Without A, naive loops shrink text each pass (345→102 reported) — A is the structural safeguard against monotonic deletion | Always include A in Borda panel |

## Key Design Principles (from literature)

1. **Cold-start isolation** — each agent gets fresh context, no history bleed (SHL0MS)
2. **Structured critique > binary preference** — critique text is directional, win/loss is not (Feedback Descent, Stanford)
3. **Panel > single judge** — 3+ diverse judges reduce bias, cheaper than 1 large judge (PoLL, arXiv:2404.18796)
4. **Randomized labels** — prevents position bias in 3-way ranking (Chatbot Arena methodology, extended to 3 candidates)
5. **Debate only when it helps** — for simple/short texts, single-pass is both cheaper and equally good (Wynn et al. ICML 2025 — naive debate can hurt)
6. **Degeneration of Thought** — once an LLM is confident, self-reflection fails; external adversarial input breaks through (Liang et al. EMNLP 2024)
7. **A/B/AB tournament necessity** — all three candidates are structurally necessary; ablation shows removing either B or AB alone collapses performance (autoreason, NousResearch 2026)
8. **Borda count > majority vote** — rank aggregation across 3 candidates captures preference intensity, not just binary win/loss; prevents split-vote failure modes (Borda 1784, applied to LLM judging by autoreason 2026)
9. **Incumbent preservation** — A (unchanged) always competing prevents prompt-bias assumption that "improvement is always possible" (autoreason 2026)
10. **Mid-tier sweet spot** — empirically the structure carries more signal than model scale: Haiku 3.5 reached perfect 42/42 with this loop while standard self-refinement degraded the same model's output below a single unrefined pass. Mid-tier recovery rate ~62% vs ~43% for frontier-only baselines. Implication: do NOT upgrade writers to Opus thinking it will help — the loop's gain comes from A/B/AB triáda + blind judges, not from raw model capability (autoreason 2026)
11. **Beware monotonic shrinkage** — naive self-refinement loops without an A baseline tend to delete content each pass (one reported case: 345 → 102 words). The incumbent-A vote is the structural safeguard; never disable it to "speed things up" (autoreason 2026)
