# Two Generators Pattern

**Type:** reasoning
**Tags:** architecture, retrieval, mental-model
**Related:** [[second-brain]], [[ecphory-rag]], [[context-engineering]]
**Source:** Reor Project (GitHub)

---

Architektonický vzor: jeden retrieval pipeline, dva konzumenti — člověk a LLM.

## Princip

```
                    ┌─── Human (editor sidebar: related notes)
Retrieval Pipeline ─┤
                    └─── LLM (Q&A: synthesized answer with citations)
```

Stejný embedding index / knowledge graph slouží oběma. Člověk vidí related notes v sidebaru při editaci. LLM stejné notes použije pro RAG odpovědi.

## Proč je to silný vzor

1. **Single source of truth** — žádná duplikace retrieval logiky
2. **Human auditovatelnost** — člověk vidí co LLM používá
3. **Symbiosis** — člověk opravuje connections, LLM je využívá; LLM nachází patterns, člověk je validuje

## Implementace v 2BRAIN

- **LLM generátor**: hybrid-retrieve.py prohledá brain/ → syntetizuje odpověď
- **Human generátor**: wiki/index.md + knowledge-graph.json umožní člověku navigovat ručně
- **Shared index**: knowledge-graph.json + grep-first retrieval slouží oběma

## Omezení

- Auto-linking (vector similarity) ≠ intentional linking (Zettelkasten)
- Vector similarity: "tyto texty jsou si podobné"
- Intentional link: "PROTO spolu tyto myšlenky souvisí"
- 2BRAIN řeší obojí: knowledge-graph.json edges = intentional, aliases.json + grep = discovery
