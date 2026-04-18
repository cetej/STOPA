---
date: 2026-04-13
topic: Karpathy LLM Wiki / Second Brain Architecture
researcher: claude-sonnet-4-6
tool_calls_budget: 8
tool_calls_used: 5
---

## Evidence Table

| # | Source | URL | Key claim | Type | Confidence |
|---|--------|-----|-----------|------|------------|
| 1 | Karpathy — LLM Wiki GitHub Gist | https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f | Three-layer architecture (raw/ wiki/ schema), compiler analogy, index-first retrieval, persistent compounding artifact | RELEVANT | high |
| 2 | VentureBeat — LLM Knowledge Base Architecture | https://venturebeat.com/data/karpathy-shares-llm-knowledge-base-architecture-that-bypasses-rag-with-an | Three-stage ingest→compile→maintain, bypasses RAG via structured text + explicit backlinks, multi-agent Quality Gate | RELEVANT | high |
| 3 | MindStudio — Compiler Analogy Breakdown | https://www.mindstudio.ai/blog/karpathy-llm-knowledge-base-compiler-analogy | Source code = raw articles, compiler = LLM, executable = wiki; lossy compression framing; 4-pass transformation | RELEVANT | high |
| 4 | Camp Pedersen — LLM OS | https://campedersen.com/llm-os | Context window as RAM, LLM as OS kernel, tools as userland extensions, MemGPT context management | PARTIAL | medium |

---

## Findings

### Architektura: tři vrstvy

Karpathyho systém je postaven na třech oddělených vrstvách [1]:

