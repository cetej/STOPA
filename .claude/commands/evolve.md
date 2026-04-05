---
name: evolve
description: Use when reviewing accumulated corrections and session trends to graduate or prune system rules. Trigger on 'run /evolve', 'analyze corrections', 'promote to critical patterns', 'prune old rules', 'cleanup learnings'. Do NOT use for iterative skill improvement (/self-evolve) or file optimization (/autoloop).
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
tags: [memory, documentation, session, orchestration]
phase: meta
---

# /evolve — Learning Evolution Audit

You are the meta-engineer improving the system that runs you.
Read accumulated signals → propose concrete changes → wait for approval → apply.

---

<!-- CACHE_BOUNDARY -->

## Step 1: Load All Signals

Read these files silently:

```
.claude/memory/corrections.jsonl     — user corrections (most valuable signal)
.claude/memory/violations.jsonl      — failed rule checks from verify-sweep
.claude/memory/sessions.jsonl        — session scorecards (trend data)
.claude/memory/learnings/critical-patterns.md  — current always-read patterns
.claude/memory/learnings/            — all learning files (for graduation candidates)
```

If a file doesn't exist, note it and continue.

---

## Step 2: Analyze Corrections

Group corrections.jsonl entries by semantic similarity (keyword overlap):
- Same pattern corrected **2+ times** → **must** be in critical-patterns.md. If not: PROMOTE.
- Correction clusters pointing to a **missing rule** → CREATE new learning.
- Correction that **contradicts** an existing learning → UPDATE (the rule was wrong, not you).

Show groupings:
```
CORRECTION CLUSTER: [pattern description]
  Occurrences: N times
  Examples: [correction 1], [correction 2]
  Action: PROMOTE | CREATE | UPDATE | ALREADY_COVERED
```

---

## Step 3: Analyze Violations

Group violations.jsonl entries by rule source:
- Same rule failing **3+ sessions** → rule not being followed → needs to graduate to `core-invariants.md` or become a linter hook
- Rule failing but already in `core-invariants.md` → implementation issue, not rule placement
- Zero violations across all rules → healthy; note this

Show:
```
VIOLATION PATTERN: [rule]
  Failed: N times across M sessions
  Action: ESCALATE_TO_CORE | ESCALATE_TO_HOOK | INVESTIGATE | OK
```

---

## Step 3b: Confidence-Based Learning Audit

Scan all files in `.claude/memory/learnings/` and evaluate each learning's confidence:

**Compute effective confidence** for each learning:
1. Read `confidence:` field (default 0.7 if missing)
2. Apply decay: if `uses: 0` AND `date:` is 60+ days old → subtract 0.1 per 30 days of inactivity (min 0.1)
3. Apply boost: add `uses × 0.05` (cap at 1.0), subtract `harmful_uses × 0.15`

**Graduation candidates** (`uses >= 10` AND effective confidence >= 0.8 AND `harmful_uses < 2`):
→ Propose PROMOTE to `critical-patterns.md` or GRADUATE to `rules/`

**Pruning candidates** (effective confidence < 0.3):
→ Propose PRUNE — learning has decayed below usefulness threshold

**Decay warnings** (effective confidence 0.3-0.5, not recently used):
→ Flag for review — may need refreshing or superseding

Show:
```
CONFIDENCE AUDIT: [N learnings scanned]
  Graduation ready: [list of filenames with uses/confidence]
  Decay warnings:   [list of filenames with age/confidence]
  Prune candidates: [list of filenames with reason]
```

Include these proposals in Step 7 alongside correction/violation-based proposals.

---

## Step 3c: Model Gate Audit

Inspired by CC `@[MODEL_LAUNCH]` tagging — flag model-specific learnings that may be stale.

1. Read current model from `ANTHROPIC_MODEL` env var or infer from session context
2. Scan all learnings with `model_gate:` field in YAML frontmatter
3. For each where `model_gate` value does NOT match current model:
   ```
   MODEL GATE AUDIT: [N model_gate learnings found]
     Current model: [model string or "unknown"]
     Stale gates:   [learning filenames where gate ≠ current model]
     Action: REVIEW [filename] — verify if still applies
   ```
4. Include in Step 7 proposals as **REVIEW** action (not auto-PRUNE — requires human confirmation)
5. If model_gate matches current model → no action needed, learning is still relevant

---

## Step 3d: Panic Episode Analysis

If `.claude/memory/intermediate/panic-episodes.jsonl` exists and has entries:

1. Group episodes by `trigger_signals` pattern (which signals dominate)
2. Look for recurring patterns:
   - Same signal combination 3+ times → systemic issue, not one-off
   - Escalations (red ignored) → investigate what tasks cause this
