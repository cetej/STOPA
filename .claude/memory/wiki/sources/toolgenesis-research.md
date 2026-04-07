---
title: "Tool-Genesis: A Task-Driven Tool Creation Benchmark for Self-Evolving Language Agents"
slug: toolgenesis-research
source_type: research_output
date_ingested: 2026-04-07
entities_extracted: 8
claims_extracted: 5
---

# Tool-Genesis: A Task-Driven Tool Creation Benchmark for Self-Evolving Language Agents

> **TL;DR**: Tool-Genesis (arXiv:2603.05578) je benchmark pro autonomní tvorbu nástrojů z abstraktních požadavků — 2,150 úkolů, 86 MCP serverů, čtyřúrovňové metriky L1–L4. Klíčové zjištění: ani SOTA modely nedokáží spolehlivě vygenerovat funkční nástroj v jednom průchodu; iterativní oprava s execution feedback (Code-Agent mód) dramaticky zlepšuje výsledky. Anti-intuitivní nález: větší modely lépe exploitují execution feedback, ale nemusí být lepší v one-shot generování (scale reversal).

## Key Claims

1. Qwen3-235B Code-Agent dosahuje SR 0.622 — překonává GPT-5.1 (0.604); open-source model poprvé vede v tool-creation benchmarku — `[verified]`
2. Claude-Haiku-3.5 dosahuje Schema-F1 0.964 (nejlepší ze všech) pod Code-Agent, ale SR jen 0.472 — povrchová správnost schématu nepredikuje downstream užitečnost (schema-utility decoupling) — `[verified]`
3. Scale reversal: Qwen3-32B překonává 235B pod Direct prompting; 235B překonává 32B pod Code-Agent — větší modely lépe exploitují execution feedback — `[verified]`
4. Code-Agent L1 pass-through pro Qwen3-8B: 65.34% → 91.36% vs. Direct — execution feedback je rozhodující proměnná — `[verified]`
5. Finetuning Qwen3-8B: Code-Agent SR 0.336 → 0.399 — repair loop profituje více z fine-tuningu než one-shot generování — `[verified]`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| Tool-Genesis | paper | new |
| Code-Agent (ReAct repair loop) | concept | new |
| EvolveTool-Bench | paper | new |
| CREATOR benchmark | paper | new |
| TM-Bench | paper | new |
| Schema-utility decoupling | concept | new |
| Cascade failure (L1→L4) | concept | new |
| MCP (Model Context Protocol) | concept | existing (check) |

## Relations

- `Tool-Genesis` `evaluates` `Code-Agent (ReAct repair loop)`
- `Code-Agent (ReAct repair loop)` `exhibits` `Scale reversal`
- `Tool-Genesis` `is complementary to` `EvolveTool-Bench`
- `Schema-utility decoupling` `is demonstrated by` `Tool-Genesis`
- `Cascade failure (L1→L4)` `is diagnosed by` `Tool-Genesis L1-L4 metrics`
