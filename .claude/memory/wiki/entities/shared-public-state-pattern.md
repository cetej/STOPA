---
name: Shared Public State Pattern
type: concept
first_seen: 2026-04-08
last_updated: 2026-04-08
sources: [coral-autonomous-multi-agent-evolution]
tags: [multi-agent, state-sharing, orchestration, coordination]
---

# Shared Public State Pattern

> A coordination pattern where isolated agents share knowledge via a single public directory (`.coral/public/`) accessed through symlinks, avoiding explicit sync protocols entirely.

## Key Facts

- Each agent has private workspace (git worktree branch) + read/write access to shared `.coral/public/` via symlink (ref: sources/coral-autonomous-multi-agent-evolution.md)
- Shared artifacts: attempts, notes, skills — visible to all agents simultaneously without message passing (ref: sources/coral-autonomous-multi-agent-evolution.md)
- Zero sync overhead: symlinks mean reads are filesystem-level, not network/IPC (ref: sources/coral-autonomous-multi-agent-evolution.md)
- Agents can publish partial results to public state without blocking their local iteration loop (ref: sources/coral-autonomous-multi-agent-evolution.md)
- Knowledge reuse via shared state is the primary driver of CORAL's 3-10× gains over isolated evolution (ref: sources/coral-autonomous-multi-agent-evolution.md)

## Relevance to STOPA

STOPA's multi-agent orchestration currently passes state through checkpoint.md and state.md (sequential reads); shared public state via symlink would enable true async parallel agents — directly applicable to farm-tier orchestration.

## Mentioned In

- [CORAL: Autonomous Multi-Agent Evolution for Open-Ended Discovery](../sources/coral-autonomous-multi-agent-evolution.md)
