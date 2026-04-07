# Second Brain Gap Analysis — STOPA Knowledge Compounding

> Analýza tří identifikovaných mezer v STOPA knowledge systému
> inspirovaná Spisak/Karpathy Second Brain pattern.
> Datum: 2026-04-07

## Stav dnes

STOPA má sofistikovaný memory systém:
- **51 learnings** s YAML metadaty, confidence tracking, decay
- **9 wiki článků** generovaných `/compile` s citacemi a health score
- **concept-graph.json** (547 KB) — spreading activation, Hebbian edges
- **3-signálový retrieval** — grep + BM25 + graph walk přes RRF fusion
- **Write-time gating** — salience gate filtruje šum při zápisu

Ale: **60 research výstupů** + **83 sub-research souborů** v `outputs/` leží mimo memory graf. Jsou to mrtvá data — systém je nikdy nekonzultuje, neindexuje, nepropojuje.

---

## Gap 1: Ingest Pipeline (raw source → structured knowledge)

### Problém

STOPA nemá systematický proces pro zpracování externích zdrojů do memory grafu:

| Vstup | Co se stane dnes | Co by mělo |
|-------|-----------------|------------|
| `/fetch` URL | Vrátí čistý text → stdout | Extrahovat entity, uložit source summary |
| `/deepresearch` | Report do `outputs/` | Extrahovat klíčová zjištění → learnings + entity pages |
| `/watch` finding | Řádek v `news.md` | Propojit s concept-graph, sledovat vývoj entity |
| `/radar` tool | Řádek v `radar.md` | Vytvořit entity page s historií verzí |
| Článek/paper | Manuální `/scribe` | Auto-extraction claims → cross-ref s existujícími |

Výsledek: znalosti se ztrácí. Research za $2-5 skončí jako soubor, který nikdo nečte.

### Návrh: `/ingest` skill

**Účel:** Zpracovat raw zdroj (URL, soubor, research output) do strukturovaných memory artefaktů.

**Pipeline (4 fáze):**

```
Raw Source → Extract → Cross-Reference → Store
     ↓           ↓            ↓              ↓
  fetch/read   entities    concept-graph   learnings/
               claims      wiki updates    wiki/sources/
               metadata    related links   entity pages
```

**Fáze 1 — Normalize:**
- Vstup: URL → `/fetch`, soubor → `Read`, research output → přečíst `outputs/*.md`
- Výstup: čistý text + metadata (autor, datum, URL, typ zdroje)

**Fáze 2 — Extract (Haiku sub-agent):**
- **Entity extraction:** osoby, nástroje, knihovny, společnosti, koncepty
  - Formát: `{name, type: person|tool|company|concept|paper, description, first_seen}`
- **Claim extraction:** klíčová tvrzení s evidence level
  - Formát: `{claim, evidence: verified|inferred|single-source, source_url}`
- **Relation extraction:** vztahy mezi entitami
  - Formát: `{entity_a, relation: uses|competes|extends|contradicts, entity_b}`
- Max 15 entit, 10 claims, 10 relací per zdroj (prevent bloat)

**Fáze 3 — Cross-Reference:**
- Grep existující learnings/wiki pro každou extrahovanou entitu
- Detekce: nová entita vs. update existující vs. kontradikce
- Aktualizace concept-graph.json: nové entity nodes + edges
- Identifikace related learnings pro `related:` field

**Fáze 4 — Store:**
- Source summary → `.claude/memory/wiki/sources/<slug>.md` (max 80 řádků)
- Nové/aktualizované entity pages → `.claude/memory/wiki/entities/<name>.md`
- Extrahované learnings (pokud projdou salience gate) → `.claude/memory/learnings/`
- Index update → wiki/INDEX.md

**Rozhodnutí k implementaci:**

