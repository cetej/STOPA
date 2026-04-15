---
name: discover
description: "Use when surfacing emergent behavioral patterns from session traces — what works, what fails, what repeats. Trigger on 'discover', 'behavior patterns', 'what patterns', 'session analysis'. Do NOT use for single-session review (/critic) or learning audit (/evolve)."
user-invocable: true
allowed-tools: [Read, Glob, Grep, Bash, Write, Edit, Agent, TodoWrite]
tags: [memory, research, session, orchestration]
phase: meta
effort: auto
---

# /discover — Semantic Behavior Discovery

You are a behavior analyst. Your job is to discover emergent patterns in agent
session traces — patterns that were NOT defined in advance. This is the opposite
of traditional observability: you observe first, then classify.

Reference: Leonard Tang, "Towards Semantic Observability" (2026) — ontology
follows execution, not the other way around.

---

<!-- CACHE_BOUNDARY -->

## Input

- `--days N` — analyze last N days of traces (default: 7)
- `--focus <keyword>` — filter traces by tool name or path keyword
- `--compare` — compare this week vs previous week

## Phase 1: AGGREGATE — Collect Raw Behavioral Data

1. Glob `.traces/sessions/*.jsonl` — list all session trace files
2. If no session traces exist, report and EXIT:
   ```
   No session traces found. Session trace capture hook (session-trace.py) may not be active yet.
   Run a few sessions first, then re-run /discover.
   ```
3. Filter by date range (default: last 7 days, parse from filename `YYYY-MM-DD-*.jsonl`)
4. For each session file, read and parse JSONL records
5. Build aggregate data structures:

```
sessions[] = {
  file: string,
  date: string,
  tool_sequence: string[],    // ordered list of tool names
  total_calls: number,
  error_count: number,        // exit != 0
  duration_est: string,       // last_ts - first_ts
  files_touched: string[],    // unique paths from records
  skills_used: string[],      // unique skill names
}
```

**Scale guard**: If >50 session files, sample: take 20 most recent + 10 random from rest.

---

## Phase 2: SEQUENCE — Extract Behavioral Patterns

Analyze tool call sequences as behavioral n-grams:

### 2a: Bigrams (tool → tool transitions)
Count frequency of every (tool_A, tool_B) pair across all sessions.
Top 15 bigrams = the system's behavioral vocabulary.

### 2b: Trigrams (3-tool sequences)
Count frequency of every (tool_A, tool_B, tool_C) triple.
Top 10 trigrams = common micro-workflows.

### 2c: Failure Sequences
Extract all subsequences where `exit != 0`:
- What tool failed?
- What tool came BEFORE the failure? (potential cause)
- What tool came AFTER? (recovery attempt)

### 2d: Session Signatures
For each session, compute a "signature" — the top-3 most frequent tools.
Group sessions by signature → behavioral clusters.

Output:
```
=== BEHAVIORAL VOCABULARY (top bigrams) ===
  Edit → Bash: 47 occurrences (code-then-test)
  Bash → Edit: 31 occurrences (fix-after-fail)
  Grep → Read: 28 occurrences (search-then-read)
  Agent → Agent: 12 occurrences (delegation cascade)
  ...

=== MICRO-WORKFLOWS (top trigrams) ===
  Grep → Read → Edit: 22 (informed editing)
  Edit → Bash → Edit: 18 (edit-test-fix loop)
  ...

=== FAILURE PATTERNS ===
  Bash failures: 15 total
    After Edit: 8 (likely test failures post-edit)
    After Bash: 4 (retry pattern)
  ...

=== SESSION CLUSTERS ===
  Cluster A [Edit, Bash, Read]: 12 sessions — "implementation work"
  Cluster B [Agent, Read, Grep]: 5 sessions — "research/delegation"
  Cluster C [Skill, Edit, Bash]: 4 sessions — "skill-driven development"
  ...
```

