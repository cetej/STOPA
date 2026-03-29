# Claude Subconscious — Research Brief

**Date:** 2026-03-27
**Question:** Full technical architecture of Claude Subconscious — hooks, 8 memory blocks, transcript processing, whispering mechanism, limitations, community reception, maturity
**Scope:** deep
**Sources consulted:** 12 (GitHub repo, README, CHANGELOG, Subconscious.af agent file, issues tracker, releases page, blog post, threads/X social)

---

## Executive Summary

Claude Subconscious (`github.com/letta-ai/claude-subconscious`) is an MIT-licensed Claude Code plugin from Letta, Inc. (the MemGPT company) that attaches a persistent Letta agent as a "background brain" to Claude Code sessions. Released January 2026, it reached ~1.9k stars by late March 2026 and is at v1.5.1 with active development. The core idea: four Claude Code hooks funnel session transcripts to a Letta agent that builds structured memory across sessions, then "whispers" guidance back via stdout injection before each user prompt — never blocking the main Claude Code workflow. The default agent runs on GLM-5 (free tier via z.ai), embeds conversations using OpenAI text-embedding-3-small, and maintains 8 typed memory blocks with per-block token limits. The project is actively maintained but has several open Linux/macOS compatibility bugs (3 as of 2026-03-27). The original CLAUDE.md-write architecture was replaced in v1.3.0 with a cleaner stdout injection model after token bloat issues.

---

## Detailed Findings

### 1. GitHub Repository & Maturity

- **URL:** https://github.com/letta-ai/claude-subconscious
- **Stars:** ~1.9k (as of late March 2026; earlier figure of 862 was from a different snapshot)
- **Forks:** 61
- **License:** MIT (Copyright Letta, Inc. 2026)
- **Release cadence:** v1.0.0 on Jan 16, 2026 → v1.5.1 on Mar 4, 2026 — 8 releases in 7 weeks
- **Organization:** Letta AI (formerly MemGPT / cpacker), San Francisco
- **Author of blog post:** Cameron Pfiffer (works at Letta)
- **Maturity status:** Experimental / alpha — self-described as "experimental extension of Claude Code (closed-source agent)"

### 2. Architecture Overview

Claude Subconscious implements a **dual-agent system**:

```
Claude Code (primary, visible)
    ↕  4 hooks
Letta Agent (background, async)
    ↓
Memory blocks (8 typed blocks, persisted in Letta cloud or self-hosted)
    ↓
Whisper injection (stdout → prepended to user prompts)
```

The Letta agent is **not** running in the same process as Claude Code. It is a separate stateful agent managed by the Letta platform (cloud at `app.letta.com` or self-hosted). Each session gets its own Letta conversation, but the memory blocks are **shared globally** across all projects via a single agent instance at `~/.letta/claude-subconscious/config.json`.

### 3. Hook Integration — All Four Hooks

Claude Code hooks are configured in the plugin manifest. Four hooks are used:

| Hook | Source file | Timeout | What it does |
|------|-------------|---------|--------------|
| `SessionStart` | `session_start.ts` | 5s | Creates/maps a new Letta conversation for this session; cleans legacy CLAUDE.md `<letta>` sections from pre-v1.3.0; notifies agent |
| `UserPromptSubmit` | `sync_letta_memory.ts` | 10s | Fetches pending agent messages + memory blocks; injects into Claude's context via stdout before the user prompt is processed |
| `PreToolUse` | `pretool_sync.ts` | 5s | Delivers mid-workflow updates via `additionalContext` when agent has new messages since last sync; addresses "workflow drift" (added v1.1.0) |
| `Stop` | `send_messages_to_letta.ts` | 120s | **Spawns a detached background worker** (`send_worker_sdk.ts`) and immediately exits — the hook itself never blocks Claude Code; the worker processes the full transcript independently |

The `Stop` hook's async-detach pattern is the key design: it spawns `send_worker_sdk.ts` as a separate OS process (via `spawnSilentWorker`), passes the session transcript via a temp file in `$TMPDIR/letta-claude-sync-$UID/`, and returns immediately. The worker then runs an SDK session with tool access.

**Checkpoint hooks** were added in v1.5.1: transcripts are also sent at decision points (before Claude answers questions), so Letta sees the question before Claude responds.

### 4. The 8 Memory Blocks

Defined in `Subconscious.af` (the bundled agent definition file). Each block has a size limit:

