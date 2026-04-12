---
name: NLAH Paper — Natural-Language Agent Harnesses
description: arXiv:2603.25723 academic validation of STOPA's SKILL.md approach; NLAH=SKILL.md, IHR=hooks, file-backed state=memory system; ablation results; self-evolution +4.8%, file-backed +5.5%
type: reference
---

## Paper: Natural-Language Agent Harnesses (arXiv:2603.25723)

**Authors:** Pan, Zou, Guo, Ni, Zheng (Tsinghua + HIT Shenzhen)
**Date:** 2026-03-26
**URL:** https://arxiv.org/abs/2603.25723

## Core Thesis

Harness logic (orchestrace, role, kontrakty, failure handling) by měla být **explicitní přenositelný artefakt**,
ne scattered kód. NLAH = natural-language harness soubor. IHR = shared runtime pro jeho exekuci.

## Kanonická workspace struktura (paper)

```
TASK.md              — run-local task statement
SKILL.md             — harness control logic
task_history.jsonl   — append-only invocation record
artifacts/           — benchmark-facing deliverables
children/            — child agent workspaces
```

## STOPA Korespondence

| Paper | STOPA |
|-------|-------|
| NLAH (natural-language harness) | `.claude/skills/<name>/SKILL.md` |
| IHR Runtime Charter | hooks v `.claude/settings.json` |
| File-backed state module | `.claude/memory/` systém |
| Failure taxonomy | circuit breakers, 3-fix escalation |
| Roles (solver/verifier/orchestrator) | sub-agenti s explicit model |
| Contracts | `allowed-tools`, `permission-tier` v SKILL.md |

## Klíčové výsledky (SWE-bench Verified, baseline 75.2%)

| Modul | Delta |
|-------|-------|
| Self-evolution | **+4.8%** |
| File-backed state | +1.6% |
| Evidence-backed answering | +1.6% |
| Verifier | -0.8% (diverguje od benchmark acceptance) |

## Klíčové výsledky (OSWorld, baseline 41.7%)

| Modul | Delta |
|-------|-------|
| File-backed state | **+5.5%** |
| Multi-candidate search | +2.7% |

## Migrace kód → NLAH (RQ3)

OSWorld OS-Symphony: 30.4% (nativní kód) → **47.2%** (NLAH). Ne lepší model, ale topologický shift:
file-backed state + artefaktová verifikace >> screenshot-grounded repair.

## Hlavní varování

- Extra struktura neimplicitně nezlepšuje: Verifier škodí, dynamic orchestration neutrální
- 90% tokenů jde v child agentech, ne v parent threadu → IHR = koordinátor, ne vykonavatel
- Runtime contamination: silný shared runtime může absorbovat harness chování
- Evaluace na GPT-5.4 (vnitřní/experimentální model) — přenositelnost na Claude nepotvrzena
