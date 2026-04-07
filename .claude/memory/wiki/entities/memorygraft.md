---
name: MemoryGraft
type: paper
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [agent-memory-problems]
tags: [memory, security, adversarial]
---

# MemoryGraft

> Xiong et al. 2024 (arXiv:2512.16962) — adversarial attack na LLM agent memory: malé množství otrávených záznamů exponenciálně dominuje retrieval výsledky.

## Key Facts

- 10 otrávených záznamů z 110 (9%) → 47.9% všech retrieval výsledků (ref: sources/agent-memory-problems.md)
- Poisoning přetrvává neomezeně napříč sessions
- Embedding similarity nemá mechanismus pro posouzení faktické správnosti
- Plausibilně formulovaná špatná paměť se retrievne stejně snadno jako správná

## Relevance to STOPA

Ukazuje proč STOPA `source:` weighting a `harmful_uses:` counter jsou kritické. Bez provenance trackingu a confidence decay může jediný špatný learning dominovat retrieval. `verify_check:` pole je obrana — machine-checkable assertion ověří faktickou správnost.

## Mentioned In

- [Agent Memory Problems Research](../sources/agent-memory-problems.md)
