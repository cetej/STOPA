---
date: 2026-04-28
type: bug_fix
severity: high
component: pipeline
tags: [translation, termdb, species, glossary, hallucination, anti-pattern]
summary: Při překladu článků o nově objevených druzích Phase 1 Claude halucinoval české názvy ("tarantule" pro Ceratogyrus attonitifer, "býčí slon" pro bull elephant), protože druh nebyl v termdb a žádný projekt neměl genus-level fallback. Fix: NormalizedTermDB.lookup_genus_consensus extrahuje shared CZ genus z ≥3 sourozenců v termdb a poskytuje formulaci "nový druh <CZ_genus> (*Latin*)" jako pre-fetch hint do Phase 1.
source: critic_finding
uses: 3
successful_uses: 0
harmful_uses: 0
confidence: 1.00
maturity: validated
skill_scope: []
verify_check: "Grep('lookup_genus_consensus', path='C:/Users/stock/Documents/000_NGM/terminology-db/ngm_terminology/normalized_db.py') → 1+ matches"
related: [2026-04-12-sycophancy-not-hallucination.md, 2026-04-07-cross-project-memory-design.md, 2026-04-19-multica-curated-vs-similarity.md]
---

## Problém

Okavango článek (PREKLAD okavango_8.docx, 2526 slov, biology) přeložil Phase 1
4 nově objevené druhy halucinací českých názvů:

| Latin | Halucinace v překladu | Standardní česká forma |
|---|---|---|
| Ceratogyrus attonitifer | "Rohatý pavián pavouk" + "Tento tarantule má na zádech…" | sklípkan rohatý / nový druh sklípkana |
| Microctenopoma steveboyesi | "Šplhavec" | nový druh ostnovce |
| Breviceps ombelanonga | "Angolská dešťová žába" | otylka / nový druh otylky |
| (bull elephant) | "býčího slona" | samec slona |

