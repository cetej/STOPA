# Orchestration System for AI Coding Agents

This is an **idea file** in the sense of Karpathy (2026-04-04): a pattern description,
not runnable code. Give it to your LLM agent and let it build the implementation
customized to your project.

---

## The Problem

AI coding agents (Claude Code, Codex, Cursor, etc.) are stateless between sessions.
Every new session starts from zero — no memory of what worked, what failed, what was decided.
Teams of sub-agents lose coordination when context windows compress.
There is no compilation layer turning daily agent work into structured knowledge.

## The Pattern: Shared Memory + Compound Loop

### Architecture

```
Your Project/
  .claude/ (or .agents/ or equivalent)
    commands/          # Skills: markdown files telling the agent HOW to do things
    memory/
      state.md         # Current task (what am I doing right now?)
      learnings/       # Atomic discoveries (YAML frontmatter + markdown)
      wiki/            # Compiled knowledge (synthesized from learnings)
      raw/             # Unprocessed session captures (append-only)
      checkpoint.md    # Session resume point
      budget.md        # Cost tracking
      decisions.md     # Decision log
      news.md          # External ecosystem signals
    hooks/             # Automation scripts triggered by agent events
    settings.json      # Hook registration
```

### The Compound Loop

Every session follows: **PLAN -> WORK -> ASSESS -> COMPOUND**

1. **PLAN**: Agent reads memory (checkpoint, learnings, wiki). Plans work.
2. **WORK**: Agent executes. Sub-agents work in parallel. Shared state coordinates.
3. **ASSESS**: Verify results. Prove it works — exit code is not enough.
4. **COMPOUND**: Capture what was learned. Write to learnings/. Update wiki.

The key insight: **step 4 happens DURING work, not after**. If you wait until session end,
context is gone and learnings are lost.

### Knowledge Lifecycle (3 phases)

```
Phase 1: INGEST (fast, per-event)
  Hook captures session data → raw/*.md (immutable, timestamped)
  User corrections → corrections.jsonl
  Agent discoveries → learnings/*.md (YAML frontmatter)

Phase 2: CONSOLIDATE (periodic, batch)
  /compile reads all learnings → clusters by component → generates wiki articles
  Quality gate: independent reviewer validates each article
  Contradictions and gaps explicitly tracked

Phase 3: REFLECT (rare, strategic)
  /evolve analyzes accumulated corrections and patterns
  Graduates high-confidence learnings to always-loaded rules
  Prunes low-confidence knowledge
  Connects external signals (ecosystem news) to internal strategy
```

### Budget Tiers

Not every task needs the same resources:

| Tier | Sub-agents | Critic passes | When |
|------|-----------|---------------|------|
| light | 0-1 | 1 at end | Simple fix |
| standard | 2-4 | 2 | Multi-file change |
| deep | 5-8 | 3 | Cross-cutting change |

Start with the lowest viable tier. Upgrade only when complexity demands it.

### Circuit Breakers

Agents in loops can burn infinite tokens. Hard stops:
- 3 failed attempts on same subtask -> STOP, escalate to human
- Infrastructure errors (file not found, permission denied) -> immediate STOP, don't retry
- Budget exceeded -> synthesize what you have, note truncation
- Nesting depth > 2 -> STOP

### Skills as Markdown

Skills are `.md` files with YAML frontmatter. They tell the agent what to do in specific
situations. The agent reads them when triggered, not at startup (progressive disclosure).

Key principle: `description` field contains ONLY trigger conditions ("Use when...").
Never summarize the workflow in the description — the agent will shortcut it.

Skills are the "idea files" of your orchestration: they encode patterns, not code.

### Verification Culture

Never say "done" without proof from tool output:
- After code edit: run tests, show output
- After pipeline: check output size and content, not just exit code
- After agent work: grep for expected changes

## What This Enables

- **Session continuity**: New session reads checkpoint, picks up where you left off
- **Knowledge compounding**: 60 days of learnings synthesized into navigable wiki
- **Team coordination**: Sub-agents share state through markdown, not API calls
- **Error prevention**: Corrections from past sessions prevent repeated mistakes
- **Cost awareness**: Budget tracking prevents runaway agent costs

## What This Does NOT Include

- No vector database or embeddings — plain Markdown files, grep-based retrieval
- No persistent daemon — everything runs within agent sessions + lightweight hooks
- No specific LLM provider dependency — works with any agent that reads markdown
- No complex infrastructure — just files in a directory

## Customization Points

Your agent should adapt these to your project:
- **Component taxonomy**: what categories of learnings make sense for your codebase?
- **Hook triggers**: which agent events should capture data?
- **Skill set**: which workflows does your team repeat?
- **Budget calibration**: what's "light" vs "deep" for your token budget?
- **Compilation frequency**: weekly? After every N sessions?

---

*This idea file describes the orchestration pattern used by STOPA (github.com/cetej/STOPA).
The implementation details — specific hooks, skill definitions, memory schemas — are
intentionally omitted. Your agent will figure out what works for your setup.*