| Block name | Limit | Purpose |
|------------|-------|---------|
| `core_directives` | 5 KB | Role definition and behavioral guidelines for the agent itself |
| `guidance` | 3 KB | Active guidance for next Claude Code session; explicitly cleared when stale |
| `user_preferences` | 3 KB | Learned coding style, tool choices, communication preferences |
| `project_context` | 3 KB | Codebase architecture, key files, architectural decisions |
| `session_patterns` | 3 KB | Recurring behaviors, common struggles, time-based patterns |
| `pending_items` | 3 KB | Unfinished work and explicit TODOs across sessions |
| `self_improvement` | 5 KB | Guidelines for how the agent should evolve its own memory architecture |
| `tool_guidelines` | 5 KB | Instructions for how the agent should use its own tools |

Total memory budget per agent: ~30 KB across all blocks. Memory blocks are readable/writable by the agent itself using specialized memory tools.

### 5. Transcript Processing

The `Stop` hook writes the full session transcript (JSONL format from Claude Code) to a temp file. The background worker reads this file and starts a Letta SDK session. The transcript contains:
- User messages
- Assistant responses including thinking blocks
- Tool usage events and results
- Timestamps

The Letta agent then processes this context with access to **SDK tools** (configurable):
- **read-only** (default): `Read`, `Grep`, `Glob`, `web_search`, `fetch_webpage`
- **full**: All tools including `Bash`, `Edit`, `Write`, `Task` (can spawn sub-agents)
- **off**: Memory-only, no client-side tools

After processing, the agent updates its memory blocks via Letta's memory management tools (str_replace, insert, delete, rethink).

### 6. Whispering — Technical Mechanism

"Whispering" = the `UserPromptSubmit` hook injecting context via **stdout** before Claude processes each user prompt.

How it works exactly:
1. Before each user message is sent to Claude, `sync_letta_memory.ts` fires
2. It queries the Letta agent for pending `guidance` block content and any new agent messages
3. Any content is written to stdout by the hook — Claude Code reads hook stdout and prepends it to the user prompt context
4. Claude Code then processes the combined [whisper content + user message]

**Three modes** (controlled by `LETTA_MODE` env var):
- `whisper` (default): Only agent messages injected
- `full`: Full memory blocks injected on first prompt, then diffs only (to control token cost)
- `off`: All injection disabled

**One-step lag:** The agent always processes transcripts from the *previous* interaction. It cannot respond in real-time to the current message. Guidance is prepared between sessions or between turns.

**Multi-session:** Using Letta's Conversations API, one agent serves multiple Claude Code sessions in parallel, with memory blocks synchronized across all of them.

### 7. Limitations, Issues & Community Feedback

**Architectural limitations:**
- One-step lag: agent is always one turn behind
- Cannot directly modify CLAUDE.md or inject into Claude's system prompt (only user prompt prepend via stdout)
- All memory through one shared agent brain — cross-project contamination risk if memory blocks are not well managed
- Requires Letta account (cloud) or self-hosted Letta server

**Known bugs (open as of 2026-03-27):**
- Issue #42: `spawnSilentWorker` uses `npx tsx` on macOS/Linux — fails to resolve `@letta-ai/letta-code-sdk` (module path resolution bug)
- Issue #41: Unhandled 'error' event on `/dev/tty` WriteStream crashes `session_start` hook
- Issue #34: `UserPromptSubmit` hook fails — `CLAUDE_PLUGIN_ROOT` env var empty on Linux
- Issue #27: Feature request — bidirectional conversation (Claude can't query Subconscious directly)

**Historical issues (resolved):**
- CLAUDE.md token bloat: pre-v1.3.0 architecture wrote memory blocks to `.claude/CLAUDE.md`, which grew to 49K+ characters causing token bloat and cross-project contamination. Fixed in v1.3.0 by switching entirely to stdout injection
- Multi-user `/tmp` collision: hardcoded `/tmp/letta-claude-sync/` caused EACCES errors when multiple OS users shared a machine. Fixed by making path user-specific: `$TMPDIR/letta-claude-sync-$UID/`
- Windows console flashing: background worker spawning caused visible console windows on Windows. Fixed in v1.3.2

**Community tone:** Positive reception on launch (social media sharing, 1.9k stars in ~2 months). The 3 open Linux/macOS issues suggest the project is primarily developed and tested on macOS but Linux support is incomplete. No Hacker News thread found.

### 8. Model Configuration (Default Agent)

