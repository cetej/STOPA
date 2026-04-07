---
name: MetaGPT SOPs
type: paper
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [egoa-prompt-techniques]
tags: [orchestration, multi-agent, output-contracts]
---

# MetaGPT SOPs

> Hong et al. 2023 (arXiv:2308.00352) — Standardized Operating Procedures jako prompt sekvence v multi-agent systémech. Assembly-line paradigma kde každý agent produkuje definovaný output format pro dalšího.

## Key Facts

- Explicitní output contracts mezi agenty snižují halucinační kaskády (ref: sources/egoa-prompt-techniques.md)
- Každý agent produkuje definovaný artifact v pevném formátu
- Inspirace pro `output-contract:` field v SKILL.md frontmatter
- `input-contract:` + `output-contract:` umožňují static plan chain validation

## Relevance to STOPA

STOPA skills/skill-files.md již obsahuje `output-contract:` a `input-contract:` pole v SKILL.md frontmatter — přímá implementace MetaGPT SOP vzoru. Orchestrátor by měl ověřovat output(A) satisfies input(B) před spuštěním agentů.

## Mentioned In

- [EgoAlpha/prompt-in-context-learning Research Brief](../sources/egoa-prompt-techniques.md)