| Otázka | Doporučení | Alternativa |
|--------|-----------|-------------|
| Kde entity pages? | `wiki/entities/` (nová složka) | Inline v existujících wiki článcích |
| LLM pro extraction? | Haiku sub-agent (levný, dostatečný) | Regex-only (omezené, ale deterministické) |
| Automaticky po `/deepresearch`? | Ano, opt-out `--no-ingest` | Manuální trigger (konzervativnější) |
| Backfill existujících 60 outputs? | Batch ingest v samostatném session | Ingestovat jen nové od teď |

**Effort:** ~400 řádků skill + 100 řádků helper. 1 session na implementaci, 1 na backfill.

---

## Gap 2: Synthesis Feedback Loop (query → knowledge)

### Problém

`/deepresearch` generuje hodnotné výstupy (průměr ~15 KB per report), ale:
- Výstupy jdou do `outputs/` — **mimo memory graf**
- Žádná automatická extrakce learnings
- Žádná aktualizace concept-graph
- Žádné propojení s existujícími wiki články
- `/compile` pracuje jen s `learnings/`, ne s `outputs/`

60 research reportů × ~15 KB = **~900 KB nevyužitých znalostí**.

### Návrh: Research → Memory Bridge

**Dvě úrovně integrace:**

**Úroveň A — Automatická (po každém `/deepresearch`):**
1. Po dokončení research reportu automaticky spustit ingest pipeline (Gap 1)
2. Extrahovat 3-5 top learnings z research závěrů
3. Aktualizovat concept-graph novými entitami z reportu
4. Přidat source page do `wiki/sources/`
5. Cross-referencovat s existujícími wiki články

Implementace: hook na konci `/deepresearch` workflow → volá `/ingest` na output soubor.

**Úroveň B — Periodická syntéza (nový `/compile` mód):**
1. Rozšířit `/compile` o skenování `outputs/` (ne jen `learnings/`)
2. Cluster research reporty podle tématu (existující Jaccard clustering)
3. Generovat synthesis pages: "Co říkají 4 research reporty o agent memory?"
4. Tyto synthesis pages jsou nové wiki články s cross-referencemi
5. Detekce kontradikce mezi research výstupy

Implementace: nová fáze v `/compile` — Phase 7.8 "Research Synthesis Bridge"

**Compounding efekt:**
```
Research 1: agent memory → 3 learnings + entity pages
Research 2: agent teams  → 4 learnings + entity updates
                    ↓
Compile: detekuje overlap → synthesis article
"Agent Memory vs Team Coordination — shared patterns"
                    ↓
Research 3: dotaz na memory → retrieval najde synthesis
→ research je LEPŠÍ protože staví na předchozích
```

**Rozhodnutí k implementaci:**

| Otázka | Doporučení | Alternativa |
|--------|-----------|-------------|
| Auto-ingest po deepresearch? | Ano (default on) | Opt-in `--ingest` flag |
| Compile skenuje outputs/? | Jen s `--include-research` flag | Vždy (rizikovější, outputs velké) |
| Backfill 60 existujících? | Batch po implementaci Gap 1 | Ingestovat jen top 20 (podle velikosti/relevance) |

**Effort:** Úroveň A = modifikace `/deepresearch` (50 řádků) + závislost na `/ingest`. Úroveň B = nová fáze v `/compile` (~150 řádků).

---

## Gap 3: Knowledge Graph Visualization

### Problém

`concept-graph.json` (547 KB, stovky entit a edges) je silný datový zdroj, ale:
- Viditelný jen jako raw JSON
- Žádná vizualizace propojení
- Žádný způsob jak "procházet" graf interaktivně
- Wiki články mají textové cross-reference, ale ne grafový pohled

### Návrh: Dvě cesty

**Cesta A — Obsidian export (read-only viewer):**
- Skript `export-to-obsidian.py`: konvertuje wiki/ + learnings/ + concept-graph na Obsidian vault
- Backlinks přes `[[wiki links]]` syntax
- Obsidian graph view automaticky vizualizuje propojení
- Jednosměrný export (STOPA = source of truth, Obsidian = viewer)
- **Pro:** okamžitě použitelné, zero custom code pro vizualizaci
- **Proti:** duplicitní data, manuální re-export

