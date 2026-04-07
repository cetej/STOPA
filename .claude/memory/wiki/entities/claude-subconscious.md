---
name: Claude Subconscious
type: tool
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [claude-subconscious-research]
tags: [memory, session, hooks, dual-agent, claude-code]
---
# Claude Subconscious

> MIT-licensed Claude Code plugin from Letta AI that attaches a persistent Letta agent as a background brain, maintaining 8 typed memory blocks (~30 KB) and injecting guidance via stdout before each user prompt.

## Key Facts

- 4 hooks: SessionStart (5s), UserPromptSubmit (10s), PreToolUse (5s), Stop (120s async-detach) (ref: sources/claude-subconscious-research.md)
- 8 memory blocks: core_directives (5KB), guidance (3KB), user_preferences (3KB), project_context (3KB), session_patterns (3KB), pending_items (3KB), self_improvement (5KB), tool_guidelines (5KB) — total ~30 KB (ref: sources/claude-subconscious-research.md)
- v1.3.0 replaced CLAUDE.md write-back (caused 49K+ char bloat) with stdout injection (ref: sources/claude-subconscious-research.md)
- One-step lag: agent processes previous interaction's transcript, cannot respond in real-time (ref: sources/claude-subconscious-research.md)
- Default model: GLM-5 via z.ai (free tier); embeddings: text-embedding-3-small (ref: sources/claude-subconscious-research.md)
- 3 open Linux/macOS compatibility bugs as of 2026-03-27 (ref: sources/claude-subconscious-research.md)
- ~1.9k GitHub stars; MIT license; github.com/letta-ai/claude-subconscious (ref: sources/claude-subconscious-research.md)

## Relevance to STOPA

Architecture reference for STOPA's own memory system. Key lessons: (1) stdout injection > CLAUDE.md for context delivery to avoid token bloat; (2) async-detach Stop hook pattern prevents blocking; (3) global single-agent memory causes cross-project contamination — STOPA's per-project memory design avoids this.

## Mentioned In

- [Claude Subconscious — Technical Architecture Deep Dive](../sources/claude-subconscious-research.md)
