---
date: 2026-04-05
type: architecture
severity: medium
component: orchestration
tags: [agent-os, sandbox, audit-trail, scheduling, rust, architecture-reference]
summary: "OpenFang (Rust Agent OS) nabízí 3 architektonické vzory pro STOPA: sandbox izolaci skills, Merkle audit trail pro OSINT výstupy, a daemon-based scheduling bez session. Žádný není urgentní, ale všechny řeší reálné limity."
source: external_research
uses: 0
harmful_uses: 0
confidence: 0.6
verify_check: manual
successful_uses: 0
---

# OpenFang Architecture Patterns pro STOPA

Zdroj: [OpenFang](https://github.com/RightNow-AI/openfang) — Rust Agent OS, v0.3.30, MIT.

## 3 přenositelné vzory

### 1. Sandbox izolace pro skills
- **OpenFang:** WASM dual-metered sandbox (CPU + memory limity per Hand)
- **STOPA gap:** Skills běží v Claude Code kontextu bez izolace, špatný Bash v sub-agentu může shodit session
- **Realistická cesta:** Per-skill runtime budget přes `tool-gate.py` hook — max N Bash calls, max M sekund. Rozšíření existujícího `constrained-tools` o runtime metering
- **Priorita:** Nízká — aktuální circuit breakers stačí pro běžný provoz

### 2. Audit trail s integritou (Merkle hash-chain)
- **OpenFang:** Každý log záznam referencuje hash předchozího → append-only, tamper-evident
- **STOPA gap:** `decisions.md` a `learnings/` jsou plain markdown — agent je může přepsat retroaktivně
- **Realistická cesta:** Append-only JSONL s hash chainem pro MONITOR/ZACHVEV OSINT výstupy kde evidence integrity matters
- **Priorita:** Střední — relevantní až MONITOR/ZACHVEV začnou produkovat OSINT výstupy

### 3. Autonomous scheduling bez session
- **OpenFang:** Agenti operují na schedules nezávisle na uživatelské session
- **STOPA gap:** `scheduled-tasks` MCP vyžaduje běžící Claude Code session
- **Realistická cesta:** Lightweight Python daemon (systemd/Task Scheduler) triggerující CC headless přes `claude-code-sdk-python` na cron
- **Priorita:** Vysoká — SDK už v radaru jako 🔴, autonomous scheduling je klíčový use case

## Co z OpenFang NEPŘEBÍRAT
- 40 messaging adapterů (máme Telegram MCP)
- 27 LLM providerů (all-in Anthropic)
- Bundled Hands (STOPA skills jsou flexibilnější a composable)
- Rust rewrite (Python stack je správná volba pro orchestraci nad Claude Code)