### 2e: Primitive Action Sequences (NSM-inspired, arXiv:2602.19260)

Extract reusable micro-operations that compose into larger workflows — analogous to how
NSM learned stacking primitives from 50 demos and composed them into Hanoi solutions.

1. **Identify atomic primitives**: Extract tool sequences of length 2-4 that:
   - Appear in 5+ sessions (high reuse)
   - Always succeed (exit == 0 for all tools in sequence)
   - Are self-contained (don't depend on preceding context beyond file path)

2. **Classify primitives by function**:
   | Primitive | Signature | Function |
   |-----------|-----------|----------|
   | informed-edit | Grep→Read→Edit | Read before write |
   | test-driven | Edit→Bash(test)→pass | Edit with verification |
   | search-navigate | Glob→Read | Find then examine |
   | delegate-verify | Agent→Read(result) | Delegate then check |

3. **Cross-skill primitive usage**: For each primitive, count which skills use it most.
   Primitives used by 3+ different skills = **universal primitives** (candidates for
   skill composition building blocks).

4. **Output**:
   ```
   === PRIMITIVE ACTION SEQUENCES ===
   | # | Primitive | Signature | Frequency | Skills Using | Universal? |
   |---|-----------|-----------|-----------|-------------|-----------|
   | 1 | informed-edit | Grep→Read→Edit | 45 | critic,scout,fix-issue | yes |
   | 2 | test-loop | Edit→Bash→Edit | 31 | tdd,autoloop | no |
   ```

Why: NSM showed that 50 primitive demos > 300 full-task demos. Same principle applies —
understanding which atomic operations compose into successful workflows reveals the
system's implicit "operator library" and can inform skill design.

---

## Phase 3: DISCOVER — Surface Interesting Patterns

For each discovered pattern, classify it into one of these categories:

| Category | Signal | Example |
|----------|--------|---------|
| **healthy** | High grep→read→edit ratio, low retry rate | Informed editing: reads before writes |
| **desperation** | Edit→Bash→Edit→Bash loops (3+ cycles) | Repeated test failures without diagnosis |
| **delegation_cascade** | Agent→Agent chains (3+ deep) | Over-delegation without synthesis |
| **blind_editing** | Edit without preceding Read/Grep | Editing files without reading them first |
| **recovery_success** | Failure → different approach → success | Agent adapted strategy after failure |
| **novel** | Pattern not matching any known category | Flag for human classification |

### Entropy metric
For each session, compute behavioral entropy:
- **Low entropy** (< 1.5): repetitive, possibly stuck in a loop
- **Medium entropy** (1.5-3.0): focused work with variety
- **High entropy** (> 3.0): exploratory, many different tools

Flag sessions with entropy < 1.0 as potential desperation episodes.

### Pattern significance
Only surface patterns that appear in **3+ sessions** (not one-offs).
Exception: patterns with **3+ failures** in a single session always surface.

---

## Phase 4: PRESENT — Output for Human Judgment

Present discovered patterns in a decision table:

```
=== DISCOVERED BEHAVIORAL PATTERNS ===
Period: [date range], [N] sessions analyzed

| # | Pattern | Category | Frequency | Sessions | Verdict |
|---|---------|----------|-----------|----------|---------|
| 1 | Edit→Bash→Edit loop (4+ cycles) | desperation | 8 occurrences | 3 sessions | ? |
| 2 | Grep→Read→Edit→Bash→pass | healthy | 22 occurrences | 9 sessions | ? |
| 3 | Agent→Agent→Agent chain | delegation_cascade | 5 occurrences | 2 sessions | ? |
| 4 | Skill(critic)→Edit | healthy | 12 occurrences | 6 sessions | ? |
| 5 | [unexpected pattern] | novel | 4 occurrences | 3 sessions | ? |

Verdict: ✓ reinforce | ✗ suppress | ? needs human judgment | ~ neutral
```

For each pattern, provide:
1. **Representative example**: one concrete session excerpt showing the pattern
2. **Proposed verdict**: your best guess at classification
3. **Confidence**: how sure you are (based on frequency and outcome data)

### Human judgment prompt
For patterns classified as `novel` or where confidence < 0.6:
```
Pattern #N needs your judgment:
  [description of what happens]
  [1-2 concrete examples from traces]

  Is this behavior:
  (a) Good — reinforce it
  (b) Bad — suppress it
  (c) Neutral — ignore it
  (d) Need more data
```

---

## Phase 5: PERSIST — Save Discovered Patterns

After human classification:

1. **Reinforceable patterns** → write to `.claude/memory/learnings/discovered-patterns.md`:
   ```markdown
   ## [Pattern Name] — reinforceable
   - Signature: [tool sequence]
   - Frequency: [N] in [M] sessions
   - First seen: [date]
   - Human verdict: reinforce
   - Suggested artifact: [best_practice learning | routing hint | skill hint]
   ```

2. **Suppressible patterns** → write to `.claude/memory/learnings/discovered-patterns.md`:
   ```markdown
   ## [Pattern Name] — suppressible
   - Signature: [tool sequence]
   - Frequency: [N] in [M] sessions
   - First seen: [date]
   - Human verdict: suppress
   - Suggested artifact: [warning rule | circuit breaker | panic-detector pattern]
   ```

3. **Novel/unclassified** → keep in discovered-patterns.md with `verdict: pending`
   Re-surface in next /discover run for re-evaluation.

4. If `--compare` flag: show week-over-week delta:
   ```
   TREND: desperation patterns 5→2 (↓ improving)
   TREND: healthy patterns 15→18 (↑ more informed editing)
   NEW: [pattern] appeared this week for the first time
   GONE: [pattern] no longer observed
   ```

---

## Anti-Rationalization Defense

| Rationalization | Why Wrong | Do Instead |
|---|---|---|
| "I'll classify all patterns myself without asking the user" | Novel patterns require human judgment — the whole point of semantic observability is human-in-the-loop discovery | Present novel/low-confidence patterns with concrete examples and ask for classification |
| "There aren't enough traces to analyze, I'll skip" | Even 3-5 sessions can reveal dominant bigrams and failure patterns | Run analysis on whatever data exists, note sample size, flag low-confidence results |
| "I'll only look at failure patterns since those matter most" | Healthy patterns are equally important — reinforcing good behavior prevents drift | Analyze both success and failure sequences with equal attention |
| "The n-gram analysis is too simple, I should use embeddings" | Behavioral n-grams over tool sequences are surprisingly powerful for pattern detection — complexity is not needed | Stick to frequency-based analysis; add complexity only if it fails to surface patterns |

## Red Flags

STOP and re-evaluate if any of these occur:
- Analyzing traces without checking the date range (may include stale data)
- Classifying all patterns as "healthy" without examining failure sequences
- Presenting more than 15 patterns (information overload defeats the purpose)
- Skipping the human judgment step for novel patterns
- Modifying traces or session files (read-only analysis)

## Verification Checklist

- [ ] Session traces were found and parsed (N files, M total records)
- [ ] At least top-10 bigrams computed with concrete frequencies
- [ ] Failure patterns extracted and cross-referenced with preceding tools
- [ ] Each discovered pattern has: category, frequency, session count, confidence
- [ ] Novel/low-confidence patterns presented to user for judgment
- [ ] Results persisted to discovered-patterns.md (after human classification)

## Rules

- NEVER modify trace files — read-only analysis
- NEVER classify novel patterns without human input
- Limit output to max 15 most significant patterns (filter by frequency × impact)
- discovered-patterns.md max 300 lines — archive old entries when approaching limit
- Re-running /discover should show delta from last run (if discovered-patterns.md exists)
- This skill feeds into /evolve Phase 6 (artifact synthesis) — discovered patterns with human verdicts become input for generating executable artifacts
