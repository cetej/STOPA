---
name: dreams
description: "Use when running offline memory consolidation — cross-linking learnings, backward-updating contexts, surfacing cross-session patterns. Trigger on 'dreams', 'consolidate memory', 'dream cycle'. Do NOT use for numerical maintenance (that's autodream.py) or manual learning capture (/scribe)."
user-invocable: true
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash", "Agent", "TodoWrite"]
permission-tier: workspace-write
phase: meta
tags: [memory, session]
requires: []
max-depth: 1
effort: auto
discovery-keywords: [consolidate, integrate, reflect, cross-link, pattern detection, memory health, offline processing, sleep]
input-contract: "scheduled-task or user → no input required → reads memory state autonomously"
output-contract: "dream log → markdown → .claude/memory/dreams/YYYY-MM-DD.md"
preconditions: [".claude/memory/learnings/ directory exists"]
effects: ["related: fields updated in learnings", "dream log written", "concept-graph.json updated if new connections found"]
---

# Dreams — Offline Memory Consolidation

You are the Dream Consolidator. While the user is away, you review recent memory activity, find hidden connections, and strengthen the knowledge base.

## Philosophy

Research validates this approach:
- Reflexion (91% vs 80% HumanEval) proves reflection is load-bearing
- Generative Agents degenerate in 48h without reflection
- A-MEM's backward-updating makes old memories evolve with new context
- MemMachine shows retrieval quality >> storage sophistication
- OpenClaw's dream cycle: collect → consolidate → evaluate with Smart Skip

## Process

### Phase 0: Smart Skip Check

Before doing anything expensive:

1. Read `.claude/memory/dreams/` — check last dream date
2. Read `.claude/memory/intermediate/autodream-report.json` — last maintenance report
3. Count new learnings since last dream: `Glob("*.md", path=".claude/memory/learnings/")` and check dates
4. Count new outcomes since last dream: `Glob("*.md", path=".claude/memory/outcomes/")`

**Skip conditions** (exit with "Nothing new to consolidate"):
- Last dream was < 3 days ago AND no new learnings AND no new outcomes
- Zero learnings total

If skipping, write a 1-line log: `.claude/memory/dreams/YYYY-MM-DD-skip.md` with reason.

### Phase 1: Collect (read-only scan)

Gather raw material for consolidation:

1. **Recent learnings** (last 14 days): Read all `.claude/memory/learnings/2026-*.md` files from the last 14 days
2. **Recent outcomes** (last 14 days): Read `.claude/memory/outcomes/2026-*.md` if directory exists
3. **Current checkpoint**: Read `.claude/memory/checkpoint.md` — what was the user working on?
4. **Autodream report**: Read `.claude/memory/intermediate/autodream-report.json` — what's stale, what's graduating?
5. **Concept graph**: Read `.claude/memory/concept-graph.json` — existing knowledge connections

Build a mental model: What themes keep appearing? What's connected but not linked?

### Phase 2: Consolidate (the actual dreaming)

#### 2a: Cross-link Discovery

For each recent learning, check:
- Does it share themes/component with other learnings that don't have `related:` connections?
- Would adding `related:` links improve retrieval for common queries?

**Rules:**
- Max 3 `related:` entries per learning (already in memory-files.md rules)
- Only link genuinely related learnings, not just same-component
- Prefer linking across components (cross-cutting insights are most valuable)

#### 2b: Backward-Update (A-MEM inspired)

When a new learning changes context for an older one:
- Update the older learning's body text with a brief note: `> Updated YYYY-MM-DD: <context from new learning>`
- Don't change the original content — append context
- Max 1 backward-update per old learning per dream cycle

#### 2c: Pattern Detection

Look for recurring patterns across learnings and outcomes:
- Same `failure_class` appearing 3+ times → candidate for critical-patterns.md
- Same component failing repeatedly → systemic issue
- Techniques that work across different contexts → candidate for generalization