Web search potvrdil: "býčí slon" v češtině prakticky neexistuje (0 hitů jako
zoologický termín), Ceratogyrus se v české zoologické literatuře nazývá **sklípkan**
(viz [ČT24 článek](https://ct24.ceskatelevize.cz/clanek/veda/68142) o tomtéž druhu).

## Root cause — 3 vrstvy selhání

1. **Druh není v termdb.** Nově objevené druhy z roku 2019-2021 nejsou v BIOLIB termdb
   (která má sourozenecké druhy stejného rodu).
2. **Žádný genus-level fallback.** Pre-translation lookup_terms_for_article hledal pouze
   exact binomial match. Nenašel-li, druh prošel do prompt term_table prázdný a
   Claude měl volnou ruku vymyslet český název.
3. **Žádný collocation guard.** Phase 5 (Czech context) neměla v tabulce false friends
   anglické "bull/cow/calf + animal" patterny ani "tarantula → tarantule" kalk.

Důsledek: pro tentýž druh ČT24 publikuje "sklípkan rohatý", PREKLAD vyprodukuje
"tarantule" — chybný gramatický rod (tarantule je feminine v ČJ) i nesprávná
zoologická čeleď (tarantule = Lycosa, sklípkan = Theraphosidae kam Ceratogyrus patří).

## Proč se to neopakovalo dřív

NG-ROBOT v dubnu 2026 už řešil podobný pattern u lesňáčka cerulea (commit `8e46032`
"core defekt: pre_resolve_species se volá až ve fázi 3" → fix `2417793`
"TermEnricher v ngrobot.py + unverified collector"). ADOBE-AUTOMAT má `docs/TASK_term_verification_audit.md`
(2026-04-17) varující před stejným patternem. Žádný z těchto auditů ale **neřešil
nový druh kde rod má sourozence v DB** — auditovali jen "druh je v DB" vs. "druh není v DB → web search".

PREKLAD byl klon NG-ROBOT/ADOBE-AUTOMAT a zdědil úplně stejnou mezeru. Plus regresi:
`termdb_misses=[]` jako TODO v orchestrátoru, takže Phase 3 web search vůbec neběžela.

## Řešení — 4-vrstvá obrana

### Vrstva 1 (PRE-translation): genus consensus extraction
Sdílená metoda `NormalizedTermDB.lookup_genus_consensus(genus)` v `terminology-db/ngm_terminology/normalized_db.py`:

- Hledá v termdb sourozenecké druhy stejného rodu
- Pokud ≥3 druhy a ≥70% sdílí stejné první slovo v českém názvu → vrátí ten genus name
- `Ceratogyrus` → `("sklípkan", 8)`, `Microctenopoma` → `("ostnovec", 4)`, `Breviceps` → `("otylka", 12)`
- Tato metoda je dostupná z PREKLAD (vlastní client.py má vlastní implementaci),
  NG-ROBOT (`pre_resolve_species` přes `_main_db`), ADOBE-AUTOMAT (`_extract_article_terms_from_db` přes `_main_db`)

### Vrstva 2: term_table pre-fetch s genus fallback
`lookup_terms_for_article(en_text, with_genus_fallback=True)` (PREKLAD termdb client) /
`_extract_article_terms_from_db(..., with_genus_fallback=True)` (ADOBE-AUTOMAT) /
`pre_resolve_species` "Genus consensus" sekce (NG-ROBOT) — všechny tři pre-fetch
do prompt term_table přidají formulaci `"nový druh <CZ_genus> (*Latin binomial*)"`.

### Vrstva 3: master_prompt anti-hallucination directives
Aktualizováno ve všech třech projektech:
- PREKLAD: `prompts/master_translator_v1.md` — sekce "Druhy mimo termdb — ZÁKAZ HALUCINACE"
- NG-ROBOT: `projects/1-PREKLAD-FORMAT/00_MASTER_v42.2.6.md` — "DRUHY MIMO TERMDB" + "POHLAVNÍ DIMORFISMY"
- ADOBE-AUTOMAT: `backend/services/text_pipeline/prompts/5-JAZYK-KONTEXT/MASTER_INSTRUCTIONS.md` — sekce 5a (collocation guard) + 5b (zoologická terminologie)

### Vrstva 4 (POST-translation): Phase 3 web_search trigger
PREKLAD orchestrator opraven: `termdb_misses=[]` TODO nahrazen reálným tracking
z Phase 1.6 artifacts. Phase 3 (web_search) nyní spustí pro Latin binomialy
nedohledatelné v termdb. Genus consensus hits se předávají do Phase 3 promptu jako
hint, takže verifier nemusí googlit známé rody.

## Co zůstalo nedotažené

- Live test okavango_8: 3/4 hits opraveno (sklípkan, ostnovec, samec slona),
  ale `Breviceps ombelanonga` Claude přeložil jako "Angolská dešťová žabka"
  místo "nový druh otylky" — Claude **přepsal** termdb hint vlastní heuristikou.
- Pro tvrdší enforcement potřebuje master prompt *invariant clause* nebo
  Phase 8 domain critic dostat termdb subset (kód x prompt rozpor v PREKLAD).

## Files changed

- `terminology-db/ngm_terminology/normalized_db.py` — nová metoda `lookup_genus_consensus`
- `BIOLIB/termdb.py` — top-level fallback `lookup_genus_consensus` (pro non-NormalizedTermDB konzumenty)
- `PREKLAD/preklad/termdb/client.py` — vlastní `lookup_genus_consensus` + genus fallback v `lookup_terms_for_article`
- `PREKLAD/preklad/pipeline/phase16_glossary.py` — track `termdb_misses` + `genus_consensus_hits`, CZ stopwords proti regex false-positive
- `PREKLAD/preklad/pipeline/orchestrator.py` — Phase 3 trigger nyní `if termdb_misses_list` místo `<5 fixes`
- `PREKLAD/preklad/pipeline/phase3_term_verification.py` — accept `genus_consensus_hits` parameter pro lepší prompt
- `PREKLAD/prompts/master_translator_v1.md` — anti-hallucination + dimorphism rules
- `PREKLAD/prompts/phase5_czech_context.md` — sekce 5a (dimorphism) + 5b (zoological taxa)
- `PREKLAD/tests/test_orchestrator_wiring.py` — přepsán Phase 3 trigger test pro novou sémantiku
- `NG-ROBOT/claude_processor/utilities.py` — `pre_resolve_species` Genus consensus sekce
- `NG-ROBOT/projects/1-PREKLAD-FORMAT/00_MASTER_v42.2.6.md` — DRUHY MIMO TERMDB + POHLAVNÍ DIMORFISMY
- `ADOBE-AUTOMAT/backend/services/text_pipeline/phases.py` — `_extract_article_terms_from_db` Pass 3 (genus fallback)
- `ADOBE-AUTOMAT/backend/services/text_pipeline/prompts/5-JAZYK-KONTEXT/MASTER_INSTRUCTIONS.md` — sekce 5a + 5b

## Live verification (PREKLAD okavango_8)

Před fixem: `audit.json line 204: "Tento tarantule má na zádech..."` + `line 175: "velkého býčího slona"`

Po fixu: `output.txt: "Tento nový druh sklípkana má na zádech..."` + `"velkého samce slona, který se přiblížil"`

Testy: 248 passed, 7 preexisting fails (Phase 1 chunking refactor, Phase 5 mock,
exporter — nesouvisí s touto změnou).
