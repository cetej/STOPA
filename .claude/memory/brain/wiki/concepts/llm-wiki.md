# LLM Wiki Pattern

**Type:** concept
**Tags:** ai, pkm, architecture, knowledge-management
**Related:** [[karpathy]], [[compiler-analogy]], [[context-engineering]], [[second-brain]], [[two-generators]]
**Source:** https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

---

Architektonický vzor od Karpathyho: LLM inkrement buduje a udržuje strukturovanou markdown wiki místo re-derivování znalostí při každém dotazu (RAG).

## Tři vrstvy

| Vrstva | Vlastník | Popis |
|--------|----------|-------|
| **raw/** | Člověk | Neměnné kuratované zdroje. LLM čte, nikdy nepíše. |
| **wiki/** | LLM | Kompilované markdown soubory: summaries, entity pages, concept pages, comparisons, synthesis. |
| **schema** | Oba | Konfigurační dokument (CLAUDE.md) definující strukturu, konvence, workflow. Ko-evoluce. |

## Tři operace

### Ingest
Nový zdroj → LLM diskutuje klíčové poznatky → píše summary → aktualizuje index → reviduje relevantní entity/concept pages. Jeden zdroj může dotknout 10-15 wiki stránek.

### Query
Dotaz na wiki → LLM prohledá relevantní stránky → syntetizuje odpověď s citacemi → hodnotné výstupy uloží zpět jako nové stránky.

### Lint
Periodický health check: kontradikce, stale tvrzení, osiřelé stránky, chybějící cross-reference, datové mezery.

## Klíčové soubory

- **index.md** — content-oriented katalog po kategoriích, s linky a one-line summary. Aktualizuje se při každém ingestu.
- **log.md** — append-only chronologický záznam ingestů, dotazů a lint průchodů.

## Proč bypasuje RAG

Při ~100 zdrojích / 400K slovech structured markdown index překonává embedding-based RAG:
- Žádná vektorová infrastruktura
- Lidsky čitelné, auditovatelné
- Cross-reference jsou "already there" — ne dynamicky hledané

## Dělba práce

Člověk: kuratuje zdroje, řídí analýzu, ptá se, přemýšlí o smyslu.
LLM: vše ostatní — cross-referencing, consistency maintenance, contradiction flagging.

## Přesnější 3-složková architektura (CoderSera, Apr 2026)

| Složka | Role | Pravidla |
|--------|------|---------|
| **raw/** | Append-only zdrojový repozitář | PDF, články, screenshoty → markdown. LLM pouze čte. |
| **wiki/** | LLM output — strukturované wiki | Interlinked markdown + index.md |
| **outputs/** | Persistentní výstupy dotazů | Auditovatelné syntetizované reporty |

## Token Economy Shift (Karpathy, Apr 2026)

Token consumption se přesouvá od **"operating code"** k **"operating knowledge"**. LLM apps vrstva migrace: code generation → knowledge management. Hodnota je v akumulované strukturované znalosti, ne v generativním throughput.

**Hippocampus analogie:** LLM jako hippocampus — konsoliduje short-term observations do long-term knowledge structures. Nekopíruje raw zážitky, extrahuje patterns a ukládá je strukturovaně.

## Proč LLM Wiki překonává manuální systémy

Zettelkasten / Obsidian selhávají protože "bookkeeping burden — updating cross-references, tagging, and noting contradictions — grows much faster than the value" (EvoAI Labs, Apr 2026).

LLM Wiki automatizuje tuto vrstvu: AI je "tireless librarian and system maintainer".

## Limity škálování

- ~few hundred articles před context window constraints
- Token cost roste s scale (každý Lint = celý index)
- Human oversight nutný pro fact-checking
- Žádný real-time retrieval pro concurrent multi-user access

## Implementace v 2BRAIN

2BRAIN přímo implementuje tento vzor:
- `brain/raw/` = Raw Sources
- `brain/wiki/` = The Wiki (+ `brain/wiki/outputs/` pro dotazy)
- `CLAUDE.md` + skill `/capture` = The Schema + operace

**Validace taxonomií:** Write-Manage-Read loop (arXiv:2603.07670) formalizuje 2BRAIN cyklus jako Hierarchical Virtual Context paměťový mechanismus — akademicky nejtěsněji odpovídající architektuře.
