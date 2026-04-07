---
name: Schema-utility decoupling
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [toolgenesis-research]
tags: [testing, code-quality, evaluation]
---

# Schema-utility decoupling

> Empirický jev kdy syntakticky/sémanticky správné schéma (vysoké Schema-F1) nepredikuje downstream užitečnost (SR) — demonstrováno na Claude-Haiku-3.5 v Tool-Genesis.

## Key Facts

- Claude-Haiku-3.5 Code-Agent: Schema-F1 0.964 (nejvyšší ze všech), SR jen 0.472 (ref: sources/toolgenesis-research.md)
- Hypotéza autorů: model generuje syntakticky správné schéma "napodobením", ale nedokáže vygenerovat sémanticky konzistentní implementaci
- Mechanismus není plně vysvětlen v paperu
- Obecný princip: povrchové metriky (formát, syntax, schema match) jsou nutné, ale ne dostatečné

## Relevance to STOPA

/critic skill nesmí spoléhat pouze na syntaktické kontroly. Verification checklist musí zahrnovat downstream utility check (funguje to v kontextu?), ne jen format compliance. Odpovídá STOPA core-invariants.md pravidlo č. 6: "Verify before claiming done."

## Mentioned In

- [Tool-Genesis Research Brief](../sources/toolgenesis-research.md)
