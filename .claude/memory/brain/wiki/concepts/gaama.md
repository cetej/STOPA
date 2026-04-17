# GAAMA — Graph Augmented Associative Memory for Agents

**Source:** arXiv:2603.27910
**Added:** 2026-04-17

## Core Idea

Flat RAG ztrácí strukturální vztahy. Kompresní metody nedokáží zachytit asociativní vzory. GAAMA kombinuje hierarchický knowledge graph s hybridním retrieval — výsledkem je paměť, která "vzpomíná přes asociace", ne jen přes keyword shodu.

## Třívrstvá Architektura

```
Vrstva 3 — REFLECTION: Higher-order syntézy z faktů
    ↑ synthesized from
Vrstva 2 — FACT + CONCEPT: Atomická fakta + topic koncepty (LLM extraction)
    ↑ extracted from
Vrstva 1 — EPISODE: Raw konverzace verbatim
```

**4 typy nodů**: episode, fact, reflection, concept
**5 typů hran**: (typed relationships enabling PPR traversal)

## Retrieval Mechanismus

**Hybridní kombinace:**
1. Cosine k-NN semantic search (tradiční embedding similarity)
2. Edge-type-aware Personalized PageRank (PPR) — propaguje relevanci přes hrany grafu

PPR insight: relevance se šíří přes konceptuální hrany — "fakta asociovaná se stejnými koncepty jako dotaz jsou relevantní, i když keyword similarity je nízká."

Ablation: hybrid ranking → +1.0pp nad semantic-only. Graf walk samotný nestačí, ale jako second-pass re-ranker je klíčový.

## Výsledky (LoCoMo-10 benchmark — 1540 otázek, 10 konverzací)

| Systém | Mean Reward |
|--------|-------------|
| **GAAMA** | **78.9%** |
| RAG baseline | 75.0% |
| HippoRAG | 69.9% |
| Nemori | 52.1% |
| A-Mem | 47.2% |

## Klíčový insight: Koncept uzly jako mediátory

Konceptuální vrstva je bridge mezi episodickou a reflektivní: "Zmínil jsem 'Python' v 5 různých konverzacích" → concept node Python → episody spojené přes tento uzel jsou asociativně příbuzné. Toto umožňuje cross-session retrieval bez explicitního propojení epizod.

## Significance pro 2BRAIN

2BRAIN knowledge-graph.json již implementuje principy GAAMA:
- Typed nodes (person, concept, project, reasoning) ↔ GAAMA node types
- Typed edges ↔ GAAMA edge types
- Wiki articles ↔ Reflection layer synthesis

Chybí: episodická vrstva (raw conversations) a PPR retrieval. Hybridní retrieval v `hybrid-retrieve.py` lze rozšířit o PPR přes knowledge-graph.json pro asociativní recall.

## Connections

- Formalizes: [[agent-memory-taxonomy]] — GAAMA přidává konkrétní implementaci 4-node/5-edge schema k write-manage-read taxonomii
- Related: [[ecphory-rag]] — oba graf-based, EcphoryRAG entity-centric s 94% token reduction, GAAMA PPR-based s benchmark SOTA
- Enables: [[second-brain]] — GAAMA architektura s 78.9% validuje KG-based second brain přístup empiricky
- Related: [[memfactory]] — MemFactory: RL-based update policy; GAAMA: graph-based struktura. Komplementární: MemFactory řídí CO udržovat, GAAMA JAK strukturovat
- Related: [[active-metacognitive-curation]] — reflection nodes ≈ metacognitive curation výstup; GAAMA implementuje synthesis tier
