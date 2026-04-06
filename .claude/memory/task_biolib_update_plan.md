# BIOLIB — plán pravidelné aktualizace databází

## Kontext (aktualizováno 2026-03-30)

Po velkém rozšíření (2026-03-30) máme:

| DB | Umístění | Velikost | Termínů | Účel |
|----|----------|----------|---------|------|
| **termdb.db** | BIOLIB/ | 747 MB | **1,439,718** | Jediný lookup zdroj pro NG-ROBOT + ADOBE-AUTOMAT |
| **species_names.db** | BIOLIB/ | 87 MB | 218K taxonů | Taxonomická metadata (rank, wikidata, sources, verified) |

### Rozložení termínů v termdb.db

| Domain | Count | Zdroj | Licence |
|--------|-------|-------|---------|
| derivation | 1,035,553 | DeriNet 2.2 (LINDAT) | CC BY-NC-SA 4.0 |
| biology | 218,835 | Wikidata + iNaturalist + BioLib | mixed |
| foreign_words | 69,795 | Kaikki.org (EN Wiktionary CZ) | CC BY-SA |
| encyclopedia | 66,559 | Czech Wiktionary dump | CC BY-SA 4.0 |
| geography | 41,490 | Wikidata + OpenStreetMap | mixed + ODbL |
| chemistry | 4,020 | Wikidata | CC0 |
| medicine | 2,800 | Wikidata/MeSH | CC0 |
| general | 442 | Phase 3 enrichment | — |
| astronomy | 126 | Wikidata | CC0 |
| geology | 68 | Wikidata | CC0 |

## Pravidelný sync cyklus

| Frekvence | Zdroj | Importer | Příští run |
|-----------|-------|----------|------------|
| Měsíčně | Kaikki.org delta | `importers.kaikki_wiktionary` | 2026-04-29 |
| Kvartálně | Czech Wiktionary dump | `importers.cswiktionary` | 2026-06-28 |
| Ročně | DeriNet 2.x | `importers.derinet` | 2027-03-30 |
| Pololetně | OSM Czech Republic | `importers.osm_places` | 2026-09-26 |
| Měsíčně | Wikidata species | `importers.biology_wikidata` | TBD |

Stav syncu: `BIOLIB/data/last_sync.json`
Orchestrátor: `python -m importers.sync_scheduler --check`

## Implementované importéry (2026-03-30)

| Soubor | Doména | Zdroj |
|--------|--------|-------|
| `importers/kaikki_wiktionary.py` | foreign_words | kaikki.org JSONL |
| `importers/cswiktionary.py` | encyclopedia | MediaWiki XML dump |
| `importers/derinet.py` | derivation | DeriNet 2.2 TSV |
| `importers/osm_places.py` | geography | Overpass API |
| `importers/morfflex.py` | inflections | MorfFlex TSV (PREPARED, not yet run) |
| `importers/czech_wordnet.py` | synonym | Czech WordNet XML (BLOCKED: no download) |
| `importers/sync_scheduler.py` | — | Orchestrátor se state tracking |

## Nedokončené / odložené

### MorfFlex CZ 2.1 (inflections tabulka)
- 127M trojic lemma→tvar→tag, 6GB uncompressed
- Importer `importers/morfflex.py` hotový, jen potřeba stáhnout data
- Download: https://lindat.mff.cuni.cz/ (DSpace 7 API, bitstream endpoint)
- Použitelné pro fuzzy matching (zadaný skloněný tvar → nalezení lemma)

### Czech WordNet 1.9
- LINDAT download 404 — soubor pravděpodobně odstraněn
- OMW (Open Multilingual Wordnet) 1.4 nemá češtinu
- Alternativa: `wn` Python package, ale české lexicon chybí
- STATUS: BLOCKED — čekat na nové vydání nebo kontaktovat UFAL

## Otevřené otázky

### 1. Inkrementální sync species_names.db → termdb.db
- Aktuálně merge script jednorázový
- Potřeba: delta sync (jen nové/změněné)

### 2. Data quality
- Některé CZ překlady v plurálu místo singuláru
- Duplicity mezi doménami (slovo může být v foreign_words i derivation)

### 3. Distribuce
- ~/.ngm/ symlinks pro portabilitu
- Env var `NGM_MULTI_DOMAIN_DB`

### 4. KARTOGRAF integrace
- geography doména nyní obsahuje 41K termínů — připraveno pro lokalizaci map
