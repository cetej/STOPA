---
date: 2026-05-01
source: AHE Pattern 2 follow-up (outputs/ahe-pilot-2026-04-30.md)
status: research-only — no implementation chip
verdict: hooks suffice for STOPA's current needs; middleware deferred
estimated_time: 1.5h
---

# Middleware vs Hooks — STOPA Capability Gap Analysis

## TL;DR

**STOPA does not need a middleware layer at this time.** Existing hook infrastructure (109 hooks across 6 event types) covers the use cases AHE solves with middleware, with one narrow exception: **runtime LLM call interception** (e.g., context compaction at the moment of model invocation). That gap is real but low-frequency in STOPA's current workload, and the proposed Anthropic SDK has no public API for `wrap_model_call` anyway. **Recommendation:** track this as a future capability, do not implement.

## Source

[outputs/ahe-pilot-2026-04-30.md](ahe-pilot-2026-04-30.md) Pattern 2:
> "STOPA gap: middleware vrstva (intercepts/transforms execution layer). STOPA hooks fire na PreToolUse/PostToolUse, ale **wrap_model_call** (intercept LLM calls) chybí."

AHE evolve_prompt.md L86-95 enumerates 8 component types of an agent system, including **Middleware** as a distinct layer between tools and the model.

## What is AHE middleware?

In AHE's architecture:
- **Middleware** = Python wrappers that intercept and transform either tool calls OR model calls during runtime
- Mounted via `wrap_tool_call` (intercepts ToolUse before/after) or `wrap_model_call` (intercepts model.invoke before/after)
- Common middleware patterns:
  - **Context compactor**: when prompt approaches token limit, summarize older history
  - **Tool result transformer**: post-process tool output (e.g., truncate large file reads, redact secrets)
  - **Retry with backoff**: catch tool errors, retry with exponential backoff
  - **Telemetry**: log every tool/model call to external system
  - **Cost gate**: refuse model invocations if budget exceeded

In AHE's evolve loop, middleware is one of the 8 component levels the executor can modify between iterations.

## What does STOPA have?

STOPA has 109 hooks across 6 event types in `.claude/hooks/`:

| Event | Fires when | STOPA usage examples |
|-------|-----------|---------------------|
| **PreToolUse** | Before tool call | `bash-safety.sh`, `tool-gate.py`, `drift-pr-guard.py` |
| **PostToolUse** | After tool call | `learning-admission.py`, `panic-detector.py`, `stagnation-detector.py` |
| **UserPromptSubmit** | User sends a message | `associative-recall.py`, `auto-checkpoint-suggest.py` |
| **SessionStart** | Session opens | `verify-sweep.py`, `improvement-funnel.py`, `memory-brief` |
| **PreCompact** | Before context compaction | (1 hook — preserves critical state) |
| **Stop** | Agent finishes | `auto-scribe.py`, `evolve-trigger`, `improvement-notify` |

Architecture: hooks are **shell scripts or Python files** invoked by Claude Code's harness at the named event. They can:
- Read tool inputs/outputs (via stdin JSON)
- Block tool execution (return non-zero exit code)
- Inject messages into the model's context (PreToolUse / UserPromptSubmit)
- Write to memory files (PostToolUse / Stop)
- Modify tool inputs before they execute (PreToolUse — limited support)

## Coverage comparison

For each AHE middleware pattern, can STOPA achieve the same with hooks?

| AHE pattern | STOPA hook equivalent | Coverage |
|-------------|----------------------|----------|
| **Context compactor** | PreCompact event + manual `/compact` skill | **Partial.** PreCompact fires only on Claude Code's threshold; AHE compacts mid-prompt. STOPA's `/compact` is user-invoked. |
| **Tool result transformer** | PostToolUse hooks (e.g., `panic-detector.py` reads tool output) | **Yes** — hook can inspect output but cannot rewrite the tool result the model sees (no `replace_output` API). |
| **Retry with backoff** | PreToolUse + custom skill logic | **Partial** — hooks block but don't auto-retry. Skills handle retry themselves (`/orchestrate` 3-fix escalation, transient/logic classification). |
| **Telemetry** | Multiple hooks log to JSON/JSONL files | **Yes** — `advisor-log.jsonl`, `learning lifecycle`, `outcome-credit.py` all fire on hook events. |
| **Cost gate** | PreToolUse with budget check | **Yes** — `acceptance-gate.py` and budget tracking via `state.md`/`budget.md`. |

