---
date: 2026-04-14
type: architecture
severity: high
component: orchestration
tags: [orchestration, multi-agent, heartbeat, async, plan-persistence, ci-monitoring, cross-provider]
summary: "Paseo (getpaseo/paseo) — open-source multi-provider orchestrátor pro Claude Code/Codex/OpenCode. 8 adoptovatelných vzorů identifikováno: heartbeat scheduler (5 min), plan-on-disk pro přežití compaction, post-PR CI monitoring loop, cross-provider worker/verifier, event-driven launch (notifyOnFinish), read-only coordinator hard rule, Grill interview phase, preferences persistence. STOPA je silnější v memory/learnings/evolve, Paseo v multi-device/multi-provider distribuci."
source: external_research
uses: 2
successful_uses: 0
harmful_uses: 0
confidence: 1.0
maturity: draft
verify_check: "Glob('outputs/paseo-stopa-research.md') → 1+ matches"
task_context: {task_class: research, complexity: high, tier: standard}
related: [2026-04-12-morning-briefing-cron-pattern.md]
---

## Paseo Orchestration Patterns — Adoption Analysis

**Source:** https://github.com/getpaseo/paseo (AGPL-3.0, active 2026-04-14)
**Full brief:** `outputs/paseo-stopa-research.md`

### P1 — Quick Wins (řeší reálné gapy)

1. **Plan-on-disk**: Orchestrate zapisuje plan do `intermediate/orchestrate-plan.md` — přežije compaction, agenti re-read z disku
2. **Background agents**: `run_in_background: true` v orchestrate místo blokujícího čekání
3. **Heartbeat scheduler**: CronCreate po spuštění agentů — periodický self-check (re-read plan, check agent status, course-correct)

### P2 — Integrations

4. **Post-PR CI loop**: Po PR creation monitorovat `gh pr checks`, spawn fix agent na failure, smazat heartbeat po ALL green
5. **Lightweight Grill**: Batch 1-3 questions PŘED research fází (ale respektovat autonomous behavioral genome)

### P3 — Optimization

6. **Heterogenní verification**: Critic s model override (haiku worker / opus critic)

### Skip (nepřenositelné nebo redundantní)

- Multi-provider routing (Paseo-specific daemon, CC je single-provider)
- Config persistence (STOPA auto-memory + key-facts stačí)
- Dynamic provider registry (overkill pro CC scale)

### STOPA výhody nad Paseo

Learnings system, hybrid retrieval, behavioral genome, core invariants, auto-evolve, dreams consolidation, 50+ skills vs 6, budget tracking — Paseo řeší distribuci, ne knowledge management.

### Doplňkové zdroje

- TAKT (github.com/nrslib/takt): YAML workflow s `edit: false` per step — strukturální read-only enforcement, nejsilnější implementace
- MCP Tasks spec: call-now/fetch-later, `tasks/get` = source of truth, notifications = hints only
- MindStudio heartbeat: Wake→Observe→Reason→Act 4-phase pull loop
- Temporal Signals: guaranteed async delivery across process restarts
