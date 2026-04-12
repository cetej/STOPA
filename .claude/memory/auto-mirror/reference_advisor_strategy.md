---
name: Advisor Strategy (Anthropic)
description: Native API feature — Opus as advisor for Sonnet/Haiku executors, zero orchestration overhead, advisor_20260301 tool
type: reference
---

## Advisor Strategy — Anthropic (2026-04)

**Zdroj:** https://claude.com/blog/the-advisor-strategy

Nativní API pattern: Opus jako rádce + Sonnet/Haiku jako exekutor v jednom API callu.

### Mechanismus

- Exekutor (Sonnet/Haiku) řeší úkol end-to-end, volá tools, iteruje
- Při obtížných rozhodnutích zavolá Opus jako `advisor_20260301` tool
- Opus vrátí plán/korekci (typicky 400-700 tokenů) — sám tools nevolá
- `max_uses` parametr pro cost control

### Výsledky

| Kombinace | Benchmark | Zlepšení | Cost |
|-----------|-----------|----------|------|
| Sonnet + Opus advisor | SWE-bench Multilingual | +2.7 pp | -11.9% |
| Haiku + Opus advisor | BrowseComp | 19.7% → 41.2% | -85% vs solo Sonnet |

### Relevance pro STOPA

- STOPA orchestrace dělá to samé ručně (haiku/sonnet exekutoři, opus pro reasoning)
- Native API výhoda: **nulový orchestrační overhead** — vše v jednom API callu
- STOPA výhoda: **full tool access pro advisor** (native Opus advisor tools nevolá)
- Nejlepší kandidáti pro integraci: `/autoloop`, `/autoresearch` — iterativní smyčky kde Sonnet exekuuje a Opus koriguje strategii
- Integrace: beta header + `advisor_20260301` tool v requestu, advisor tokeny = Opus sazba

### How to apply

Experimentovat při příštím autoloop/autoresearch běhu — změřit cost vs quality oproti současnému tiering. Nenahrazovat orchestrate celý — jen iterativní inner loops.
