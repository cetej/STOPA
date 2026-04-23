---
title: Chase Context-Engineering 5-Pattern Gap Analysis
date: 2026-04-23
source: startuphub.ai/ai-news/ai-video/2026/context-engineering-is-the-new-ai-moat
author: Harrison Chase (LangChain CEO), April 2026
analyst: claude (hungry-grothendieck-8125a9)
---

# Chase Context-Engineering 5-Pattern Gap Analysis

## Executive Summary

STOPA pokrývá **4/5 Chase patterns plně**, **1/5 částečně** (#4 HITL).
Trace infrastruktura (session-trace.py + trace-capture.py + trace-bridge.py + /eval)
je silnější než baseline audit předpokládal → #1 reclass: partial → **full**.

**Top gap akce** (seřazeno podle effort/impact):

1. **#4 Align Eval loop** — proaktivní trace annotation. Dnes máme implicit loop
   (corrections.jsonl → auto eval case po 2+ opakování). Chybí explicit UX kde
   user projde minulou session a označí "tento decision byl špatně". Effort ~3h.
2. **#1 Agent hierarchy v trace** — `session-trace.py` zachytává `skill:` ale ne
   `agent_id`/`parent_agent`. Multi-agent orchestration je un-attributable. Effort ~1h.
3. **#1 Decision rationale** — trace má tool/input/output, ale ne "proč Claude zvolil
   tuhle větev". Nice-to-have, nižší priorita. Effort ~2h.

**Verdict**: STOPA je **Chase-kompatibilní**. #4 gap není blokátor — existující
correction → eval case pipeline je funkční ekvivalent, jen bez proaktivního UX.

---

## Pattern #1: Trace-Based Observability

**Pokrytí**: **Full** (reclass z "partial" po inspekci kódu)

**Evidence**:
- [session-trace.py](.claude/hooks/session-trace.py) — PostToolUse hook, always-on,
  lightweight. Zapisuje `{ts, tool, exit, path, cmd, skill}` do `.traces/sessions/*.jsonl`.
  Read-only tools skipped pokud nefailují. Auto-purge po 14 dnech.
- [trace-capture.py](.claude/hooks/trace-capture.py) — PostToolUse hook, rich trace
  during optimization runs (marker-gated via `.claude/memory/intermediate/trace-active.json`).
  Captures input_snippet(500), output_snippet(2000), output_full(errors), tokens_est, iteration.
  Meta-Harness inspired (arXiv:2603.28052, 56.7% vs 38.7%).
- [trace-bridge.py](.claude/hooks/trace-bridge.py) — Stop hook, bridges run traces
  into session traces → unified replay via `/discover` a `/eval`.
- [/eval skill](.claude/skills/eval/SKILL.md) — grading, replay, baseline diff,
  regression detection. Explicit `--replay`, `--diff`, `--baseline` modes.
- `retrieval-metrics.jsonl` (ADR 0016 Phase C) — retrieval-specific subset.
- Active session trace: `.traces/sessions/2026-04-21-0206.jsonl` (existuje).

**Gap** (minor, nice-to-have):
- Agent hierarchy: `session-trace.py` record nezachytává `agent_id` ani `parent_agent`,
  takže sub-agent volání (Agent tool) není attributable na konkrétní sub-agent run.
- Decision rationale: záznam má WHAT (tool, input, output), ne WHY. Replay ukáže
  "Claude udělal X", ale ne "Claude zvolil X protože Y".

**Akce**: Pattern je kvalifikačně full. Pokud chceme posílit, přidat `agent_id` a
`parent_agent` do session-trace.py record (6 řádků kódu v `main()`).

---

## Pattern #2: State Management Across Steps

**Pokrytí**: **Full**

**Evidence**:
- [state.md](.claude/memory/state.md) — per-task YAML frontmatter + markdown,
  aktivní task tracking (31 řádků, aktuální).
- [checkpoint.md](.claude/memory/checkpoint.md) — session snapshot (65 řádků),
  last commit, resume prompt.
- [activity-log.md](.claude/memory/activity-log.md) — 708 řádků (⚠ over 500 limit,
  kandidát na archivaci při maintenance per `memory-files.md`).
- `.claude/memory/intermediate/` — per-skill post-it pattern (max 30 řádků, overwrite,
  24h TTL), `farm-ledger.md` pro shared group trace.

**Gap**: žádný architektonický. Pouze operational: activity-log.md přes limit.

**Akce**: `/sweep` nebo `/evolve` navrhne archivaci activity-log.md → activity-log-archive.md.

---

## Pattern #3: Externalized Memory Systems

**Pokrytí**: **Full** (ADR 0017 implementing)

**Evidence**:
- [ADR 0017](docs/decisions/0017-memory-backend-abstraction.md) — MemoryBackend ABC,
  LocalMemoryAdapter + CMMemoryAdapter (mock), contract tests.
- `.claude/memory/learnings/` — per-file YAML learnings (grep-first retrieval,
  supersedes/related graph, maturity tiers, confidence decay).
- `.claude/memory/failures/` — HERA-inspired failure trajectories (arXiv:2604.00901).
- `.claude/memory/outcomes/` — RCL credit records (arXiv:2604.03189).
- `~/.claude/memory/projects/*.yaml` — global project profiles pro cross-project routing.
- Auto-memory system v `C:\Users\stock\.claude\projects\...\memory\` (persistent napříč sessions).

**Gap**: žádný.

**Akce**: pokračovat v ADR 0017 implementation (CM adapter wiring).

---

## Pattern #4: Human-in-the-Loop Validation

**Pokrytí**: **Partial** — máme implicit loop, chybí proaktivní trace annotation

**Evidence (co máme)**:
- [corrections.jsonl](.claude/memory/corrections.jsonl) — 34 záznamů od 2026-03-29.
  Auto-detekce CZ+EN phrases, frustration signals.
- [correction-tracker.py](.claude/hooks/correction-tracker.py) — UserPromptSubmit hook.
  Similarity-based dedup. Po 2+ opakováních auto-generuje eval case v `.claude/evals/`
  (skeleton input.md / expected.md / eval.md).
- [permission-sentinel.py](.claude/hooks/permission-sentinel.py) — L2 LLM-gated
  approval (GuardAgent inspired, arXiv:2406.09187). Currently opt-in, fail-closed.
- [/critic skill](.claude/skills/critic/SKILL.md) — automated review (ne HITL, ale gate).

**Gap (co chybí proti Chase "Align Evals")**:
- Chase's Align Evals = user proaktivně projde trace a označí "tento step good,
  tento bad" → kumulativní dataset → replay na budoucí sessions.
- STOPA dělá opak: čeká na user correction/frustration → capture. Tj. **reactive**,
  ne **proactive** annotation.
- Chybí UI/skill pro retrospective trace review: "ukaž mi trace z včerejška, označ chyby".
- Současný correction-tracker řeší in-session real-time, ne post-hoc trace audit.

**Akce**: Přidat `/annotate` skill (Tier 2, phase=review). Workflow:
1. Seznam recent session traces z `.traces/sessions/` (last 7 dní)
2. User vybere trace → skill přečte JSONL + transcript
3. Pro každý non-trivial decision point: user zvolí `good | bad | skip`
4. "Bad" anotace → nový eval case v `.claude/evals/annotated/` + entry do
   `.claude/memory/annotations.jsonl`
5. `/evolve` čte annotations při graduaci learnings (boost u user-confirmed bad patterns)

Effort: ~3h (skill file + jednoduchý TSV/JSONL handler + unit test).

---

## Pattern #5: Recursive Self-Improvement

**Pokrytí**: **Full**

**Evidence**:
- [/dreams](.claude/skills/dreams/SKILL.md) — offline memory consolidation (cross-link,
  backward-update, pattern surfacing). Běží nightly (evidence:
  `.claude/memory/dreams/2026-04-11.md`…`2026-04-21-skip.md`).
- [/evolve](.claude/skills/evolve/SKILL.md) — learning audit, graduation (draft →
  validated → core), critical-patterns.md promotion.
- [/self-evolve](.claude/skills/self-evolve/SKILL.md) — adversarial co-evolution loop
  s auto-generated eval cases (Agent0 inspired).
- `.claude/memory/outcomes/` — 6 recent records (self-evolve, koder).
- `.claude/memory/replay-queue.md` — HERA-inspired failure-sourced learning validation
  (arXiv:2604.00901, +38.69% SOTA).
- `.claude/memory/optstate/` — per-skill momentum (RCL, arXiv:2604.03189).
- [autodream.py](.claude/hooks/autodream.py) — scheduled consolidation hook.

Toto odpovídá Chase's "sleep time compute" téměř doslova: offline agent reflektuje
na past traces (`/dreams` + `/evolve`), updatuje persistent learnings.

**Gap**: žádný.

**Akce**: none — pattern je nadprůměrně silný (Chase baseline říká "agenti reflektují",
STOPA má 4 distinct loop skills + 2 scheduled hooks).

---

## Souhrn

| Pattern | Pokrytí | Top evidence | Gap action |
|---------|---------|--------------|------------|
| #1 Trace Obs | Full | session-trace.py + /eval | (optional) agent_id v record, ~1h |
| #2 State Mgmt | Full | state.md + checkpoint.md + intermediate/ | activity-log archivace (ops) |
| #3 External Mem | Full | ADR 0017 + learnings/ + failures/ + outcomes/ | — |
| #4 HITL | Partial | corrections.jsonl + correction-tracker.py | `/annotate` skill, ~3h |
| #5 Self-Improve | Full | /dreams + /evolve + /self-evolve + replay-queue | — |

**Verdict**: STOPA je Chase-kompatibilní. Jediný skutečný gap je proaktivní trace
annotation (#4) — ale stávající correction → eval case auto-generation je funkční
ekvivalent pro nejčastější use case (opakovaná chyba).

**Celkem 2 konkrétní akce**:
1. `/annotate` skill pro proactive trace review (#4, ~3h) — největší impact
2. `agent_id` v session-trace.py record (#1, ~1h) — optional polish
