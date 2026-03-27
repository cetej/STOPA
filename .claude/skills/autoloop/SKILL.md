---
name: autoloop
description: Use when iteratively optimizing a file or metric via Karpathy loop. Trigger on 'autoloop', 'optimize skill', 'auto-improve'. Do NOT use for one-shot edits.
context:
  - gotchas.md
argument-hint: <target file/scope> [goal] [verify:<command>] [guard:<command>] [budget:N]
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
model: sonnet
effort: high
maxTurns: 50
disallowedTools: Agent
---

# AutoLoop — Autonomous Optimization Loop

Karpathy autoresearch pattern for Claude Code: constrain scope → define metric → iterate autonomously → keep/revert → compound gains.

## Two Modes

| Mode | Trigger | Metric source |
|------|---------|---------------|
| **File mode** | Target is a file path | Built-in structural scorer (SKILL.md) or LLM-as-judge |
| **Metric mode** | `verify:<command>` provided | External command output (test coverage, benchmark, bundle size...) |

## 8 Critical Rules (from Karpathy's autoresearch)

| # | Rule |
|---|------|
| 1 | **Loop until done** — run all iterations, never ask "should I continue?" |
| 2 | **Read before write** — understand full context before modifying |
| 3 | **One change per iteration** — atomic changes. If it breaks, you know why |
| 4 | **Mechanical verification only** — no subjective "looks good." Use metrics |
| 5 | **Automatic rollback** — failed changes revert instantly via git |
| 6 | **Simplicity wins** — equal results + less code = KEEP |
| 7 | **Git is memory** — read `git log` + `git diff` before each iteration to learn from history |
| 8 | **When stuck, think harder** — re-read, combine near-misses, try radical changes |

## Phase 0: Setup

### Parse input

From `$ARGUMENTS`, extract:
- **target**: file path OR scope glob (required)
- **goal**: what to optimize for (optional — inferred from file type if missing)
- **verify**: command that outputs the metric number (optional — triggers metric mode)
- **guard**: command that must always pass — safety net (optional)
- **budget**: iteration count (default: 10, override with `budget:N`)
- **direction**: `higher` or `lower` is better (auto-detected from goal keywords, or ask)

Examples:
```
/autoloop src/api/*.ts verify:"npm test -- --coverage | grep All | awk '{print $4}'" guard:"npm run typecheck" budget:20
/autoloop .claude/skills/critic/SKILL.md
/autoloop src/index.ts "reduce bundle size" verify:"npx esbuild src/index.ts --bundle --minify | wc -c" direction:lower
```

### Precondition checks

```bash
# 1. Git repo exists?
git rev-parse --git-dir 2>/dev/null || echo "FAIL: not a git repo"

# 2. Clean working tree?
git status --porcelain
# → If dirty: warn and ask to stash/commit first

# 3. Stale lock files?
ls .git/index.lock 2>/dev/null && rm .git/index.lock
```

If any FAIL: stop and inform user. Do not enter the loop with broken preconditions.

### Detect mode

| Condition | Mode |
|-----------|------|
| `verify:` provided | **Metric mode** — use external command |
| Target is `*/SKILL.md` | **File mode** — built-in structural scorer |
| Target is other file | **File mode** — LLM-as-judge or custom scorer |

### Create feature branch

```bash
git checkout -b autoloop/$(basename <target> .md)-$(date +%s)
```

### Initialize TSV results log

```bash
echo "# metric_direction: <higher_is_better|lower_is_better>" > autoloop-results.tsv
echo -e "iteration\tcommit\tmetric\tdelta\tguard\tstatus\tdescription" >> autoloop-results.tsv
```

### Establish baseline (iteration 0)

Run verify/scorer on unmodified state. Record as baseline in TSV:
```
0	a1b2c3d	85.2	0.0	pass	baseline	initial state
```

## Phase 1: Iteration Loop

For each iteration (1 to budget):

### Step 1: Review (git as memory)

**MUST complete ALL steps** — git history is the primary learning mechanism:

1. Read current state of in-scope files
2. Read last 10-20 entries from `autoloop-results.tsv`
3. Run `git log --oneline -10` — see recent experiments (kept vs reverted)
4. If last iteration was "keep": run `git diff HEAD~1` — understand WHAT worked
5. Decide: exploit success (variant of what worked) or explore new approach

**Priority order for next change:**
1. Fix crashes/failures from previous iteration
2. Exploit successes — try variants in same direction
3. Explore new approaches — untried in git history
4. Combine near-misses — two changes that individually didn't help
5. Simplify — remove code while maintaining metric
6. Radical experiment — when incremental changes stall

### Step 2: Modify (one atomic change)

Make ONE focused edit. The one-sentence test: if you need "and" to describe it, it's two changes — split them.

Rules:
- **One change per iteration** — don't rewrite
- **Small, targeted edits** — a hypothesis, not a rewrite
- **Preserve structure** — never break YAML frontmatter or file format
- **In-scope only** — never modify guard/test files