**Coverage summary:** 3/5 fully covered, 2/5 partial. The partial cases are **context compaction at runtime** and **transparent tool-result rewriting** — neither needed often in STOPA workflows.

## Where the gap is real

### 1. `wrap_model_call` (intercept LLM calls mid-prompt)

STOPA cannot:
- Compress conversation history JUST before sending to the model
- Inject system-prompt tweaks based on runtime conditions (e.g., "you are now in conservative mode because budget is low")
- A/B test different system prompts in production

The Anthropic SDK does not expose a public `wrap_model_call` API for the model.invoke step inside Claude Code. The PreCompact event is the closest analog and fires only at compaction boundaries.

**STOPA workload analysis:** Most STOPA tasks complete in 5-50 turns, well below context limits. When context approaches threshold, `/compact` skill is invoked manually or `PreCompact` hook fires. Mid-prompt compression has not surfaced as a need in any session captured in `outcomes/` (13 records over 30 days, all complete without compaction issues).

### 2. Tool result rewriting (transparent to model)

STOPA hooks can READ tool output and inject SEPARATE messages, but cannot REPLACE the tool output the model sees. AHE middleware can substitute output entirely (e.g., truncate a 50K-line file read to a 200-line summary before the model processes it).

**STOPA workload analysis:** Skills handle this themselves — e.g., `/scout` agent reads files and returns summaries, raw file content is not passed to the orchestrator. The transformation happens at the SKILL level, not the runtime level. This shifts complexity to skills but works.

## Decision

**Hooks suffice. Do not add middleware.**

Rationale:
1. **Anthropic SDK constraint:** `wrap_model_call` is not exposed as a public extension point. Adding "middleware" to STOPA without SDK support means custom HTTP proxying or fork-and-rebuild — disproportionate effort for the gain.
2. **Empirical workload:** No outcome record in the last 30 days shows mid-prompt compression as a blocker. The two partial-coverage cases are hypothetical, not active pain points.
3. **STOPA architecture preference:** complexity at the skill level (where it's reviewable, testable, versionable) beats complexity at the runtime level (which is harder to debug and reason about).
4. **AHE's middleware exists because their harness is custom-built:** AHE controls the entire agent loop; STOPA runs inside Claude Code's harness which has its own boundaries. The architectural levers are different.

## Future capability (track, don't build)

If/when one of these signals fires, revisit:
- 3+ outcome records show "context overflow" or "compaction-related failure" within a 30-day window
- Anthropic SDK adds public `wrap_model_call` or equivalent (e.g., custom callbacks in agent SDK)
- A specific use case emerges that fundamentally cannot be solved at the skill or hook level (e.g., stripping PII from all tool results system-wide before model sees them)

Until then, the gap stays documented but unfilled.

## What this PR does

This is a **research-only chip**. It produces:
1. This document (`outputs/middleware-vs-hooks-research-2026-05-01.md`) for future reference
2. No code changes
3. No skill changes
4. No new hooks

Closes the AHE pilot Pattern 2 (P3 priority) with an explicit decision rather than open question.

## References

- AHE pilot report: [outputs/ahe-pilot-2026-04-30.md](ahe-pilot-2026-04-30.md) Pattern 2
- AHE evolve_prompt.md L86-95 (8-component taxonomy)
- STOPA hooks: `.claude/hooks/` (109 files), `.claude/settings.json` event configuration
- STOPA `/compact` skill: `.claude/skills/compact/SKILL.md` (manual compaction)

---
_Research complete. No follow-up implementation planned. Revisit only if signals listed above fire._
