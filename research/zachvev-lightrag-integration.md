# Záchvěv + LightRAG — Integration Spec

**Datum:** 2026-03-23
**Status:** DRAFT
**Cílový projekt:** [ZACHVEV](https://github.com/cetej/ZACHVEV) (v0.7.0)

---

## 1. Motivace

Záchvěv aktuálně detekuje kaskády přes statistické signály (EWS variance, AC1, Kendall tau) a NLP lexikony. **Chybí strukturální vrstva** — kdo šíří co, jak se narativy propojují přes aktéry a komunity, jaké entity se opakují napříč tématy.

LightRAG přidá **knowledge graf** extrahovaný z Reddit postů/komentářů, který umožní:

| Schopnost | Bez LightRAG | S LightRAG |
|-----------|-------------|------------|
| Kdo šíří narativ X? | Nelze (jen agregáty) | Graf: autor → narativ → komunita |
| Propojení témat? | HDBSCAN clustery (izolované) | Entity sdílené mezi clustery |
| Historická paměť | Session-based (reset) | Perzistentní knowledge graf |
| Dotazování analytika | Žádné | "Jaké narativy šíří účet X?" |
| Kontext pro CRI | Cluster metadata proxy | Skutečná síťová struktura |

---

## 2. Architektura integrace

### 2.1 Kde v pipeline

```
STÁVAJÍCÍ PIPELINE:
  Ingest → Sentiment → Embeddings → Topics → CRI → Campaign

NOVÁ PIPELINE (LightRAG větev):
  Ingest → Sentiment → Embeddings → Topics → CRI → Campaign
                 ↓
           LightRAG indexace (paralelní)
                 ↓
           Knowledge Graf
                 ↓
           Strukturální obohacení CRI
                 ↓
           Analytický dotazovací endpoint
```

LightRAG běží **paralelně** s hlavní pipeline — neblokuje stávající flow. Obohacuje CRI o strukturální signály z grafu.

### 2.2 Co se indexuje

Každý Reddit post/komentář se vloží do LightRAG jako dokument:

```python
doc = f"""
Subreddit: r/{row['subreddit']}
Autor: u/{row['author']}
Datum: {row['created_utc']}
Sentiment: {row['sent_label']} ({row['sent_sentiment_num']:.2f})
Téma: {row.get('topic_label', 'unknown')}
---
{row['title']}
{row['selftext'] or row['body']}
"""
```

Metadata (subreddit, autor, datum, sentiment, téma) se vloží jako kontext pro extrakci — LLM je vidí a extrahuje entity s tímto kontextem.

### 2.3 Očekávané entity typy

Konfigurace `ENTITY_TYPES` pro Záchvěv:

```python
ENTITY_TYPES = [
    "Osoba",           # autor, zmíněná osoba, politik
    "Organizace",      # strana, firma, média, NGO
    "Komunita",        # subreddit, online skupina
    "Narativ",         # opakující se tvrzení / frame
    "Událost",         # protest, volby, skandál
    "Lokace",          # město, region, stát
    "Médium",          # zdroj informace (odkaz, web)
]
```

### 2.4 Dotazovací režimy

| Režim | Použití v Záchvěvu |
|-------|-------------------|
| `hybrid` | Default — "Jaké narativy se šíří kolem události X?" |
| `local` | Entity-centric — "Co víme o účtu u/xyz?" |
| `global` | Relační — "Jaké vztahy existují mezi narativy a komunitami?" |
| `mix` | Fallback — když hybrid nestačí, přidá surové chunky |

---

## 3. Technická specifikace

### 3.1 Nový modul

```
zachvev/
├── knowledge/              # NOVÝ modul
│   ├── __init__.py
│   ├── graph.py            # LightRAG wrapper (init, index, query)
│   ├── enrichment.py       # CRI strukturální obohacení z grafu
│   └── config.py           # LightRAG konfigurace
```

### 3.2 `graph.py` — hlavní wrapper

```python
from lightrag import LightRAG, QueryParam
from lightrag.llm.openai import openai_complete_if_cache, openai_embedding
from lightrag.utils import EmbeddingFunc
from pathlib import Path

class ZachvevKnowledgeGraph:
    """LightRAG wrapper pro Záchvěv."""

    def __init__(self, working_dir: str = "data/knowledge_graph"):
        self.rag = LightRAG(
            working_dir=working_dir,
            llm_model_func=openai_complete_if_cache,
            llm_model_name="gpt-4o-mini",          # levné pro extrakci
            llm_model_max_async=4,
            embedding_func=EmbeddingFunc(
                embedding_dim=1536,
                max_token_size=8192,
                func=lambda texts: openai_embedding(texts, model="text-embedding-3-small"),
            ),
            chunk_token_size=1600,
            chunk_overlap_token_size=200,
            entity_extract_max_gleaning=0,          # šetří tokeny
            entity_types=ZACHVEV_ENTITY_TYPES,
            enable_llm_cache=True,
        )

    async def index_posts(self, df: pd.DataFrame) -> int:
        """Indexuj DataFrame s Reddit posty do knowledge grafu."""
        documents = []
        doc_ids = []
        for _, row in df.iterrows():
            doc = self._format_document(row)
            documents.append(doc)
            doc_ids.append(row.get("id", compute_mdhash_id(doc)))
        await self.rag.ainsert(documents, ids=doc_ids)
        return len(documents)

    async def query(self, question: str, mode: str = "hybrid") -> dict:
        """Dotaz na knowledge graf."""
        result = await self.rag.aquery(
            question,
            param=QueryParam(
                mode=mode,
                top_k=30,
                max_total_tokens=20000,
            ),
        )
        return {"answer": result.content, "sources": result.raw_data}

    async def get_entity_network(self, entity_name: str) -> dict:
        """Získej síť kolem entity (pro vizualizaci)."""
        graph = self.rag.chunk_entity_relation_graph
        edges = await graph.get_node_edges(entity_name)
        node = await graph.get_node(entity_name)
        return {"node": node, "edges": edges}
```

### 3.3 `enrichment.py` — CRI obohacení

```python
async def structural_enrichment(kg: ZachvevKnowledgeGraph, topic_label: str) -> dict:
    """Extrahuj strukturální signály z knowledge grafu pro CRI."""

    # Kolik unikátních aktérů šíří narativy v tomto tématu?
    result = await kg.query(
        f"Kteří autoři a organizace jsou zapojeni do tématu '{topic_label}'?",
        mode="local",
    )

    # Jak propojené jsou entity (cross-topic overlap)?
    cross = await kg.query(
        f"Jaké entity z tématu '{topic_label}' se objevují i v jiných tématech?",
        mode="global",
    )

    return {
        "actor_count": ...,         # počet unikátních aktérů
        "cross_topic_entities": ..., # entity sdílené mezi tématy
        "narrative_coherence": ...,  # jak konzistentní jsou narativy
        "network_density": ...,      # hustota grafu kolem tématu
    }
```

Tyto signály vstoupí do **strukturálního pilíře CRI** (váha 0.3), kde nahradí stávající cluster metadata proxy skutečnými síťovými metrikami.

### 3.4 API endpointy

Přidat do `zachvev/api/app.py`:

```python
# Knowledge graf dotazy
POST /api/knowledge/query    {"question": "...", "mode": "hybrid"}
GET  /api/knowledge/entity/{name}   # síť kolem entity
GET  /api/knowledge/stats    # počet entit, relací, dokumentů

# Indexace (spouští se automaticky po ingestu, nebo ručně)
POST /api/knowledge/index    {"session_id": "..."}  # indexuj aktuální session
```

### 3.5 Storage

| Fáze | Backend | Důvod |
|------|---------|-------|
| PoC | Default (JSON + NanoVectorDB + NetworkX) | Zero-config, stačí pro <5K postů |
| Produkce | PostgreSQL + pgvector | Jeden DB, perzistence, škálovatelnost |

Working directory: `data/knowledge_graph/` (gitignored, jako ostatní data).

---

## 4. Implementační plán

### Fáze 1 — PoC (1 session)

1. `pip install lightrag[openai]` do ZACHVEV
2. Vytvořit `zachvev/knowledge/` modul (graph.py, config.py)
3. Indexovat existující `letna_sentiment.parquet` (417 postů)
4. Ověřit extrakci — jaké entity a relace se vytvoří
5. Ruční dotazy přes CLI: "Kdo organizoval protest na Letné?"

**Úspěch:** Graf obsahuje smysluplné entity (osoby, organizace, narativy), relace odpovídají realitě.

### Fáze 2 — Pipeline integrace (1 session)

1. Napojit `index_posts()` do stávajícího ingest flow (paralelní)
2. Přidat `/api/knowledge/*` endpointy
3. UI panel v Streamlit: dotazovací pole + vizualizace entity sítě
4. Automatická indexace po každém scanu/searchi

### Fáze 3 — CRI obohacení (1 session)

1. Implementovat `enrichment.py`
2. Napojit strukturální signály do CRI kalkulace
3. Porovnat CRI s/bez LightRAG na Letná datasetu
4. Validovat: zlepšuje graf prediktivní hodnotu CRI?

### Fáze 4 — Produkční hardening (volitelné)

1. Migrace na PostgreSQL + pgvector
2. Inkrementální indexace (nové posty, ne celý dataset)
3. Graf maintenance (deduplikace entit, merge starých sessions)
4. Prompt tuning pro české texty (custom extraction prompt)

---

## 5. Cenový odhad (Fáze 1 PoC)

Dataset: ~500 postů → ~500 chunků

| Operace | Model | Tokeny/chunk | Celkem | Cena |
|---------|-------|-------------|--------|------|
| Extrakce entit | gpt-4o-mini | ~2K in + ~500 out | ~1.25M | ~$0.25 |
| Embeddings | text-embedding-3-small | ~400 | ~200K | ~$0.004 |
| Dotazy (10×) | gpt-4o-mini | ~5K/dotaz | ~50K | ~$0.01 |
| **Celkem PoC** | | | | **~$0.27** |

Pro produkci (~50K postů): ~$25 jednorázová indexace, pak marginální pro dotazy.

---

## 6. Rizika a mitigace

| Riziko | Pravděpodobnost | Dopad | Mitigace |
|--------|----------------|-------|----------|
| LLM extrahuje nesmysly z krátkých postů | Střední | Špatný graf | Filtrovat posty <50 znaků, custom prompt |
| České texty → anglické entity | Střední | Nekonzistence | Custom extraction prompt s "odpověz česky" |
| Indexace trvá dlouho | Nízká | UX | Async + progress bar, paralelní s pipeline |
| gpt-4o-mini nestačí na kvalitní extrakci | Nízká | Šum v grafu | Fallback na gpt-4o pro komplex posty |
| Duplikátní entity ("Babiš" vs "Andrej Babiš") | Vysoká | Fragmentace | Entity resolution post-processing |

---

## 7. Rozhodnutí — POTVRZENO (2026-03-23)

| # | Otázka | Rozhodnutí | Důvod |
|---|--------|-----------|-------|
| 1 | LLM provider | **gpt-4o-mini** | Extrakce je formulaická, 2× levnější než Haiku |
| 2 | Jazyk extrakce | **Anglické prompty, české entity** | LightRAG prompty otestované, entity z CZ textu vyjdou česky automaticky |
| 3 | Scope Fáze 1 | **Jen Letná dataset** (417 postů) | Známá ground truth, validovatelné výsledky |
| 4 | Embedding model | **text-embedding-3-small** (1536-dim) | Oddělený namespace od stávajících Seznam embeddings (ty zůstávají pro UMAP/HDBSCAN) |
| 5 | CRI váhy | **Beze změny** (0.4/0.3/0.3) | Nejdřív změřit přínos grafu, pak ladit váhy na základě dat |
