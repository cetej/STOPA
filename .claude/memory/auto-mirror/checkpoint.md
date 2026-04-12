# Session Checkpoint

**Saved**: 2026-04-03 ~19:00
**Task**: NG-ROBOT Media Expansion — Bundle Composer modul
**Branch**: main (pushed)
**Progress**: Bundle Composer funguje, ale narušil article preview parser

## What Was Done This Session

- **Bundle upload dialog** — Fáze 1b: pre-processing dialog pro výběr hlavního dokumentu, typu výstupu, sloučení textů
- **Bundle Composer modul** — Nový nezávislý modul `bundle_composer.py` s 4-tier token managementem:
  - Tier 1 (<80K): přímá kompozice (Sonnet)
  - Tier 3 (150-300K): 2-pass Haiku extrakce → Sonnet kompozice
  - 4 typy výstupu: článek, reportáž, rozhovor, video titulky
- **projects/KOMPOZICE/** — 5 instrukčních souborů (base metodika + per-type)
- **blueprints/bundles_bp.py** — 3 API endpointy (compose, types, list)
- **UI integrace** — typ selector v bundle dialogu, composed articles v inbox s ✍️ ikonou
- **Pipeline integrace** — bundle.json v composed output pro media copy, bundle detection fix v task_process_inbox_selected
- **`_remove_phase_notes` rozšíření** — filtry pro SEO METADATA, TRIAGE, STATISTIKY, FAQ, FOTO šablony, V KOSTCE
- **Fix: `import json` v specialized.py** — chybějící import (ruff autofix regrese)

## KRITICKÝ BUG — NARUŠENÝ ARTICLE PREVIEW

Úpravy v `_remove_phase_notes()` v `claude_processor/phases.py` **narušily article preview parser** (`parse_final_article`). Symptomy:
- **body = prázdný string** — tělo článku se neparsuje
- **photos = 0** — žádné fotky
- h1_title a perex fungují
- Postihuje **všechny články**, ne jen composed

**Root cause**: Pravděpodobně nové regex pattern v `_remove_phase_notes` (krok 0f) filtrují příliš agresivně a odstraňují i legitimní sekce článku. Regex pro pipeline sekce (`## SEO METADATA`, `## V KOSTCE` atd.) může matchovat i obsah těla.

**Soubor**: `C:\Users\stock\Documents\000_NGM\NG-ROBOT\claude_processor\phases.py`, řádky ~3644-3700 (krok 0f + analytical_patterns)

## What Remains

| # | Subtask | Status | Method |
|---|---------|--------|--------|
| 1 | **FIX: _remove_phase_notes regex** | CRITICAL | Revert nebo opravit regex v kroku 0f. Test na 3+ článcích. |
| 2 | **FIX: parse_final_article pro composed articles** | HIGH | `## PEREX` → bold text konverze, body parsing |
| 3 | **Ověřit fotky v pipeline output** | MEDIUM | Zkontrolovat že bundle.json → _process_bundle → images/ kopie funguje |
| 4 | **Uklidit analytics/ KONGO-DENIK adresář** | LOW | Smazat starý bundle v analytics/ |
| 5 | **Vylepšit KOMPOZICE instrukce** | LOW | Na základě výstupů doladit prompty per typ |

## Immediate Next Action

**REVERT nebo FIX `_remove_phase_notes` v `claude_processor/phases.py`** — krok 0f (pipeline section filtering) je příliš agresivní. Nejbezpečnější: revertovat commit `2c8a8ae` (ten přidal nové filtry) a pak přidat filtry opatrněji s testem na 3+ existujících článcích.

## Tried and Failed

- **Bundle → analytics flow**: Analytika je příliš těžký workflow (3-stage: analyze → ideas → drafts). 205K text způsobil max_tokens truncation. → Vytvořen samostatný Bundle Composer.
- **`## PEREX` formát**: Composer generuje perex jako H2 nadpis, ale pipeline/preview parser očekává bold text. → Nutno opravit buď v composeru nebo v parseru.

## Key Context

- Bundle Composer je NEZÁVISLÝ modul — nepoužívá analytiku ani existující pipeline pro kompozici
- Composed articles mají `metadata.json` + `bundle.json` + `original.md` v inbox/
- `list_inbox_files` pořadí: composed (metadata.json) → bundle (bundle.json) → flat files
- Pipeline `_process_bundle` detekce funguje pro composed articles díky bundle.json
- Model IDs z `config.py`: `claude-sonnet-4-6`, `claude-haiku-4-5-20251001` (NE s datem suffixem!)
- `import json` v `specialized.py` chyběl kvůli ruff autofix regresi
- Projekt: `C:\Users\stock\Documents\000_NGM\NG-ROBOT`

## Git State

- Branch: main (pushed)
- Uncommitted changes: Ne
- Last commits: 23 commitů v této session

## Resume Prompt

> **FIX CRITICAL: article preview broken in NG-ROBOT**
>
> Projekt: `C:\Users\stock\Documents\000_NGM\NG-ROBOT`
> Přečti CLAUDE.md.
>
> Změny v `_remove_phase_notes()` v `claude_processor/phases.py` (krok 0f, ~řádky 3644-3700) narušily article preview parser. Symptom: `parse_final_article()` vrací prázdný body a 0 photos pro VŠECHNY články. Příčina: nové regex filtry pro pipeline sekce (SEO METADATA, V KOSTCE, STATISTIKY atd.) jsou příliš agresivní.
>
> Postup:
> 1. Přečti `phases.py` krok 0f (řádky ~3644-3700) a `analytical_patterns` list
> 2. Testuj `parse_final_article` na 3 různých článcích v `processed/` — zjisti co přesně rozbíjí body
> 3. Oprav regex nebo revertuj commit `2c8a8ae` a přidej filtry opatrněji
> 4. Ověř že preview funguje: `/api/article/parse-preview` vrací body > 0 a photos > 0
> 5. Pak ověř composed article: `2026-04-03_za-pralesnimi-slony-ceska-umelecka-expedice-v-srdc`
>
> Sekundární: `## PEREX` v composed articles (H2 místo bold) — opravit v bundle_composer instrukcích nebo v parseru.
>
> Kontext: `.claude/memory/checkpoint.md`, plán v `~/.claude/plans/polished-fluttering-willow.md`
