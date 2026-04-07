---
name: Critic Accuracy Ledger
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [nlah-implementation-plan]
tags: [memory, review, code-quality]
---

# Critic Accuracy Ledger

> JSONL soubor sledující alignment mezi critic verdikty a skutečnými user outcomes — základ pro detekci verifier divergence a calibraci critic vah.

## Key Facts

- Soubor: `.claude/memory/critic-accuracy.jsonl` (ref: sources/nlah-implementation-plan.md)
- Formát: `{date, task, verdict, score, user_outcome, aligned, note}` (ref: sources/nlah-implementation-plan.md)
- Implicit signal (doporučeno jako default): commit po PASS = `accepted/aligned`, commit po FAIL = `overridden/misaligned`, revert po PASS = `rejected/misaligned` (ref: sources/nlah-implementation-plan.md)
- Explicit signal (opt-in): `--feedback` flag po critic → "Souhlasíš s verdiktem? [y/n/skip]" (ref: sources/nlah-implementation-plan.md)
- Hook `critic-accuracy-tracker.py` (PostToolUse na git commit po /critic) (ref: sources/nlah-implementation-plan.md)
- `/evolve` rozšíření: alignment rate z posledních 20 verdiktů; <80% → varování + identifikace divergujících dimenzí (ref: sources/nlah-implementation-plan.md)

## Relevance to STOPA

P2 priorita (4h + 2h evolve). Closure smyčky pro `/critic` — jediný způsob jak empiricky ověřit zda critic váhy odpovídají uživatelským preferencím. Zabraňuje tiché degradaci kvality critic verdiktů.

## Mentioned In

- [NLAH Implementation Plan](../sources/nlah-implementation-plan.md)
