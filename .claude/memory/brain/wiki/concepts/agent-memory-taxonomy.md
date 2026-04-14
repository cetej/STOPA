# Agent Memory Taxonomy (Write-Manage-Read Loop)

**Type:** concept  
**Tags:** ai, memory, agent, taxonomy, survey  
**Related:** [[memfactory]], [[active-metacognitive-curation]], [[second-brain]], [[ecphory-rag]]  
**Source:** https://arxiv.org/abs/2603.07670  
**Updated:** 2026-04-14

---

Formální taxonomie memory systémů pro autonomní LLM agenty z survey 2022–2026. Unifikující rámec: **write-manage-read loop** propojený s perception a action.

## Write-Manage-Read Loop

```
perception → WRITE → [memory store] → MANAGE → RETRIEVE → action
```

Každá fáze je semi-nezávislá a optimalizovatelná odděleně — základ pro modulární design.

## Třírozměrná klasifikace

| Dimenze | Hodnoty | Příklady |
|---------|---------|---------|
| **Temporal scope** | session / cross-session / permanent | chat history / user profile / world knowledge |
| **Representational substrate** | text / vector / graph / structured | markdown / embeddings / KG / JSON |
| **Control policy** | rule-based / learned / hybrid | retention rules / RL policy / threshold+RL |

2BRAIN sedí na: **cross-session + text+graph + hybrid** (rule-based ingest + learned retrieval prioritization).

## Pět rodin memory mechanismů

| Rodina | Princip | Příklady |
|--------|---------|---------|
| **Context-resident compression** | Vměstnání do token window | MemGPT, compression prompts |
| **Retrieval-augmented stores** | Externí KB, vektorové DB | RAG, vector store |
| **Reflective self-improvement** | Učení z past interactions | Reflexion, self-critique |
| **Hierarchical virtual context** | Vrstvená organizace (summary trees) | hierarchical summarization, 2BRAIN |
| **Policy-learned management** | Neuronové řízení paměti přes RL | MemFactory, MemAgent |

2BRAIN primárně implementuje **Hierarchical virtual context** (raw/ → wiki/), s prvky **Reflective self-improvement** (Lint).

## Posun v evaluaci

Od: static recall benchmarks  
Na: multi-session agentic tests interleaving memory s decision-making

Tento posun odhaluje výrazné limitace context-only přístupů (MemGPT, pure RAG).

## Nevyřešené výzvy (2026)

1. **Continual consolidation** bez catastrophic forgetting
2. **Causally grounded retrieval** (příčina, ne korelace)
3. **Trustworthy reflection** (hallucination v paměti samotné)
4. **Learned forgetting** (co aktivně zapomenout)
5. **Multimodal embodied memory** (visual, spatial)

## Aplikace v STOPA

Write-Manage-Read taxonomie formalizuje STOPA memory stack:
- **Write** → `/ingest`, `/scribe`, `/capture`
- **Manage** → `/evolve`, `/compile`, `/sweep`, `/dreams`
- **Read** → grep-first retrieval, hybrid BM25+graph, `/status`