The bundled `Subconscious.af` agent uses:
- **LLM:** GLM-5 via z.ai (`https://api.z.ai/api/paas/v4/`) — free tier available
- **Context window:** 90,000 tokens
- **Temperature:** 0.7
- **Parallel tool calls:** disabled
- **Embeddings:** `text-embedding-3-small` (OpenAI), 1536 dimensions, 300-token chunks (for conversation_search)

Users can override via `LETTA_MODEL` env var or by substituting their own agent via `LETTA_AGENT_ID`.

Model auto-selection fallback order:
1. claude-sonnet-4-5
2. gpt-4.1-mini
3. claude-haiku-4-5
4. gpt-5.2
5. gemini-3-flash
6. gemini-2.5-flash
7. First available model

---

## Disagreements & Open Questions

- **Star count discrepancy:** One search returned 862 stars, another 1.9k. The 1.9k figure appears more recent (repo front page vs indexed snapshot). Status: unresolved (inferred from multiple sources).
- **Bidirectional communication:** Currently one-way — Subconscious whispers to Claude but Claude cannot query Subconscious. Issue #27 is open as a feature request.
- **Actual memory effectiveness:** No independent evaluation of whether the 8-block memory architecture actually improves Claude Code behavior over time. The "Evaluate usefulness" issue (#10) is still open from January 2026.

---

## Evidence Table

| # | Source | URL | Key Claim | Type | Confidence |
|---|--------|-----|-----------|------|------------|
| 1 | GitHub repo (letta-ai) | https://github.com/letta-ai/claude-subconscious | 1.9k stars, MIT license, active | primary | high |
| 2 | README.md | https://github.com/letta-ai/claude-subconscious/blob/main/README.md | 4 hooks, 8 memory blocks, 3 modes, config vars | primary | high |
| 3 | Subconscious.af | https://github.com/letta-ai/claude-subconscious/blob/main/Subconscious.af | Memory block names/limits, GLM-5 model, 7 tools | primary | high |
| 4 | CHANGELOG.md | https://github.com/letta-ai/claude-subconscious/blob/main/CHANGELOG.md | v1.0 (Jan 16) → v1.5.1 (Mar 4), 8 releases | primary | high |
| 5 | Releases page | https://github.com/letta-ai/claude-subconscious/releases | v1.5.1 Mar 4 is latest, checkpoint hooks added | primary | high |
| 6 | Issues tracker | https://github.com/letta-ai/claude-subconscious/issues | 6 open issues, 3 Linux/macOS compat bugs | primary | high |
| 7 | Cameron Pfiffer blog | https://cameron.stream/blog/claude-subconscious/ | Whispering mechanism, one-step lag, author context | primary | high |
| 8 | LICENSE file | https://github.com/letta-ai/claude-subconscious/blob/main/LICENSE | MIT, Letta Inc. 2026 | primary | high |
| 9 | Threads post (Cameron) | https://www.threads.com/@cameron_pfiffer/post/DT_amoFjlkd/ | Sidecar architecture, CLAUDE.md injection (pre-v1.3.0) | primary | medium |
| 10 | Web search aggregation | multiple | Token bloat history, CLAUDE.md 49K+ char issue, fix in v1.3.0 | inferred from multiple sources | high |

---

## Sources

1. GitHub — letta-ai/claude-subconscious — https://github.com/letta-ai/claude-subconscious
2. README.md — https://github.com/letta-ai/claude-subconscious/blob/main/README.md
3. Subconscious.af agent definition — https://github.com/letta-ai/claude-subconscious/blob/main/Subconscious.af
4. CHANGELOG.md — https://github.com/letta-ai/claude-subconscious/blob/main/CHANGELOG.md
5. Releases — https://github.com/letta-ai/claude-subconscious/releases
6. Issues tracker — https://github.com/letta-ai/claude-subconscious/issues
7. Cameron Pfiffer blog post — https://cameron.stream/blog/claude-subconscious/
8. LICENSE — https://github.com/letta-ai/claude-subconscious/blob/main/LICENSE
9. Threads post by Cameron — https://www.threads.com/@cameron_pfiffer/post/DT_amoFjlkd/

---

## Coverage Status

- **Directly verified (read source):** All 4 hooks and their source files, all 8 memory blocks with exact names and limits from Subconscious.af, whispering mechanism, 3 LETTA_MODE options, SDK tools config, all releases v1.0→v1.5.1, all 6 open issues, MIT license, GLM-5 model config, token bloat history
- **Inferred (multi-source):** Star count (~1.9k), contributor count (not explicitly stated), effectiveness of memory system in practice
- **Unresolved:** No Hacker News or Reddit thread found; no independent benchmarks of memory quality; exact number of contributors unknown
