---
title: "Claw Code — Architektonická analýza pro STOPA"
slug: claw-code-architecture
source_type: research_output
date_ingested: 2026-04-07
entities_extracted: 9
claims_extracted: 5
---

# Claw Code — Architektonická analýza pro STOPA

> **TL;DR**: Claw Code je referenční implementace Claude Code s 3-tier permission systémem (ReadOnly/WorkspaceWrite/DangerFullAccess), 6 MCP transporty a multi-agent orchestrací přes QueryEngine. Klíčový insight: COORDINATOR_MODE omezuje koordinátora pouze na [Agent, SendMessage, TaskStop] — nutí delegaci místo přímé práce. STOPA by mělo adoptovat stejný vzor pro /orchestrate skill.

## Key Claims

1. COORDINATOR_MODE má přístup pouze k [Agent, SendMessage, TaskStop] — koordinátor nemůže číst/psát soubory — `[verified]`
2. BashTool má 8vrstvý security stack (~2500 řádků bashSecurity.ts) s 2-stage TRANSCRIPT_CLASSIFIER (Stage 1: 8.5% FPR, Stage 2: 0.4% FPR) — `[verified]`
3. Agent Teams (Opus 4.6 only) podporují 3 spawn módy: Fork (byte-identická kopie), Teammate (tmux/file-based mailbox), Worktree (izolovaný git branch) — `[verified]`
4. MCP 11-phase lifecycle state machine s degraded mode — systém pokračuje s částečnou dostupností — `[verified]`
5. 5 built-in agent typů: generalPurpose, explore (Haiku, read-only), plan (read-only), verification (all tools), guide (read-only) — `[verified]`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| Claw Code | tool | new |
| COORDINATOR_MODE | concept | new |
| QueryEnginePort | concept | new |
| ToolPermissionContext | concept | new |
| MCP 11-phase lifecycle | concept | new |
| TRANSCRIPT_CLASSIFIER | concept | new |
| Agent Teams | concept | new |
| PortRuntime | concept | new |
| FNV-1a config hashing | concept | new |

## Relations

- Claw Code `implements` COORDINATOR_MODE
- COORDINATOR_MODE `restricts` QueryEnginePort
- ToolPermissionContext `uses` deny_names/deny_prefixes
- TRANSCRIPT_CLASSIFIER `strips` assistant messages (reasoning-blind design)
- Agent Teams `requires` Opus 4.6
