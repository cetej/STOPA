# MemFactory — Unified Agent Memory Framework

**Type:** concept  
**Tags:** ai, memory, agent, rl, unified-framework  
**Related:** [[agent-memory-taxonomy]], [[active-metacognitive-curation]], [[second-brain]]  
**Source:** https://arxiv.org/abs/2603.29493  
**Updated:** 2026-04-14

---

Unifikovaný framework pro trénink a evaluaci memory-driven LLM agentů. Inspirovaný LLaMA-Factory — standardizovaná infrastruktura pro memory management místo fragmentovaných task-specific implementací.

## Tři základní paměťové operace

| Operace | Popis |
|---------|-------|
| **Extraction** | Co z interakce uložit do paměti |
| **Updating** | Jak aktualizovat existující záznamy (merge, override, append) |
| **Retrieval** | Jak hledat relevantní paměti pro aktuální kontext |

"Lego-like" modulární komponenty — kombinovatelné pro různé architektury.

## Optimalizace: GRPO

Group Relative Policy Optimization (GRPO) fine-tuní interní memory management policy přes multi-dimensionální environmental rewards. Agent se učí *jak* pracovat s pamětí — nejen co si pamatovat.

## Podporované paradigmata

- **Memory-R1** — RL-based memory reasoning
- **RMM** (Reinforced Memory Management)
- **MemAgent** — agentic memory s hierarchickými strukturami

## Výsledky

Relative gains **až 14.8%** vs base models na evaluačních setech (MemAgent architektura, open-source data).

## Klíčová myšlenka

Extraction/Updating/Retrieval jsou fundamentální primitiva — stejně jako attention/feedforward v transformer architektuře. Systémové porozumění těmto operacím je klíčové pro design memory systems.

## Vztah k 2BRAIN

| MemFactory | 2BRAIN |
|------------|--------|
| Extraction | Ingest (raw/ → wiki/) |
| Updating | Lint (aktualizace existujících articles) |
| Retrieval | Query (hledání relevantních wiki pages) |

MemFactory validuje že 2BRAIN cyklus Ingest/Query/Lint reflektuje fundamentální memory primitiva.
