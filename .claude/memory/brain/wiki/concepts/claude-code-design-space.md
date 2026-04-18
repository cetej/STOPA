---
title: Claude Code Design Space — Architecture Analysis
category: concepts
tags: [claude-code, architecture, agent-design, context-management, permissions, hooks, subagents]
sources: [arXiv:2604.14228 — Liu et al., VILA Lab / UCL]
updated: 2026-04-18
---

# Claude Code Design Space — Architecture Analysis

**Paper**: arXiv:2604.14228  
**Authors**: Jiacheng Liu et al. (VILA Lab, MBZUAI + UCL)  
**Code**: github.com/VILA-Lab/Dive-into-Claude-Code

## Core Finding

**1.6% decision logic / 98.4% operational infrastructure.** CC's architecture is NOT a reasoning engine with safety bolted on — it is a safety+context+extensibility harness with a thin reasoning layer inside. The `queryLoop()` is the core; the 98.4% surrounds it.

## Five Motivating Values (derived)

Human Decision Authority → Safety → Reliable Execution → Capability Amplification → Contextual Adaptability

## Five-Layer Context Compaction Pipeline

| Layer | Name | Trigger | Method |
|-------|------|---------|--------|
| 1 | Budget Reduction | Always | Per-message size limits → content references |
| 2 | Snip | Token pressure | Remove older history segments |
| 3 | Microcompact | Moderate pressure | Cache-aware fine-grained compression |
| 4 | Context Collapse | High pressure | Read-time projection (non-destructive) |
| 5 | Auto-Compact | Threshold exceeded | Model-generated summary |

**Principle**: Apply lightest reduction first, heaviest last. No single strategy addresses all pressure types.

## Seven Permission Modes (graduated autonomy)

`plan` → `default` → `acceptEdits` → `auto` (ML classifier) → `dontAsk` → `bypassPermissions` → `bubble` (internal subagent escalation)

Permission modes are session-scoped, not restored on resume — deliberate safety choice.

## 27 Hook Event Types

Covers 6 categories: Tool authorization (PreToolUse, PostToolUse, PermissionRequest, PermissionDenied), Session lifecycle (SessionStart, SessionEnd, Setup, Stop), User interaction (UserPromptSubmit, Elicitation), **Subagent coordination (SubagentStart, SubagentStop, TaskCreated)**, **Context management (PreCompact, PostCompact)**, Workspace events (CwdChanged, FileChanged).

STOPA uses 12 (verified against settings.json): SessionStart, PreToolUse, PostToolUse, PermissionRequest, PreCompact, PostCompact, Stop, TaskCompleted, TeammateIdle, StopFailure, UserPromptSubmit, TaskCreated. **Genuinely missing**: PermissionDenied, SessionEnd, Setup, Elicitation, SubagentStart, SubagentStop, CwdChanged, FileChanged.

## Sidechain Transcript Design

Each subagent writes its own `.jsonl` file. **Only final response text returns to parent.** Full history never inflates parent context window. Audit trail preserved without context explosion. This is the CC implementation of artifacts-as-memory at agent-boundary level.

## CLAUDE.md Four-Level Hierarchy

OS-level → User (~/.claude) → Project (checked-in) → Local (git-ignored). Closer to CWD = higher priority. Lazy loading for nested rules. `@include` for modular composition. **File-based transparency over embedding-based retrieval** — everything auditable, versionable, deletable.

## Comparison: CC vs OpenClaw

| Dimension | Claude Code | OpenClaw |
|-----------|-------------|----------|
| Trust model | Deny-first per-action, 7 modes, ML | Single trusted operator, DM pairing |
| Extension | 4 mechanisms (MCP, plugins, skills, hooks) | 12-capability manifest |
| Memory | CLAUDE.md 4-level + 5-layer compaction | 8 workspace files, vector+keyword hybrid |
| Multi-agent | Task-delegating subagents, worktree isolation | Routing + delegation, nesting ≤5 |

**Insight**: Identical design questions → different answers based on deployment context.

## Long-Term Capability Paradox

AI-assisted developers score **17% lower on comprehension tests** (external research). CC optimizes for short-term amplification (27% tasks wouldn't be attempted otherwise) but this concern is NOT prominently reflected in architectural decisions. Potential tension: amplification vs. atrophy.

## STOPA Relevance

Direct architectural parent. STOPA extends CC's hook system (behavioral-genome, calm-steering, panic-detector), CLAUDE.md hierarchy (rules/*.md + behavioral-genome.md), and subagent delegation pattern. This paper provides the first systematic naming of CC's architectural layers — useful for reasoning about which CC mechanisms STOPA leverages vs. gaps that remain unexploited (PreCompact hooks, SubagentStart/Stop).

## Related Concepts

→ [context-engineering.md](context-engineering.md)  
→ [multi-agent-orchestration-protocols.md](multi-agent-orchestration-protocols.md)  
→ [prompt-injection-defense.md](prompt-injection-defense.md)  
→ [artifacts-as-memory.md](artifacts-as-memory.md)  
→ [tool-use-evolution.md](tool-use-evolution.md)
