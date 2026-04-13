# EcphoryRAG

**Type:** concept
**Tags:** ai, retrieval, academic, knowledge-graph, memory
**Related:** [[second-brain]], [[active-metacognitive-curation]], [[karpathy]]
**Source:** arXiv:2510.08958 (Tsinghua, 2025)

---

KG-RAG systém inspirovaný neurovědním konceptem ecphorie: partial cue aktivuje cílenou memory trace (engram), ne full-corpus search.

## Architektura

**Indexování:** Ukládá pouze entity + metadata (žádný full text). 94% redukce tokenů oproti jiným KG-RAG systémům.

**Retrieval:**
1. Extrakce cue entities z dotazu
2. Multi-hop associative search přes knowledge graph
3. Dynamická inference implicitních relací (ne pre-enumerované edges)
4. Populace kontextu pro LLM generaci

## Metriky

- EM (Exact Match): 0.392 → 0.474 nad HippoRAG baseline
- Benchmarky: 2WikiMultiHop, HotpotQA, MuSiQue

## Proč je to relevantní pro 2BRAIN

Principy přímo aplikovatelné:
- **Compress storage, enrich retrieval dynamically** — ukládej entity+metadata do knowledge-graph.json, ne celé dokumenty
- **Cue-based retrieval** — místo keyword matche extrahuj entity z dotazu a projdi graph
- **No exhaustive pre-enumeration** — neinferuj všechny možné relace dopředu, inferuj je at query time

## Vztah ke STOPA

STOPA learnings už fungují entity-centric (YAML frontmatter = metadata, tělo = content). EcphoryRAG validuje tento přístup akademicky a přidává multi-hop graph walk — implementovaný v STOPA jako `hybrid-retrieve.py` + `concept-graph.json`.
