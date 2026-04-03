# ADR 0012: Associative Memory Upgrade (Hippocampus Integration)

- **Date**: 2026-04-03
- **Status**: IMPLEMENTING (Phase 3a/3b/3e done, 3c/3d remaining)
- **Source**: claude_hippocampus (allthingssecurity/claude_hippocampus)

## Context

STOPA memory system uses flat markdown files with grep-first retrieval. Analysis revealed:
- `uses: 0` for all 52 learnings — system never tracks what gets applied
- No co-occurrence tracking — learnings are isolated islands
- No automatic context injection — requires manual Phase 0 in orchestrate
- No feedback loops — critic findings don't feed back to learnings

Hippocampus project demonstrated 29% faster tasks, 13% fewer tokens via spreading activation on Neo4j graph.

## Decision

Adopt hippocampus patterns in 3 phases, adapted to zero-dependency file-based architecture:

1. **Phase 1** (2-3 days): Fix dead counters — learning tracker hook, critic feedback, lifecycle automation
2. **Phase 2** (1-2 weeks): Add associative recall — concept-graph.json, spreading activation, UserPromptSubmit auto-injection
3. **Phase 3** (4-6 weeks): Self-improving memory — Hebbian learning, auto-skill crystallization, cross-project transfer

## Key Design Choices

- **No Neo4j**: Use JSON file + in-memory spreading activation (~50-100ms vs 200-600ms)
- **No LLM for extraction**: Regex-based concept extraction (same as hippocampus)
- **Preserve grep-first**: Associative layer supplements, doesn't replace existing retrieval
- **Hook-based injection**: UserPromptSubmit hook = every prompt gets relevant context automatically

## Consequences

- (+) Learnings become self-promoting/retiring based on actual usage
- (+) Cross-session context transfer without manual checkpoint
- (+) Auto-discovery of skill patterns across projects
- (-) New JSON file to maintain (concept-graph.json)
- (-) Hook latency budget: must stay under 3s for activation
