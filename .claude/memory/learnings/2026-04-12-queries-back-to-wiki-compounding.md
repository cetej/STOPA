---
date: 2026-04-12
type: best_practice
severity: high
component: memory
tags: [knowledge-management, wiki, compounding, query]
summary: "LLM query answers should be filed back into the wiki as new pages — otherwise insights vanish into chat history and the knowledge base loses compounding. Every good answer is itself a wiki artifact."
source: external_research
maturity: draft
uses: 0
successful_uses: 0
harmful_uses: 0
confidence: 0.7
verify_check: "manual"
---

# Queries Back to Wiki — Compounding Principle

## Detail

Když LLM odpoví na dotaz proti wiki, odpověď sama o sobě je hodnotná — srovnání, analýzy, nová propojení. Pokud se uloží jen do chat history, ztratí se. Pokud se uloží zpět jako wiki stránka (query→artifact), stane se součástí znalostní báze pro budoucí dotazy.

Karpathy: "good answers can be filed back into the wiki as new pages... your explorations compound in the knowledge base just like ingested sources do."

## Application to STOPA

Při `/deepresearch` nebo `/query` operaci: výstup nejen vrátit uživateli, ale nabídnout uložení jako wiki artifact (outputs/*.md). `/ingest --backfill` pak zpracuje tyto výstupy do struktury.

**Why:** Bez tohoto principu wiki stagnuje — přijímá jen ingested sources, ne LLM reasoning výstupy. Se zpětným ukládáním wiki roste i přes explorace, ne jen přes nový input.

**How to apply:** Po `/deepresearch` nebo komplexní `/query`: automaticky nabídnout uložení výstupu do `outputs/<slug>-research.md`. Při příštím `/ingest --backfill` se zpracuje.
