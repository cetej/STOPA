---
date: 2026-04-26
status: evaluated
issue: https://github.com/cetej/STOPA/issues/18
paper: arXiv:2604.17009
wiki_concept: .claude/memory/brain/wiki/concepts/paramanager-orchestrator.md
---

# ParaManager — STOPA Gap Analysis

## TL;DR

ParaManager (arXiv:2604.17009) říká: **small model + standardized Agent-as-Tool interface > large model + heterogeneous APIs**. STOPA `/orchestrate` má 3 ze 4 ParaManager features hotové. Skutečný gap je **formal state feedback contract** pro Agent() returns. Issue Suggested Action #1 (Haiku light-tier swap) je **už implementovaná** přes `tier-definitions.yaml`.

## ParaManager 4 Features vs STOPA

| ParaManager Feature | STOPA Status | Evidence |
|---|---|---|
| Parallel subtask decomposition | ✅ Done | `/orchestrate` Phase 4: subtasks v `wave:` skupinách, `run_in_background: true` (Paseo pattern, SKILL.md L744) |
| Asynchronous execution | ✅ Done | Same — non-blocking Agent() launch v rámci wave |
| Decoupled planning | ✅ Done | Plan-on-disk v `state.md` (L507-511), separace plan vs execution phases |
| **State feedback (po každé akci)** | ❌ **Chybí formal contract** | L954: "Agent output: {artifact summary — first 500 chars}" — free-form parsing, ne strukturovaný protokol |

**Agent-as-Tool paradigm**: STOPA má částečně — Agent() calls jsou uniform, `method: "Agent:general"` / `method: "Skill:/review"` v subtask schema (L510-511). Ale chybí **standardizovaný return shape** napříč skill/agent invokacemi.

## Discovery: "Haiku light-tier" je už hotová

Issue #18 Suggested Action #1: *"Evaluate jestli /orchestrate light-tier můžu switch na Haiku."*

**Status: ALREADY IMPLEMENTED.** `.claude/skills/orchestrate/references/tier-definitions.yaml`:
```yaml
tiers:
  light:    {model: haiku,  agent_limit: 1, ...}
  standard: {model: sonnet, agent_limit: 4, ...}
  deep:     {model: opus,   agent_limit: 8, ...}
  farm:     {model: sonnet, agent_limit: 8, ...}
```

Pozn.: `/orchestrate` SKILL.md L22 má `model: opus` — to je **orchestrator's own** model, ne workerů. Otázka jestli orchestrátor SAMOTNÝ by měl být Haiku na light tier (pure ParaManager thesis) je samostatná — vyžaduje A/B test, ne re-implementaci tier definic.

## Skutečný gap: Formal state feedback contract

ParaManager design vyžaduje "explicit state signals after each action". STOPA momentálně:

**Co se vrací po Agent() call (current state):**
- Free-form text output, parsed v orchestrátoru jako "artifact summary — first 500 chars" (L954)
- Žádný status enum, žádný structured blockers field, žádný next-action signal
- Orchestrátor musí inferovat z prózy jestli agent uspěl, byl blocked, nebo potřebuje retry

**Co by ParaManager-style contract vypadal:**
```json
{
  "status": "complete" | "blocked" | "partial" | "failed",
  "subtask_id": "st-2",
  "artifacts": ["path/to/file1.py", "outputs/eval.md"],
  "verified": true | false,
  "verification_method": "tests pass" | "manual" | "none",
  "blockers": [{"type": "missing_dep", "detail": "..."}],
  "next_action_signal": "ready_for_critic" | "needs_user_input" | "next_wave",
  "brief": "1-sentence summary"
}
```

**Benefity:**
1. Orchestrátor parsuje strukturovaně, ne LLM-inference z prózy → menší token cost na Phase 5 critic gate
2. `next_action_signal` umožňuje deterministic flow control (ne LLM rozhoduje co dál)
3. `verified: false` + `verification_method: "none"` → automatic trigger /verify handoff
4. Cross-skill compatibility — všechny skills vrací stejný shape, swappable

## Doporučení: Minimal proxy (#20-style)

Jako u #20 (rule-based selector místo plné RL training), minimal proxy by byl:

### Phase 1 — Contract spec (low risk)
1. Napsat `references/agent-return-contract.md` v orchestrate skill — JSON schema + 3 příklady
2. Update orchestrate Phase 4 prompt template: "Agent MUST return JSON matching this contract: {schema}"
3. Backward compat: pokud agent vrací free-form, orchestrátor fallback na L954 chování

### Phase 2 — Pilot test (1 task, 30 min)
- Spustit 1 light-tier task s contract-enforced returns
- Měřit: Phase 5 critic prompt size (tokens), success rate vs baseline

### Phase 3 — Adopt pokud signal pozitivní
- Promote contract do core-invariants
- Update agent worker SKILL.md templates s return shape requirement

### Co NE-implementovat v proxy
- ❌ RL training (paper Section 4) — out of scope, requires labeled trajectories
- ❌ SFT s recovery mechanisms — overkill pro current STOPA scale
- ❌ Light-tier orchestrátor swap (opus→haiku) — separate experiment, závislé na contract

## Side effects pokud bude adopted

- **Plan chain validation** (rules/skill-files.md `effects:` field) by mohlo využít `next_action_signal` automaticky
- **Outcome credit** (`outcome-credit.py` hook) získá structured input místo regex parsing
- **/eval trace replay** dostane consistent schema napříč skill runy

## Status pro issue

**Issue zůstává OPEN** — proxy implementace je další session task. Recommend user-call:
- `light` (Phase 1 only): ~30 min, design contract spec, žádná code change
- `medium` (Phase 1+2): ~60 min, contract + 1 pilot test, dokumentovat findings
- `full` (Phase 1+2+3): ~3-4 hod, adoption napříč všemi skills, breaking change pro existing agent templates

Phase 1 doporučuju nezávisle — design doc je užitečný i kdyby pilot neproběhl.