3. Cross-reference with `window_summary` for file/error patterns

Show:
```
PANIC EPISODES: [N total, M red, K yellow]
  Dominant pattern: [most common signal combination]
  Recurring triggers: [error types / file clusters that cause panic]
  Action: ADD_TO_RUNBOOK | CREATE_LEARNING | INVESTIGATE
```

If a pattern triggers panic 3+ times → create a learning or runbook entry
so the model recognizes the situation earlier and switches to /systematic-debugging
proactively instead of waiting for the panic detector.

---

## Step 3e: Wiki Freshness Check

If `.claude/memory/wiki/INDEX.md` exists:
1. Read wiki INDEX.md header — extract `Last built` date
2. Compare against newest learning file date (Glob `learnings/2*.md`, sort descending, check first)
3. If wiki is >7 days stale AND new learnings exist since last compile:
   - Add to Step 7 proposals: `RECOMMEND: Run /compile (wiki N days stale, M new learnings since last build)`
4. If wiki INDEX.md shows open contradictions, include note in Step 7

If `.claude/memory/wiki/INDEX.md` does NOT exist:
- Add to Step 7 proposals: `RECOMMEND: Run /compile --full (wiki not yet built, N learnings available)`

This is **advisory only** — evolve does NOT auto-run compile.

---

## Step 4: Analyze Session Trends (sessions.jsonl)

If 5+ entries in sessions.jsonl, calculate:
- Average corrections per session (last 5 vs. previous 5) — is it decreasing?
- Most violated rules (recurring in violations)
- Skills with highest error correlation

Output one-line trend:
```
TREND: Corrections X→Y (↓ improving | → flat | ↑ worsening)
       Most violated: [rule name]
       Healthy sessions: N/M (last M sessions)
```

---

## Step 4c: Skill Usage Audit

Read `.claude/memory/skill-usage.jsonl` (if it exists). Each line is `{"ts":"...","skill":"..."}`.

**Build usage report:**
1. Count invocations per skill (last 60 days)
2. List ALL skills from `.claude/skills/*/SKILL.md` — compare against usage data
3. Identify **stale skills** (0 invocations in 60+ days or never used)
4. Identify **hot skills** (top 5 by usage count)

**Stale skill action:**
- Skill with 0 uses AND tier 3+ (advanced/methodology) → ARCHIVE candidate (move to `.claude/skills-archive/`)
- Skill with 0 uses AND tier 1-2 → Flag for review — maybe it should be used more, not archived

Show:
```
SKILL USAGE AUDIT: [N skills total, M with usage data]
  Hot skills (top 5):  [skill: N calls] ...
  Stale (60+ days):    [list with tier]
  Never invoked:       [list]
  Action: ARCHIVE [skill] | REVIEW [skill] | OK
```

If skill-usage.jsonl doesn't exist or is empty, note "No usage data yet — tracking started" and skip.

---

## Step 5: Audit critical-patterns.md

For each of the 8 patterns:
- **Still accurate?** Does codebase/workflow still follow this?
- **Has verify: annotation?** If not → add one (required)
- **Graduation candidate?** If referenced 0 times in violations/corrections → might be internalized, could prune
- **Redundant?** Now covered by core-invariants.md? → PRUNE from critical-patterns

Show for each:
```
PATTERN: [name]
  Has verify: [yes/no]  Violations: [N]  Corrections: [N]
  Action: KEEP | ADD_VERIFY | PRUNE | UPDATE
```

---

## Step 6: Check Evolution Log

Read `.claude/memory/evolution-log.md` (or decisions.md if no evolution-log).
**Never re-propose a previously rejected change** unless user explicitly asks.

---

## Step 7: Propose Changes

For each proposed change, show:

```
PROPOSE: [action type]
  Target: [file:section or learning filename]
  Change: [exact text to add/remove/update]
  Evidence: [corrections/violations/sessions data behind this]
  Destination: critical-patterns.md | core-invariants.md | learnings/ | DELETE
```

Action types:
- **PROMOTE**: Add correction pattern to critical-patterns.md (with verify: check)
- **GRADUATE**: Move from critical-patterns.md to core-invariants.md (persists through compaction)
- **ADD_VERIFY**: Add verify: annotation to existing pattern that lacks one
- **PRUNE**: Remove pattern that's now redundant or internalized
- **UPDATE**: Modify existing rule based on new evidence
- **CREATE**: New learning file for observed but uncaptured pattern
- **ESCALATE_TO_HOOK**: Pattern violated so often it needs a hook, not just a rule

---

## Step 7b: Artifact Synthesis (Semantic Observability)

Convert discovered patterns and graduated learnings into **executable artifacts** — not just rules.

