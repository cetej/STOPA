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

## Implementace v 2BRAIN

2BRAIN přímo implementuje tento vzor:
- `brain/raw/` = Raw Sources
- `brain/wiki/` = The Wiki
- `CLAUDE.md` + skill `/capture` = The Schema + operace
