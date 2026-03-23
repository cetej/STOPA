# Harness Engine — Shared Execution Logic

Tento dokument definuje jak číst, spouštět a validovat harnessy. Každý harness (HARNESS.md) ho implicitně používá.

## Jak číst HARNESS.md

Harness soubor má:
1. **YAML frontmatter** — metadata (name, description, phases count, estimated tokens, output template)
2. **Fáze** — sekce `## Phase N: Name (type)` kde type je `deterministic`, `LLM`, `template`, `parallel`, nebo `human-input`
3. **Validace per fáze** — řádek `- **Validation**:` s podmínkami které MUSÍ projít

## Spouštění fází

### Sekvenční exekuce
Fáze se spouštějí **striktně v pořadí 1 → N**. Žádná fáze nesmí být přeskočena.

### Resumability
Pokud existuje `.harness/` adresář s mezivýsledky, engine:
1. Najde poslední úspěšně validovanou fázi (soubor `phaseN_*.json` existuje a je validní)
2. Pokračuje od fáze N+1
3. Informuje uživatele: "Resuming from Phase N+1 (phases 1-N already completed)"

### Postup per fáze
```
1. Přečti instrukce fáze z HARNESS.md
2. Načti vstupy (předchozí fáze z .harness/ nebo uživatelský vstup)
3. Zvol model dle `- **Model**:` řádku (default: sonnet)
4. Spusť akci (Glob/Grep/Read pro deterministic, Agent pro LLM, template fill)
5. Ulož výstup do `.harness/phaseN_<name>.json`
6. Validuj dle `- **Validation**:` pravidel
7. Pokud validace PASS → pokračuj na N+1
8. Pokud validace FAIL → STOP, zapiš chybu do `.harness/error.md`, informuj uživatele
```

## Validace výstupů

### Typy validací
| Typ | Příklad | Implementace |
|-----|---------|-------------|
| Count | `≥1 entry point nalezen` | Kontrola length pole v JSON |
| Schema | `JSON schema validace` | Kontrola povinných klíčů |
| Range | `CRI ∈ [0,1]` | Numerická kontrola |
| Completeness | `no {{MISSING}} placeholders` | Grep výstupního souboru |
| Format | `české texty, ≤500 slov` | Word count + encoding check |
| Exit code | `exit code 0` | Bash return code |

### Validace = programatická, ne LLM
Validace MUSÍ být kontrolovatelná kódem (assertions, schema checks), ne LLM reviewem. Jedinou výjimkou je kvalitativní review na konci (quality gate), kde se použije `/critic`.

## Ukládání mezivýsledků

Working directory: `.harness/` (relativní k projektu)

```
.harness/
├── phase1_inventory.json
├── phase2_analysis.json
├── phase3_risks.json
├── ...
├── error.md              # Pokud fáze selže — obsahuje fázi, chybu, vstup
└── report.md             # Finální výstup (pokud harness generuje report)
```

- Formát: JSON pro strukturovaná data, MD pro reporty
- Encoding: UTF-8
- Každý soubor obsahuje `_meta` klíč: `{"phase": N, "timestamp": "ISO8601", "model": "haiku/sonnet/opus"}`

## Model routing per fáze

| Typ fáze | Doporučený model | Důvod |
|----------|-----------------|-------|
| deterministic (Glob, Grep, Read) | haiku | Stačí na file listing, levný |
| LLM analysis (single) | sonnet | Dobrý reasoning za rozumnou cenu |
| LLM synthesis (summary, report) | sonnet | Potřebuje reasoning |
| Parallel sub-agents | sonnet | Narrow task per agent |
| Template fill | haiku | Mechanické vyplňování |
| Complex/creative | opus | Jen když sonnet nestačí |

Engine RESPEKTUJE `- **Model**:` z HARNESS.md. Pokud chybí, použije tabulku výše.

## Error handling

- Fáze selže → engine zapíše `.harness/error.md` s kontextem
- 2× selhání stejné fáze → STOP, escalate k uživateli
- Budget exceeded → STOP, save progress to `.harness/`
- Timeout (fáze > 5 minut bez output) → WARN, continue

## Integration se STOPA orchestrací

- Harness aktualizuje `.claude/memory/state.md` — "Running harness: X, Phase N/M"
- Po dokončení: zapíše do `.claude/memory/decisions.md` výsledek
- Pokud harness najde problém: zapíše do `.claude/memory/learnings.md`
- Budget tracking: každá fáze reportuje token usage do `.claude/memory/budget.md`