**raw/** — neměnný archiv zdrojů (články, papery, obrázky, datasety). LLM čte, nikdy nepíše.

**wiki/** — kompilovaný, strukturovaný artefakt. LLM-generované Markdown soubory organizované podle entit, konceptů a syntéz. Tato vrstva se akumuluje a rozrůstá s každým ingestem.

**schema** — konfigurační dokument (např. `CLAUDE.md`), který definuje strukturu, konvence a workflow. Evolve ho člověk i LLM dohromady.

### Compiler Analogy

Analogie se softwarovou kompilací [1][3]:

- **Source code** = raw články, papery, poznámky, webové stránky
- **Compiler** = LLM
- **Compiled binary/executable** = wiki (syntézovaný, navigovatelný artefakt)

Klíčová myšlenka: "compiled once and then kept current, not re-derived on every query." Raw zdroje jsou verbose, redundantní, plné kontextového šumu irelevantního pro konzumaci. Kompilační krok odstraňuje duplicitu, řeší kontradikce a produkuje koherentní celek, který jednotlivé zdroje samy o sobě nemohou dosáhnout [3].

LLM je frámován jako "lossy compression" — specificky váš zdrojový materiál, prioritizuje užitečnost nad dokonalou věrností zdroji [3].

### Workflow: Capture → Compile → Maintain

**Ingest flow** [1]:
> "The LLM reads the source, discusses key takeaways with you, writes a summary page in the wiki, updates the index, updates relevant entity and concept pages across the wiki, and appends an entry to the log."

Jeden zdroj může dotknout 10–15 wiki stránek. Kompilační průchod sestává ze 4 kroků [3]:
1. Extraction — identifikace klíčových konceptů z jednotlivých zdrojů
2. Synthesis — kombinace informací napříč zdroji + řešení kontradikcí
3. Structure — organizace do navigovatelného formátu
4. Refinement — iterativní průchody zvyšující koherenci

**Query flow** [1]: LLM prohledá relevantní stránky, syntetizuje odpovědi s citacemi, hodnotné výstupy (srovnání, analýzy) uloží zpět do wiki jako nové stránky.

**Maintenance/Lint** [1][2]: Periodické health checks identifikují kontradikce, zastaralá tvrzení, osiřelé stránky, chybějící cross-reference a datové mezery. Systém se "sám léčí" — continuous LLM passes automaticky zlepšují datovou kvalitu.

### Proč to bypasuje RAG

Na rozdíl od RAG systémů, které při každém dotazu znovu prohledávají vektorizované embeddingy, wiki udržuje syntézu explicitně [1][2]:

- **Index-first retrieval**: Strukturovaný Markdown index překonává embedding-based RAG při cca 100 zdrojích / 400 000 slovech. Žádná vektorová infrastruktura, lidsky čitelné.
- **Explicit connections**: Backlinky a indexy nahrazují semantic similarity matching.
- **No re-derivation**: "The cross-references are already there" — wiki je persistent compounding artifact.
- **Human-readable source of truth**: Markdown soubory jsou traceable a auditovatelné, žádný "black box" problem vektorových embeddingů.

### Context Engineering principy

**Persistent over ephemeral** [1]: Wiki přežívá context compaction; ephemeral chat history ne. Indexy udržovat chirurgicky malé — plný obsah žije v separátních typed souborech, načítá se on-demand.

**Index.md** (content-oriented): Katalog všech wiki stránek s linky, one-line summary a metadaty. Organizovaný po kategoriích. LLM čte jako první při odpovídání na dotazy.

**Log.md** (chronological): Append-only záznam ingestů, dotazů a lint průchodů. Umožňuje grepovat nedávnou aktivitu a sledovat evoluci wiki.

**Structured naming replaces infrastructure** [1]: File naming conventions (prefixy jako `user_`, `feedback_`, `project_`) routují LLM writes bez vector databází nebo složité retrieval logiky.

**Contradiction flagging** [1]: Nové zdroje konfliktní s existujícími stránkami vytvoří `[!contradiction]` callout, místo tichého přepisování.

### Human-LLM Division of Labor

> "The human's job is to curate sources, direct the analysis, ask good questions, and think about what it all means. The LLM's job is everything else." [1]

Klíčový insight [1]:
> "The tedious part of maintaining a knowledge base is not the reading or the thinking — it's the bookkeeping...LLMs don't get bored, don't forget to update a cross-reference, and can touch 15 files in one pass."

Lidé zůstávají decision-makers. LLM řeší maintenance, který zabíjí human-managed wikis nudou a nekonzistencí.

Byznys frámování z komunity [2]:
> "Every business has a raw/ directory. Nobody's ever compiled it. That's the product."

### Historická resonance

Karpathy propojuje vzor s Vannevar Bushovou *Memex* (1945) — personalizovaný, kurátorský knowledge store s asociativními trasami mezi dokumenty [1]. Bushova vize byla blíž tomuto modelu než se stal otevřený web: "private, actively curated, with the connections between documents as valuable as the documents themselves."

LLM řeší Bushův nevyřešený problém: kdo udržuje ty konekce? Odpověď: neúnavná AI.

### LLM OS kontext (doplňující)

Z LLM OS perspektivy [4]: kontext window jako RAM (omezený resource vyžadující inteligentní management), LLM jako OS kernel, nástroje jako userland extensions. MemGPT abstracts away from chat interface tím, že tratuje user input jako event — strategicky řídí co zůstává v kontextu.

### Technické detaily implementace

- Žádný vendor lock-in: plain Markdown soubory, git-tracked, přenositelné napříč LLM platformami [1]
- Volitelný tooling: Obsidian pro vizualizaci, qmd (BM25/vector search) pro škálování, Marp pro prezentace [1]
- Typed files: naming conventions snižují potřebu explicitních routing instrukcí [1]
- Obsidian Web Clipper pro konverzi webového obsahu do Markdown [2]
- Škáluje na 10-agent systémy s "Quality Gate" (Hermes model validuje výstupy před vstupem do live wiki) [2]
- Pro start: "Master one knowledge domain before expanding" [3]

---

## Sources

1. Karpathy — LLM Wiki GitHub Gist — https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
2. VentureBeat — "Karpathy shares LLM knowledge base architecture that bypasses RAG" — https://venturebeat.com/data/karpathy-shares-llm-knowledge-base-architecture-that-bypasses-rag-with-an
3. MindStudio Blog — "Karpathy LLM Knowledge Base: Compiler Analogy" — https://www.mindstudio.ai/blog/karpathy-llm-knowledge-base-compiler-analogy
4. Camp Pedersen — "LLM OS" — https://campedersen.com/llm-os

---

## Coverage Status

Tool calls used: 5/8
Remaining budget: 3 calls

### Coverage assessment

- [x] Three-layer architecture (raw/wiki/schema) — COVERED (high confidence, source 1)
- [x] Compiler analogy (source code → binary) — COVERED (high confidence, sources 1+3)
- [x] Workflow capture→compile→maintain — COVERED (high confidence, sources 1+2+3)
- [x] Context engineering principles — COVERED (high confidence, source 1)
- [x] Why it bypasses RAG — COVERED (high confidence, sources 1+2)
- [x] Human-LLM division of labor — COVERED (high confidence, source 1)
- [x] Historical framing (Memex) — COVERED (medium confidence, source 1)
- [x] LLM OS / memory-as-tools — PARTIAL (source 4 was tangential — covers OS vision, not second brain specifics)
- [ ] Direct Karpathy quotes from original gist — not available (Jina reader extracted summary, not verbatim gist text)

### Gaps

- Verbatim quotes from original gist not confirmed — Jina reader may have paraphrased
- LLM OS connection to second brain is thematic, not direct Karpathy statement
- Multi-agent Quality Gate detail (source 2) is community extension, not necessarily Karpathy's own design
