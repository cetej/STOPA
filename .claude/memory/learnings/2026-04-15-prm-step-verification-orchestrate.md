---
date: 2026-04-15
type: architecture
severity: high
component: orchestration
tags: [prm, step-verification, critic, early-termination, test-time-scaling]
summary: "Process Reward Models (step-level scoring) dramaticky překonávají Outcome Reward Models (finální verdikt) pro multi-step reasoning. STOPA orchestrate by měl přidat lightweight step-level verification po každém subtasku — haiku check 'splnil krok plán?', kill early při selhání."
source: external_research
uses: 1
successful_uses: 1
harmful_uses: 0
confidence: 0.7
maturity: draft
skill_scope: [orchestrate, critic]
verify_check: "manual"
---

## Detail

arXiv:2501.09686 survey dokumentuje klíčový rozdíl mezi ORM a PRM:

- **ORM (Outcome Reward Model)** = odměna jen za finální výsledek. Ekvivalent současného /critic — spustí se na konci, najde chyby pozdě.
- **PRM (Process Reward Model)** = odměna za KAŽDÝ krok. Identifikuje KDE v řetězci reasoning došlo k chybě. Umožňuje early termination.

PRM výhody pro multi-step orchestraci:
1. **Credit assignment** — ví který agent/subtask selhal (ne jen "celkově špatné")
2. **Early kill** — zastaví pipeline při prvním špatném kroku (šetří budget)
3. **Dense feedback** — agent dostává feedback po každém kroku, ne jen na konci

## Navrhovaná implementace v STOPA

### Orchestrate: Step-level checkpoints

Po dokončení každého subtasku (Phase 5: Execution):
1. Haiku agent (levný, rychlý) zkontroluje: "Splnil výstup tohoto kroku to, co plán vyžadoval?"
2. Scoring: PASS (pokračuj) / WARN (pokračuj s poznámkou) / FAIL (kill pipeline, eskaluj)
3. FAIL → okamžitý stop, reflexion nota, eskalace k uživateli
4. Výsledek se zapíše do step_results[] pro finální critic

### Cost estimate

- Haiku step-check: ~200 tokenů per subtask
- Standard tier (3-4 subtasky): ~800 tokenů navíc (~$0.001)
- Deep tier (6-8 subtasků): ~1600 tokenů navíc (~$0.002)
- ROI: zachráněný budget při early kill >> cost step-checks

### Vs. současný stav

Současně: orchestrate spustí všechny subtasky → /critic na konci → najde chybu v kroku 2 z 6 → 4 kroky zbytečně.
S PRM: orchestrate spustí subtask 1 → PASS → subtask 2 → FAIL → stop → ušetřeny 4 kroky.
