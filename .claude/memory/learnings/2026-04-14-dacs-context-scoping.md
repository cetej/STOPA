---
date: 2026-04-14
type: architecture
severity: high
component: orchestration
tags: [multi-agent, context-management, token-efficiency]
summary: "DACS (arXiv:2604.07911) — Registry↔Focus context switching pro multi-agent orchestrátory. Registry mode = ≤200 tokenů/agent summary, Focus mode = plný kontext jednoho agenta. 90–98% steering accuracy vs 21–60% baseline, 3.53× context efficiency. Aplikovat v orchestrate pro >3 paralelní agenty."
source: external_research
uses: 2
harmful_uses: 0
successful_uses: 0
confidence: 0.9
maturity: draft
skill_scope: [orchestrate]
related: [2026-04-11-task-guided-context-beats-raw-sharing.md, 2026-04-11-compression-regime-maps-to-tiers.md]
verify_check: "Grep('DACS', path='.claude/skills/orchestrate/SKILL.md') → 1+ matches"
---

## DACS — Dynamic Attentional Context Scoping

**Paper**: arXiv:2604.07911 (April 9, 2026)

**Problem**: When N concurrent agents report to an orchestrator, their combined context contaminates the orchestrator's window — steering accuracy drops to 21–60%.

**Solution**: Two-mode context management:
- **Registry mode** (default): Each agent represented by ≤200-token summary (name, subtask, status, last output hash). Orchestrator sees all agents at minimal cost.
- **Focus mode** (on demand): Full context of ONE agent loaded into orchestrator. Other agents compressed to registry entries.
- **Switch trigger**: Agent reports NEEDS_CONTEXT or BLOCKED → Focus mode for that agent.

**Results**: 90–98% steering accuracy, 3.53× context efficiency ratio.

**STOPA application**: Added to `/orchestrate` SKILL.md Phase 4 → Agent Execution. Trigger: `len(active_agents) > 3 AND tier in (standard, deep, farm)`.