### Step 3: Commit (before verification)

```bash
# Stage ONLY in-scope files (never git add -A)
git add <specific-files>

# Check if there's actually something to commit
git diff --cached --quiet && echo "no-op" || \
git commit -m "experiment(<scope>): <one-sentence description>"
```

If nothing to commit: log as `no-op`, skip verify, next iteration.
If pre-commit hook blocks: fix issue and retry (max 2 attempts), then log as `hook-blocked`.

### Step 4: Verify (mechanical only)

**Metric mode:** Run the verify command, extract the metric number.
**File mode:** Run the built-in scorer (see Scoring section).

Timeout: if verify exceeds 2x normal time, kill and treat as crash.

### Step 5: Guard (regression check)

**Only if `guard:` was configured.** Run guard command after successful verify.

- **Verify** = "Did the metric improve?" (the goal)
- **Guard** = "Did anything else break?" (the safety net)

Guard is pass/fail only (exit code 0 = pass). If guard fails:
1. Revert the change
2. Read guard output to understand WHAT broke
3. Rework the optimization to avoid the regression
4. Re-commit, re-verify, re-guard
5. Max 2 rework attempts, then discard

**NEVER modify guard/test files** — always adapt the implementation instead.

### Step 6: Decide

```
IF metric improved AND (no guard OR guard passed):
    STATUS = "keep"
    # Commit stays. Update current_best.

ELIF metric improved AND guard failed:
    # Rework (max 2 attempts) — see Step 5
    IF rework succeeded: STATUS = "keep (reworked)"
    ELSE: STATUS = "discard" — revert

ELIF metric same or worse:
    STATUS = "discard"
    git revert HEAD --no-edit  # prefer revert (preserves history)
    # Fallback: git revert --abort && git reset --hard HEAD~1

ELIF crashed:
    # See Crash Recovery below
```

**Simplicity override:** If metric barely improved (+<0.1%) but adds complexity → discard.
If metric unchanged but code is simpler → keep.

### Step 7: Log to TSV

Append to `autoloop-results.tsv`:
```
iteration	commit	metric	delta	guard	status	description
5	c3d4e5f	88.3	+1.2	pass	keep	add error handling tests
6	-	87.1	-1.2	-	discard	refactor helpers (broke 2 tests)
7	-	0.0	0.0	-	crash	add integration tests (DB failed)
```

Valid statuses: `baseline`, `keep`, `keep (reworked)`, `discard`, `crash`, `no-op`, `hook-blocked`

### Step 8: Check exit + status block

```
AUTOLOOP_STATUS:
  iteration: <N>
  score: <current>
  delta: <+/-N or 0>
  consecutive_reverts: <count>
  EXIT_SIGNAL: <true|false>
```

Exit when ANY:
- **Plateau**: 5 consecutive discards (raised from 3 — gives more room with guard)
- **Max score**: metric can't improve further
- **Budget**: iteration count hit limit
- **Crash loop**: 3 crashes in a row

Every 5 iterations, print progress summary:
```
=== AutoLoop Progress (iteration 15) ===
Baseline: 85.2 → Current: 92.1 (+6.9)
Keeps: 8 | Discards: 5 | Crashes: 2
```

## Crash Recovery Protocol

| Failure | Response | Count as iteration? |
|---------|----------|-------------------|
| Syntax error | Fix immediately, re-commit | No |
| Runtime error | Attempt fix (max 3 tries), then revert + next | Yes |
| Resource exhaustion (OOM) | Revert, try smaller variant | Yes |
| Infinite loop / hang | Kill after timeout, revert | Yes |
| External dependency | Skip, log, try different approach | Yes |

On crash: always revert to last known-good state before continuing.

## Phase 2: Final Validation (LLM-as-judge)

After loop ends, ONE semantic validation:

**Skill targets:**
> Evaluate on 3 dimensions (1-10): Trigger clarity, Instruction completeness, Integration quality.

**Other targets:**
> Does this file achieve its stated purpose clearly and completely? Score 1-10.

If validation score dropped below 5: warn — structural improvements may have hurt semantic quality.

## Phase 3: Report

```markdown
## AutoLoop Report: <target>

**Goal**: <goal>
**Mode**: file | metric (verify: <command>, guard: <command>)
**Iterations**: <used> / <budget>
**Branch**: autoloop/<name>

### Results Log

| Iter | Metric | Delta | Guard | Status | Description |
|------|--------|-------|-------|--------|-------------|
| 0 | 85.2 | — | pass | baseline | initial state |
| 1 | 87.1 | +1.9 | pass | keep | add auth edge case tests |
| ... |

### Summary
- **Baseline**: <score> → **Final**: <score> (+<total delta>)
- **Kept**: N | **Discarded**: M | **Crashes**: K
- **Validation score**: X/10
- **Exit reason**: budget | plateau | max score | crash loop
- **Guard failures**: N (reworked: M, discarded: K)
```