**Cesta B — Interaktivní HTML graf (standalone):**
- Skript generuje `knowledge-graph.html` z concept-graph.json
- D3.js force-directed layout nebo Cytoscape.js
- Filtrování podle entity type, recency, activation level
- Click na node → zobrazí learning snippety
- **Pro:** žádná závislost na Obsidian, otevře se v browseru
- **Proti:** custom vývoj (~300 řádků HTML/JS)

**Cesta C — Hybrid (doporučuji):**
- `/compile` generuje statický `wiki/GRAPH.md` s ASCII/mermaid vizualizací top 30 konceptů
- Volitelný `--html` flag generuje interaktivní D3.js verzi
- Obsidian export jako separátní utility (ne core workflow)

**Rozhodnutí k implementaci:**

| Otázka | Doporučení | Alternativa |
|--------|-----------|-------------|
| Primary viewer? | HTML graf (Cesta B) | Obsidian export (Cesta A) |
| Integrovat do /compile? | Ano, jako Phase 9 | Separátní skript |
| Mermaid jako fallback? | Ano (top 20 nodes, textový) | Jen HTML |

**Effort:** Cesta B = ~300 řádků HTML/JS template + 50 řádků Python generátor. Cesta A = ~150 řádků export skript. Cesta C = ~200 řádků celkem.

---

## Implementační Roadmap

### Fáze 1: `/ingest` skill (základ pro vše ostatní)
- **Scope:** Nový skill, entity extraction, source pages, concept-graph update
- **Závislosti:** žádné (staví na existující infra)
- **Effort:** 1 session
- **Dopad:** Každý nový zdroj automaticky obohacuje knowledge graf

### Fáze 2: Research → Memory Bridge
- **Scope:** Hook na konci `/deepresearch`, auto-ingest výstupů
- **Závislosti:** Fáze 1
- **Effort:** 0.5 session
- **Dopad:** 60 existujících + všechny budoucí research výstupy kompoundují

### Fáze 3: Backfill existujících outputs
- **Scope:** Batch ingest top 20-30 research reportů
- **Závislosti:** Fáze 1
- **Effort:** 1 session (batch, většinou automated)
- **Dopad:** Okamžité obohacení grafu o ~450 KB znalostí

### Fáze 4: Knowledge Graph Visualization
- **Scope:** HTML interaktivní graf + mermaid fallback v compile
- **Závislosti:** Fáze 1 (entity pages dávají grafu víc obsahu)
- **Effort:** 0.5 session
- **Dopad:** Vizuální procházení znalostní báze

### Fáze 5: Compile rozšíření (research synthesis)
- **Scope:** `/compile --include-research` mód
- **Závislosti:** Fáze 1-3 (potřebuje ingestované outputs)
- **Effort:** 0.5 session
- **Dopad:** Cross-research synthesis articles (nejvyšší compounding hodnota)

---

## Metriky úspěchu

| Metrika | Baseline (dnes) | Cíl po implementaci |
|---------|----------------|---------------------|
| Outputs propojené s memory grafem | 0/60 (0%) | 30+/60 (50%+) |
| Entity pages v wiki | 0 | 50+ |
| Concept-graph entity count | ~200 | 400+ |
| Retrieval hit rate (query → relevant result) | neměřeno | měřit přes uses/successful_uses |
| Wiki health score | 7/10 | 8+/10 |
| Research compounding (research N cites research N-1) | 0% | tracking zavést |

---

## Rizika

| Riziko | Mitigace |
|--------|---------|
| Entity bloat (příliš mnoho low-value entit) | Max 15 entit per ingest + salience gate |
| Stale entity pages | Decay stejný jako learnings (confidence -0.1 per 30 dní neaktivity) |
| Hallucinated cross-references | Haiku extractor + grep verification (entity musí existovat) |
| Token cost ingest pipeline | Haiku extraction (~$0.02 per source), amortizuje se přes lepší retrieval |
| Concept-graph size explosion | Prune edges < 0.05 weight (existující optimize_graph) |