**Maturity-Aware Generalization:**
- When a pattern appears 3+ times across sessions (different dates in learnings): recommend `maturity: validated` upgrade
- Cross-session patterns carry stronger signal than single-session observations
- Check: grep same `failure_class` or `component` across learnings → count unique dates

#### Phase 2e: Replay Queue Check

Read `.claude/memory/replay-queue.md`:
- Items with status `pending` older than 14 days without matching second failure → flag in dream log as "stale draft — consider manual review or archival"
- Items with status `ready` → note in dream log: "N items ready for replay validation — trigger /evolve or /learn-from-failure"
- Update Smart Skip: if replay queue has `ready` items → do NOT skip dream cycle (consolidation needed)

If file doesn't exist, skip this step silently.

#### 2d: Concept Graph Update

If new connections were found in 2a-2c:
- Read current `concept-graph.json`
- Add new edges for discovered relationships
- Keep graph manageable: max 200 nodes, prune lowest-weight edges if needed

### Phase 3: Evaluate & Report

Write dream log to `.claude/memory/dreams/YYYY-MM-DD.md`:

```markdown
---
date: YYYY-MM-DD
learnings_scanned: N
outcomes_scanned: N
connections_found: N
backward_updates: N
patterns_detected: N
duration_estimate: Nmin
---

# Dream Log — YYYY-MM-DD

## New Connections
- learning-A.md ↔ learning-B.md: <why they're related>
- ...

## Backward Updates
- Updated learning-X.md with context from learning-Y.md: <what changed>
- ...

## Emerging Patterns
- <pattern description>: seen in [learning-1, learning-2, learning-3]
- ...

## Consolidation Health
- Total learnings: N
- Average confidence: N.NN
- Learnings with 0 uses (30+ days old): N
- Graduation candidates: N
- Suggested actions: ...
```

### Phase 4: Smart Skip Optimization

Track token usage:
- If Phase 1 scan shows < 3 new items since last dream → abbreviated cycle (skip Phase 2c-2d)
- If nothing actionable found → log "clean dream" and exit
- Target: < 50K tokens for routine dreams, < 150K for full consolidation

## Anti-Rationalization Defense

| Rationalization | Why Wrong | Do Instead |
|---|---|---|
| "I'll link everything to everything" | Over-linking dilutes retrieval signal | Max 3 related per learning, cross-component preferred |
| "This pattern is obvious, no need to log" | Obvious patterns still need measurement | Log it — if it's real, uses counter will validate |
| "I'll backward-update extensively" | Heavy updates change meaning of old learnings | Append-only context notes, max 1 per learning per cycle |
| "No new learnings, nothing to do" | Cross-linking existing learnings is always valuable | Check existing learnings for missing connections |

## Red Flags

STOP and re-evaluate if any of these occur:
- Linking more than 5 learnings in one cycle (probably over-connecting)
- Backward-updating more than 3 learnings in one cycle (too aggressive)
- Dream log exceeds 100 lines (too verbose, consolidate)
- Spending > 10 minutes on Phase 1 scan (too many files, narrow scope)

## Verification Checklist

- [ ] Smart Skip correctly evaluated (checked dates, counts)
- [ ] All new `related:` links are bidirectional (A→B and B→A)
- [ ] Backward updates are append-only (original content unchanged)
- [ ] Dream log written with accurate counts
- [ ] No fabricated connections (every link has stated reason)

## Rules

- NEVER delete or modify the core content of existing learnings — only add `related:` fields and append context notes
- NEVER create new learnings — that's /scribe's job. Dreams consolidate, not create.
- NEVER skip Smart Skip check — it saves 90% of token budget on idle days
- Dream logs accumulate in `.claude/memory/dreams/` — archive after 30 days
- If concept-graph.json doesn't exist, skip Phase 2d (don't create from scratch here)
- Keep dream logs factual and brief — no speculation about "what the user might want"
