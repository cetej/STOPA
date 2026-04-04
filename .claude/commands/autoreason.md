---
name: autoreason
description: "Use when iteratively improving subjective text (prompts, arguments, copy, research) through adversarial debate. Trigger on 'autoreason', 'improve this text', 'debate this', 'make this more convincing'. Do NOT use for code optimization (/autoresearch) or code review (/critic)."
argument-hint: <file-path or inline text> [domain:text|argument|prompt|copy] [rounds:N] [judges:N]
tags: [code-quality, research, orchestration]
phase: review
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Agent, AskUserQuestion, TodoWrite
model: sonnet
effort: high
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

### Step 1: Critic Agent (Sonnet sub-agent, cold-start)

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

### Step 2: Rewriter Agent (Sonnet sub-agent, cold-start)

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

### Step 3: Synthesizer Agent (Sonnet sub-agent, cold-start)

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

### Step 4: Blind Judge Panel (Haiku sub-agents, parallel, cold-start)

Spawn `judges` (default 3) **independent Haiku** sub-agents in parallel.
Each judge sees the SAME two candidates but with **randomized labels** (X/Y instead of A/B, randomized order per judge).

Critical anti-bias measures:
- Labels are random letters (X, Y — not sequential A, B)
- Order is randomized per judge (judge 1 sees X=current, Y=synthesis; judge 2 sees X=synthesis, Y=current)
- Judges do NOT see critique, rewrite, or debate history
- Judges do NOT know which version is the "current best"

```
System: You are a blind text evaluator. You will see two versions of a text
labeled with random letters. Score each version against the rubric dimensions.
Pick the better version. You must NOT try to figure out which is the "original"
or "improved" version — evaluate purely on quality.
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

For each rubric dimension:
1. Score Version {LABEL_1}: 1-5
2. Score Version {LABEL_2}: 1-5
3. Brief justification (1 sentence)

Then: WINNER: {LABEL_1 or LABEL_2}
Reason: <1 sentence why>
```

### Step 5: Tally and Decide

De-randomize labels → map back to current_best vs synthesis.

Count votes:
- If synthesis wins majority: `current_best = synthesis` (new champion)
- If current_best wins majority: current_best holds (debate didn't improve it this round)
- If tie (only possible with even judges — shouldn't happen with odd panel): current_best holds (conservative)

Log to debate-log:
```
| Round | Winner | Judge Votes | Delta Summary |
| {N} | synthesis / current_best | 2-1 / 3-0 | Fixed hook weakness, tightened CTA |
```

Save judge scores to `outputs/autoreason-<slug>/round-{N}-judges.md`

### Step 6: Convergence Check

**Exit early if ANY:**
- Current_best won judge vote (no improvement this round) for **2 consecutive rounds**
- Critic found 0 critical + ≤1 important problems (Step 1 early exit)
- Round limit reached
- All rubric dimensions scored ≥4 by all judges

**Continue if:**
- Synthesis won and rounds remain
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
| Rewriter | Sonnet | 1 | 3 |
| Synthesizer | Sonnet | 1 | 3 |
| Judge × 3 | Haiku | 3 | 9 |
| **Total per round** | | **6** | **18** |
| + Setup (rubric) | Sonnet | 1 | **1** |
| **Grand total** | | | **~19 calls** |

Budget tiers:
- **light**: 1 round, 3 judges (~7 calls) — quick polish
- **standard**: 3 rounds, 3 judges (~19 calls) — default, good for most texts
- **deep**: 5 rounds, 5 judges (~31 calls) — important documents, research artifacts

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

## Key Design Principles (from literature)

1. **Cold-start isolation** — each agent gets fresh context, no history bleed (SHL0MS)
2. **Structured critique > binary preference** — critique text is directional, win/loss is not (Feedback Descent, Stanford)
3. **Panel > single judge** — 3+ diverse judges reduce bias, cheaper than 1 large judge (PoLL, arXiv:2404.18796)
4. **Randomized labels** — prevents position bias in pairwise comparison (Chatbot Arena methodology)
5. **Debate only when it helps** — for simple/short texts, single-pass is both cheaper and equally good (Wynn et al. ICML 2025 — naive debate can hurt)
6. **Degeneration of Thought** — once an LLM is confident, self-reflection fails; external adversarial input breaks through (Liang et al. EMNLP 2024)