Ask the user: "Merge branch `autoloop/<name>` into current branch, or discard?"

## Scoring: SKILL.md (built-in)

For `*/SKILL.md` files, use this structural heuristic. Run each check and sum points:

### Positive signals (max 15 points)

| # | Check | Points | How to verify |
|---|-------|--------|---------------|
| S1 | Description has trigger conditions | +2 | Grep description line for: `when`, `use when`, `use this`, `after`, `before`, `trigger` (case-insensitive) |
| S2 | Description is 50-200 chars | +1 | Measure description field length |
| S3 | argument-hint is present and non-empty | +1 | Check frontmatter |
| S4 | effort field is present | +1 | Check frontmatter |
| S5 | Has process/steps section | +1 | Grep for `^##.*[Pp]rocess\|^##.*[Ss]tep\|^## Phase` |
| S6 | Has error/failure handling section | +1 | Grep for `^##.*[Ee]rror\|^##.*[Ff]ail\|^##.*wrong\|circuit.breaker` |
| S7 | References `.claude/memory/` | +2 | Grep for `.claude/memory/` or `memory/state\|memory/learnings\|memory/decisions` |
| S8 | Logs to decisions or learnings | +1 | Grep for `decisions.md\|learnings.md` and context suggests writing |
| S9 | Under 500 lines | +1 | `wc -l` |
| S10 | Has output format section | +1 | Grep for `^##.*[Oo]utput\|^##.*[Ff]ormat\|^##.*[Tt]emplate\|```markdown` |
| S11 | Has rules/guidelines section | +1 | Grep for `^##.*[Rr]ule\|^##.*[Gg]uideline\|^## Rules` |
| S12 | Has shared memory read instruction | +2 | Grep for `Read first\|read.*memory\|Before anything.*read\|Shared Memory` |

### Negative signals (penalties)

| # | Check | Points | How to verify |
|---|-------|--------|---------------|
| N1 | Description is vague | -2 | Grep description for: `useful`, `helpful`, `general.purpose`, `various`, `miscellaneous` |
| N2 | Missing name in frontmatter | -1 | Check frontmatter |
| N3 | Missing description in frontmatter | -2 | Check frontmatter |
| N4 | Over 500 lines | -1 | `wc -l` |

### Scoring implementation

Run these bash commands and sum the results:

```bash
DESC=$(sed -n '/^---$/,/^---$/p' <target> | grep '^description:' | sed 's/^description: *//')
echo "$DESC" | grep -iE 'when|use (this|when)|after|before|trigger' > /dev/null && echo "S1:+2" || echo "S1:0"
LEN=$(echo -n "$DESC" | wc -c)
[ "$LEN" -ge 50 ] && [ "$LEN" -le 200 ] && echo "S2:+1" || echo "S2:0"
sed -n '/^---$/,/^---$/p' <target> | grep -q '^argument-hint:.\+.' && echo "S3:+1" || echo "S3:0"
sed -n '/^---$/,/^---$/p' <target> | grep -q '^effort:' && echo "S4:+1" || echo "S4:0"
grep -qiE '^##.*(process|step|phase)' <target> && echo "S5:+1" || echo "S5:0"
grep -qiE '^##.*(error|fail|wrong)|circuit.breaker' <target> && echo "S6:+1" || echo "S6:0"
grep -q '.claude/memory/' <target> && echo "S7:+2" || echo "S7:0"
grep -qE 'decisions\.md|learnings\.md' <target> && echo "S8:+1" || echo "S8:0"
[ "$(wc -l < <target>)" -lt 500 ] && echo "S9:+1" || echo "S9:0"
grep -qiE '^##.*(output|format|template)|```markdown' <target> && echo "S10:+1" || echo "S10:0"
grep -qiE '^##.*(rule|guideline)' <target> && echo "S11:+1" || echo "S11:0"
grep -qiE 'read first|read.*memory|before anything.*read|shared memory' <target> && echo "S12:+2" || echo "S12:0"
echo "$DESC" | grep -iE 'useful|helpful|general.purpose|various|miscellaneous' > /dev/null && echo "N1:-2" || echo "N1:0"
sed -n '/^---$/,/^---$/p' <target> | grep -q '^name:' && echo "N2:0" || echo "N2:-1"
sed -n '/^---$/,/^---$/p' <target> | grep -q '^description:' && echo "N3:0" || echo "N3:-2"
[ "$(wc -l < <target>)" -ge 500 ] && echo "N4:-1" || echo "N4:0"
```

## Scoring: Generic files

For non-SKILL.md files without `verify:`, create a custom scoring function based on the goal:
- Design 8-12 checks worth ~15 points total using grep/wc/regex
- If automated checks aren't possible, fall back to LLM-as-judge (warn about higher cost)

## Budget Awareness

1. Read `.claude/memory/budget.md` before starting
2. This does NOT count as an agent spawn (runs in main context)
3. Log the autoloop run to budget event log when done
4. Estimated cost: ~2-5k tokens per iteration + ~5k for final validation