Reference: Tang "Towards Semantic Observability" (2026) — human signal → durable, scalable artifacts.

### Input sources

1. **Discovered patterns** from `.claude/memory/discovered-patterns.md` (written by `/discover`)
   - Patterns with `verdict: reinforce` or `verdict: suppress`
2. **Graduated learnings** from Step 3b (confidence >= 0.8, uses >= 10)
3. **High-impact learnings** (impact_score >= 0.7, uses >= 5)

If none of these sources have data, skip this step and note "No artifact candidates yet — run /discover first."

### Artifact type classification

For each candidate, classify into an artifact type and propose generation:

| Signal | Artifact Type | Target | Generation |
|--------|--------------|--------|------------|
| Suppressible pattern (desperation loop) | **Warning pattern** | `panic-detector.py` config | Add regex/sequence pattern to hook's detection rules |
| Suppressible pattern (blind editing) | **Circuit breaker** | `critical-patterns.md` | New entry with verify: annotation |
| Reinforceable pattern (informed editing) | **Routing hint** | `/triage` decision logic | Note preferred approach for similar tasks |
| Reinforceable pattern (effective delegation) | **Skill hint** | `best_practice` learning | Write learning with high initial confidence (0.85) |
| Recurring failure (same test, same fix) | **Eval case** | `.claude/evals/` | Generate YAML eval case from the pattern |
| Graduated learning (proven rule) | **Rule** | `rules/` or `critical-patterns.md` | Move from learnings to permanent rule |
| High-impact learning (used 5+, impact 0.7+) | **Quality gate** | `.claude/memory/quality-gates.md` | Auto-milestone for /critic |

### Proposal format

For each artifact, add to Step 7 proposals:

```
PROPOSE: SYNTHESIZE_ARTIFACT
  Source: [discovered pattern / learning filename]
  Artifact type: [warning_pattern | circuit_breaker | routing_hint | skill_hint | eval_case | rule | quality_gate]
  Target file: [exact path where artifact will be written]
  Content: [exact text/config to add]
  Evidence: [frequency, sessions, impact_score, human verdict]
```

### Constraints
- Max 5 artifact proposals per /evolve run (prevent flooding)
- Eval cases go to `.claude/evals/discovered/` subdirectory
- Warning patterns must include the tool sequence signature (for panic-detector matching)
- All artifacts require user approval in Step 8 (same as other proposals)
- Track generated artifacts in `evolution-log.md` under `### Artifacts Generated` section

---

## Step 8: Wait for Approval

Present ALL proposals in a numbered list before making ANY changes.
For each: user says **approve**, **reject**, or **modify [text]**.

Apply ONLY approved changes.

After applying, append to `.claude/memory/evolution-log.md`:
```markdown
## Evolution Run — [DATE]
### Proposals
- [N] approved, [N] rejected

### Applied
- PROMOTE: [description]
- PRUNE: [description]

### Rejected
- [action]: [reason user gave]
```

---

## Anti-Rationalization Defense

| Rationalization | Why Wrong | Do Instead |
|---|---|---|
| "I'll apply the obvious promotions without waiting for user approval" | Evolve modifies the rules that govern ALL future sessions — unapproved changes can silently degrade behavior system-wide | Present every proposal in the numbered Step 7 list and apply ONLY after explicit approval per item |
| "corrections.jsonl doesn't exist so I'll skip Step 2" | Missing signal files mean data wasn't collected yet, not that there are no issues — other signal sources (violations, sessions) may still have evidence | Note the missing file, continue with available signals, and recommend enabling the hook that writes it |
| "This pattern only appeared once so it's not worth promoting" | Single high-severity corrections from user_correction source outweigh many auto-pattern observations | Weigh by source × severity — one user_correction/critical can justify a CREATE action |
| "critical-patterns.md already has 10 entries, so I won't propose new promotions" | The cap means you must propose a PRUNE alongside any PROMOTE — not that new graduates are blocked | Identify the lowest-confidence existing pattern as a PRUNE candidate and propose both changes together |
| "I'll skip the model_gate audit since I don't know the current model" | Stale model-specific workarounds actively mislead — surfacing them for human review is better than leaving them silently wrong | Use ANTHROPIC_MODEL env var or state "model unknown" and flag all model_gate learnings for manual review |

## Constraints

- Never remove security rules (core-invariants items 4+)
- Never weaken the 3-Fix Escalation rule
- Never add rules that contradict CLAUDE.md or core-invariants.md
- critical-patterns.md max 10 entries — if full, graduation or pruning required before adding
- core-invariants.md max 7 entries — same
- Every new rule must have a **verify: annotation** (or "verify: manual" if behavioral)
- Bias toward specificity: "never use X" > "be careful with X"
