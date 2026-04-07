---
name: ACE (Agentic Context Engineering)
type: tool
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [ace-agentic-context-engineering]
tags: [memory, self-improvement, context-management]
---

# ACE (Agentic Context Engineering)

> Qizheng Zhang et al. (arXiv:2510.04618) — self-improving systém pro správu kontextu agentů přes append-only delta updates s bullet IDs a helpful/harmful countery.

## Key Facts

- Bullet wire format: `[sec-00001] helpful=4 harmful=1 :: content` — každý záznam nese vlastní výkonnostní historii (ref: sources/ace-agentic-context-engineering.md)
- Reflector (analýza chyb) je oddělen od Curator (rozhodnutí co zapsat) — 2 separátní LLM volání
- BulletpointAnalyzer: sentence-transformers + FAISS, cosine ≥ 0.90 pro merge near-duplicates
- 86.9% nižší adaptation latence, 83.6% nižší token cost vs Dynamic Cheatsheet
- UPDATE/MERGE/DELETE v API ale pouze ADD implementováno na main branch

## Relevance to STOPA

STOPA learnings systém přidal `uses:`, `harmful_uses:`, `confidence:` countery inspirované přímo ACE bullet wire formátem. Separation of Reflector/Curator by měl být implementován jako Reflexion nota + /scribe oddělení. ACE append-only vzor potvrzuje STOPA learnings per-file přístup.

## Mentioned In

- [ACE — Agentic Context Engineering](../sources/ace-agentic-context-engineering.md)
