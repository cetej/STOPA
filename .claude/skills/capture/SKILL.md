---
name: capture
description: "Use when capturing an idea, source, thought pattern, or reasoning model into 2BRAIN. Trigger on 'capture', 'zapamatuj si', 'ulož do mozku', 'brain capture', 'nový nápad'. Do NOT use for STOPA learnings (/scribe) or project decisions (/scribe)."
user-invocable: true
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash", "WebFetch", "Agent", "TodoWrite"]
permission-tier: workspace-write
phase: build
tags: [memory, documentation, pkm]
discovery-keywords: [idea, nápad, thought, myšlenka, source, zdroj, mental model, reasoning, second brain, knowledge, znalost]
input-contract: "user → text/URL/idea description → non-empty"
output-contract: "URL: řádek v inbox.md NEBO wiki article + graph update + timeline entry → brain/ directory"
---

# /capture — Quick Entry into 2BRAIN

Rychlý vstup podle typu: URL → fronta pro asynchronní zpracování, text/myšlenka → okamžitě do wiki.

## Workflow

### Phase 1: Classify Input

Rozpoznej typ vstupu a zvol cestu:

| Input | Cesta | Důvod |
|-------|-------|-------|
| **URL** | Append do `inbox.md` → STOP | Fetch + kompilace je pomalá, brain-ingest udělá dávkově |
| **Text/myšlenka** | Přímá kompilace do wiki/ | Kontext je horký, nemůže čekat |
| **Screenshot/soubor** | Přímá kompilace do wiki/ | Máš otevřený kontext, zpracuj hned |
| **Existující STOPA learning** | Cross-link do brain/, nekopírovat | Duplikace poškozuje konzistenci |

**Pokud URL:**
1. Přečti `C:\Users\stock\Documents\000_NGM\STOPA\.claude\memory\brain\inbox.md`
2. Vlož řádek `URL: <url>` do sekce `## Queue`
3. Uložit soubor
4. Reportuj uživateli: "Přidáno do fronty. brain-ingest zpracuje při příštím spuštění."
5. STOP — nepokračuj do Phase 2

### Phase 2: Capture to raw/

1. Vytvoř soubor v `brain/raw/` s timestampem: `YYYY-MM-DD-<slug>.md`
2. Obsah: originální text nebo fetchnutý obsah
3. YAML frontmatter: `date`, `source_type` (url|text|file), `source_url` (pokud existuje)

### Phase 3: Compile to wiki/

Aplikuj Karpathyho compiler analogy — 4-pass transformation:

1. **Extraction**: Identifikuj klíčové koncepty, entity, reasoning patterns
2. **Synthesis**: Kombinuj s existujícími wiki články (čti related přes knowledge-graph.json)
3. **Structure**: Vytvoř/aktualizuj wiki článek(y) v příslušné kategorii:
   - `concepts/` — abstraktní koncepty, frameworks, technologie
   - `people/` — osoby, influenceři, mentoři
   - `projects/` — projekty, iniciativy
   - `reasoning/` — mentální modely, způsoby uvažování, heuristiky
4. **Refinement**: Aktualizuj cross-references ve wiki článcích (Related: [[...]])

### Phase 4: Connect

1. Přečti `brain/knowledge-graph.json`
2. Přidej nové nodes pro nové entity
3. Přidej edges pro vztahy (created, inspired, enables, contradicts...)
4. Ulož zpět

### Phase 5: Index & Log

1. Aktualizuj `brain/wiki/index.md` — přidej nový článek do tabulky
2. Append do `brain/wiki/log.md` — chronologický záznam
3. Append do `brain/timeline.md` — event entry

### Phase 6: Report

Vypiš uživateli:
- Co bylo zachyceno (1 věta)
- Které wiki články byly vytvořeny/aktualizovány
- Které nové connections vznikly v grafu

## Rozhodovací pravidla

- **Nový koncept** (neexistuje v wiki/): vytvoř nový článek
- **Existující koncept** (už je v wiki/): AKTUALIZUJ existující článek — přidej nové informace, aktualizuj Related
- **Kontradikce** s existujícím článkem: přidej `[!contradiction]` callout do článku, NEPŘEPISUJ
- **STOPA learning**: cross-link (`Related: → .claude/memory/learnings/...`), nekopíruj obsah

## Anti-Rationalization Defense

| Rationalization | Why Wrong | Do Instead |
|---|---|---|
| "Tohle je moc krátké na wiki článek" | I jedna věta může být atomic note (Zettelkasten) | Vytvoř krátký článek s 2-3 větami |
| "Přeskočím graph update, je to zbytečné" | Graph je retrieval backbone — bez edges ztratíš connections | Vždy přidej alespoň 1 edge |
| "Existující článek je dobrý, nebudu měnit" | Nový zdroj může obohatit nebo rozporovat | Vždy porovnej a aktualizuj |

## Red Flags

STOP and re-evaluate if:
- Vytváříš article bez jediného Related linku
- Kopíruješ celý raw text do wiki/ bez compression
- Přeskakuješ Phase 4 (Connect) — graph update

## Verification Checklist

- [ ] raw/ soubor existuje s YAML frontmatter
- [ ] Wiki článek existuje v příslušné kategorii
- [ ] index.md obsahuje nový záznam
- [ ] log.md má append entry
- [ ] knowledge-graph.json má nový node/edge
- [ ] timeline.md má event entry
