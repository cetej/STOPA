---
date: 2026-04-27
type: anti_pattern
severity: medium
component: workflow
tags: [verification, external-research, claude-code, content-marketing]
summary: External blog posts about Claude Code mix real APIs with fabricated ones (e.g., CLAUDE_CODE_FORK_SUBAGENT env var, /fork slash command, "Plan" built-in subagent — all claimed but don't exist). Verify named env vars/flags/commands against docs.anthropic.com via claude-code-guide subagent BEFORE designing tests or implementations.
source: external_research
uses: 0
successful_uses: 0
harmful_uses: 0
confidence: 0.6
maturity: draft
verify_check: manual
failure_class: assumption
---

## Thought

Article (aitmpl.com / "Keep your Claude Code context clean with Subagents") claimed `CLAUDE_CODE_FORK_SUBAGENT=1` env var lets sub-agents inherit parent context with shared prompt cache prefix (~10× cheaper input tokens for children 2-N). User asked: "test before adopting." Plausible-sounding name following CLAUDE_CODE_* convention — easy to believe.

## Action

Spawned `claude-code-guide` subagent with explicit verification prompt: check official Anthropic docs (docs.anthropic.com/en/docs/claude-code/) for the env var, the `/fork` slash command, and the built-in `Plan` subagent. Required either docs URL or explicit "not documented." Parallel `Explore` subagent reviewed STOPA's existing context-passing infrastructure for comparison.

## Result

- `CLAUDE_CODE_FORK_SUBAGENT`: NOT in docs, fabricated.
- `/fork` slash command: doesn't exist; only CLI flag `--fork-session` (forks session ID to branch a conversation, NOT sub-agent context).
- `Plan` built-in subagent: not documented; only `Explore` is real.
- Anthropic docs explicit: "Each subagent runs in its own context window... completely separate from your main conversation." Context isolation is intentional design, not a bug to fix.

The article mixed `--fork-session` (real, different purpose) with invented features. STOPA already has a finer-grained alternative: Latent Briefing pattern in `.claude/skills/orchestrate/references/agent-execution.md:42-79` (operator-scoped context per agent, not full inheritance).

## Pattern

Before testing OR implementing any externally-claimed Claude Code feature:

1. Spawn `claude-code-guide` subagent with the specific named claim (env var, flag, command, subagent name).
2. Require either an official docs URL OR explicit "not documented in official sources."
3. If verification fails → reject claim, write learning, do not waste cycles designing a test against a non-existent feature.

Cost asymmetry: one verification spawn (~90K tokens, ~17s) is much cheaper than scaffolding a benchmark for an env var that does nothing.

## Why

Content marketing about CC uses plausible naming conventions (`CLAUDE_CODE_*` prefix mimics real env vars like `CLAUDE_CODE_USE_BEDROCK`, `CLAUDE_CODE_MAX_OUTPUT_TOKENS`). Hard to distinguish real from invented from prose alone. Authors mix one real feature (`--fork-session`) with adjacent fabrication ("therefore subagents also fork"). Pattern matches /radar evaluation findings: 30%+ of Twitter/blog tool claims about CC don't survive doc verification.

Applies to: `/radar` (tool evaluation), `/ingest` (raw source processing), `/deepresearch` (citation verification), `/improve` (cross-project tip routing). Any skill that consumes external claims about CC mechanics should run this check before propagating findings.
