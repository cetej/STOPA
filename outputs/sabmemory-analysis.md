# sabmemory — Rozbor a doporučení pro STOPA

**Datum**: 2026-03-26
**Zdroj**: https://github.com/Sablinova/sabmemory
**Verze**: 0.1.0 (Rust, MIT license)

## Co to je

Lightweight MCP memory server v Rustu. Jediný statický binární soubor (4.1 MB), ~6 MB RAM za běhu.
SQLite FTS5 full-text search místo vector embeddings. Zero dependencies — žádný Python, Node, ML modely.

49 MCP tools: memories, entities, projects, documents, code artifacts, relationships, profily, versioning.

## Architektura

```
sabmemory serve (stdio MCP)     sabmemory dashboard --port 3080
        │                                │
        ▼                                ▼
   ~/.local/share/sabmemory/sabmemory.db (SQLite + FTS5)
```

- **Search**: FTS5 + BM25 ranking + importance score boosting
- **Storage**: Jediný SQLite soubor, FTS5 virtual tables
- **Auto-linking**: Nové memories automaticky propojeny s podobnými přes FTS5
- **Auto-forget**: `forget_after` datum → soft-forget + audit trail
- **Versioning**: Řetězy (updates/extends/derives), jen latest v search results
- **Token budget**: Výsledky omezeny konfigurovatelným limitem (default 8000 tokens)
- **Dashboard**: 3D WebGL knowledge graph vizualizace (Three.js)

## Srovnání se STOPA memory

| Aspekt | STOPA (file-based) | sabmemory |
|--------|-------------------|-----------|
| **Storage** | `.claude/memory/*.md` | SQLite FTS5 |
| **Search** | `grep` + MEMORY.md index | FTS5 BM25 + importance boosting |
| **Sémantika** | Žádná (keyword only) | Žádná (keyword only, ale lepší ranking) |
| **Auto-linking** | Manuální (MEMORY.md pointery) | Automatické přes FTS5 similarity |
| **Versioning** | Append-only markdown | Řetězy (updates/extends/derives) |
| **Expiry** | Manuální maintenance | Auto-forget s datem |
| **Knowledge graph** | Ne | Ano (entities + typed relationships) |
| **Auditability** | Git-tracked markdown | SQLite (git-unfriendly) |
| **Offline** | Ano | Ano |
| **RAM** | 0 (soubory) | ~6 MB |
| **Cross-project** | Ne (per-project) | Ano (container tags, projects) |
| **Token budget** | Ne (vrací vše z grepu) | Ano (default 8000) |
| **Dashboard** | Ne | Ano (3D WebGL graph) |
| **Claude Code integration** | Native (hooks, auto-memory) | MCP server (vyžaduje konfiguraci) |
| **Human readable** | Ano (markdown) | Ne (SQLite binary) |
| **Git friendly** | Ano | Ne |

## Klíčové výhody sabmemory

### 1. Knowledge Graph
Entities s typovanými vztahy (person, org, device, concept) + bidirectional links.
STOPA nemá entity model — memories jsou flat soubory bez strukturovaných vztahů.

### 2. Token-budgeted search
Výsledky omezeny token budgetem → nikdy nepřetečeme kontext.
Naše grep vrací vše bez limitu.

### 3. Auto-linking a BM25 ranking
FTS5 automaticky propojuje related memories při zápisu.
BM25 + importance score = lepší ranking než plain grep.

### 4. Memory versioning chains
`updates`/`extends`/`derives` — jen latest verze v search results.
STOPA: append-only, staré záznamy zůstávají viditelné.

### 5. Auto-forget s expiry
Nastavíš datum expirace → automaticky zmizí z vyhledávání.
STOPA: manuální maintenance (pravidlo "90 dní → ověřit").

### 6. Container scoping + Projects
Namespace izolace mezi projekty. Cross-project search.
STOPA: izolované per-project directories, žádný cross-project search.

## Klíčové nevýhody pro STOPA

### 1. Git-unfriendly
SQLite binární soubor nelze smysluplně diffovat/mergovat v gitu.
STOPA memory je git-tracked markdown — plný audit trail, code review, branching.

### 2. Žádná sémantická search
FTS5 je keyword-based, ne embedding-based. Nenajde "automobile" při hledání "car".
To je stejné omezení jako náš grep — jen s lepším rankingem.

### 3. Tool overload (49 tools)
Každý tool zabírá kontext window. 49 tool descriptions = ~3000-5000 tokenů overhead per session.
STOPA memory: 0 tokenů overhead (soubory, ne MCP tools).

### 4. Rust dependency
Build vyžaduje Rust 1.70+. Na Windows s `cargo build` potenciálně problémy.
Pre-built binaries pro Windows nejsou k dispozici (nový projekt, 2026-03-09).

### 5. Duplicitní systém
Claude Code už má native auto-memory (MEMORY.md). Přidáním sabmemory máme 2 memory systémy
které si navzájem nevidí a potenciálně se rozcházejí.

### 6. Dashboard je hezký ale zbytečný
3D WebGL knowledge graph vypadá cool, ale pro 50-100 orchestračních memories
je MEMORY.md index přehlednější a rychlejší.

## Doporučení

### Verdikt: NEADOPTOVAT jako celek

sabmemory je skvělý projekt, ale pro STOPA přináší víc komplikací než hodnoty:
- Naše memory systém je git-friendly, human-readable, zero-overhead
- Duplicitní memory systém = split-brain problém
- 49 tools = kontext bloat
- FTS5 není sémanticky lepší než grep pro naše atomic notes

### Adoptovat VZORY (inspirace bez dependency)

| Vzor ze sabmemory | Implementace v STOPA | Priorita | Effort |
|---|---|---|---|
| **Token-budgeted search** | Omezit grep výsledky na N řádků/tokenů v memory-brief.sh | Střední | Nízký |
| **Auto-forget/expiry** | Přidat `expires: YYYY-MM-DD` do YAML frontmatter learnings; maintenance hook je auto-archivuje | Nízká | Nízký |
| **Importance scoring** | Přidat `importance: 1-10` do YAML frontmatter; grep-first pak seřadí | Nízká | Střední |
| **Memory versioning** | Přidat `supersedes: <filename>` do frontmatter; starý soubor archivovat | Nízká | Nízký |
| **Container/project scoping** | Už máme (per-project `.claude/memory/`) | — | — |
| **Knowledge graph** | Není potřeba pro naši velikost (<200 memories) | — | — |

### Kdy přehodnotit

Sabmemory adoptovat pokud:
1. Memory soubory přerostou 500+ a grep je pomalý (zatím ~50)
2. Potřebujeme cross-project memory search (zatím ne)
3. Potřebujeme entity relationships (zatím nepotřebujeme)
4. Windows pre-built binaries budou dostupné

### Alternativní cesta: Vlastní SQLite FTS5

Pokud by grep přestal stačit, jednodušší varianta než adoptovat sabmemory:
- Python script s `sqlite3` FTS5 (built-in v Pythonu)
- Indexuje existující markdown memory soubory
- Zachová git-friendly markdown jako primary storage
- SQLite jen jako search index (regenerovatelný)
- ~50 řádků kódu vs 49-tool MCP server

## Shrnutí

sabmemory je technicky solidní (Rust, 6 MB RAM, 49 tools, knowledge graph).
Pro STOPA je ale overkill — naše markdown-based memory s grep-first retrieval
je jednodušší, auditovatelná, git-friendly a pro naši škálu (~50-200 memories) plně dostačující.

Adoptovat vzory (token budget, expiry, importance), ne nástroj.
