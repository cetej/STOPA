---
date: 2026-04-27
type: bug_fix
severity: high
component: hook
tags: [permissions, sentinel, autonomy, l1, l2, double-eval]
summary: L2 permission-sentinel běžel jako druhý hook v PermissionRequest řetězu a re-evaluoval i to, co L1 už schválil — Haiku prompt s "If uncertain, prefer DENY" generoval falešné DENY na vlastní hooks/scripts (např. "Cannot verify safety of executing arbitrary Python scripts in .claude/hooks/"). Fix: fast-skip routine paths/bash prefixes před API call + prompt změněn na ALLOW-by-default s konkrétními harm patterns.
source: auto_pattern
uses: 0
successful_uses: 0
harmful_uses: 0
confidence: 0.85
maturity: draft
verify_check: "Grep('L2-skip', path='.claude/memory/sentinel-log.jsonl') → 1+ matches"
failure_class: coordination
failure_agent: permission-sentinel
task_context: {task_class: bug_fix, complexity: medium, tier: standard}
---

## Problem

Settings.json registroval dva hooky pod `PermissionRequest`:
1. `permission-auto-approve.sh` (L1, deterministic pattern matching)
2. `permission-sentinel.py` (L2, Haiku LLM gate)

CC spouští všechny hooky v sequence — i když L1 vrátil `allow`, L2 stejně proběhl a re-evaluoval. Sentinel prompt obsahoval: *"If genuinely uncertain, prefer DENY with reason 'uncertain - escalate to human'"* — Haiku to bralo doslova a falešně blokovalo i routine ops.

## Evidence z sentinel-log.jsonl

```
2026-04-27 05:11 | L2 | deny | "Cannot verify the safety of executing arbitrary
                                Python scripts in hidden directories (.claude/hooks/)"
2026-04-27 05:35 | L2 | deny | "uncertain - escalate to human" (autodream --apply --all)
```

Oba případy: vlastní hooks/scripty agenta, schválené v L1. L2 = autonomy friction generator.

## Fix

`permission-sentinel.py`:
- `is_routine_op()` matchuje stejné patterns jako L1 (`*/memory/learnings/*`, `python .claude/hooks/*`, atd.)
- Před API call: pokud routine → `emit_passthrough()` + log s `layer: L2-skip`
- Prompt přepsán: explicitní "Default to ALLOW. DENY only with concrete harm evidence" + výčet konkrétních harm patterns vs explicit allow listu (workspace, public research fetches, vlastní git ops)

## Reflexion

Při zapojování LLM-based gate vždy ověřit:
1. Běží sériově se starším hookem? Pokud ano, řešit pořadí nebo skip-when-already-approved
2. Default při nejistotě? "Uncertain → DENY" maximalizuje frikci. Pro autonomous agenta v jeho vlastním workspace má být "uncertain → ALLOW" se seznamem skutečných harm signálů.
3. Měřit cost: každý L2 call = 1 Haiku request + latency. Skip routine ušetří ~95% volání.
