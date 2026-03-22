# Session Checkpoint

**Saved**: 2026-03-22
**Task**: STOPA — Harness Engineering Integration
**Branch**: main
**Repo**: https://github.com/cetej/STOPA (working dir: `C:\Users\stock\Documents\000_NGM\STOPA`)
**Status**: Analýza + strategie hotová, implementace NEZAČALA

## Co je hotové (tato session)

### Analýza videí
- Staženy a vyčištěny přepisy 2 YouTube videí (yt-dlp, ne MCP):
  - `input/video1_transcript.txt` — Harness Engineering (20K chars)
  - `input/video2_transcript.txt` — Claude Certified Architect (42K chars)
- Kompletní analýza obou videí s identifikací 10 klíčových poučení

### Dokumentace
- `docs/LEARNINGS.md` — poučení z videí + YouTube transcript fix
- `docs/HARNESS_STRATEGY.md` — kompletní strategie harness integrace:
  - Gap analýza (7 gaps identifikováno)
  - Architektura: `.claude/harnesses/` + HARNESS.md formát
  - 4 konkrétní harnessy (Záchvěv pipeline, NG-ROBOT content, STOPA skill audit, code review)
  - 4-fázový implementační plán (A→B→C→D)
  - Rozhodovací tabulka skill vs harness
  - 4 quick wins implementovatelné okamžitě
- `.claude/memory/learnings.md` — 4 nové vzory přidány (harness engineering, prompts vs hooks, tool descriptions, path-specific rules)

### Zjištění
- YouTube transcript MCP server je nefunkční (hlásí "Video unavailable" na vše)
- `yt-dlp` 2026.3.17 funguje spolehlivě (po update z 2025.09.05)
- STOPA nemá `.claude/rules/` — identifikováno jako quick win

## ZADÁNÍ PRO DALŠÍ SESSION

### Priorita 1: Quick Wins (Fáze A) — nízký effort, okamžitý přínos

#### A1: Path-specific rules
Vytvořit `.claude/rules/` se 3 soubory:
- `python-files.md` — pattern `**/*.py`, pravidla: UTF-8, pathlib, type hints pro public API
- `skill-files.md` — pattern `**/SKILL.md`, pravidla: YAML frontmatter validace, description musí říkat kdy NE-použít
- `memory-files.md` — pattern `.claude/memory/**`, pravidla: max 500 řádků, archivace starých záznamů

#### A2: Skill description audit
Projít všech 13 skills a do každého description přidat:
- Kdy NEpoužít (negativní trigger)
- Příklad typického use case
- Referenční soubory: všech 13 SKILL.md v `.claude/skills/`

#### A3: Critic — separate session instrukce
Do `critic/SKILL.md` přidat pravidlo: "Pokud reviewuješ kód, který byl napsán v TÉTO session, doporuč uživateli spustit review v nové session pro nezaujatý pohled."

### Priorita 2: Harness Engine (Fáze B) — střední effort

#### B1: Harness adresář + engine
- Vytvořit `.claude/harnesses/_engine.md` — sdílená logika:
  - Jak číst HARNESS.md
  - Jak spouštět fáze sekvenčně
  - Jak validovat výstup fáze
  - Jak ukládat mezivýsledky do `.harness/`
  - Jak routovat modely per fáze

#### B2: `/harness` meta-skill
- `.claude/skills/harness/SKILL.md` — dispatcher:
  - Načte dostupné harnessy z `.claude/harnesses/`
  - Nabídne uživateli výběr
  - Spustí vybraný harness přes engine

#### B3: První harness — `skill-audit`
- `.claude/harnesses/skill-audit/HARNESS.md` — 5 fází:
  1. Inventory (glob skills, extract metadata)
  2. Description audit (specifičnost, negativní triggery)
  3. Tools audit (least privilege)
  4. Integration audit (shared memory, learnings)
  5. Report (template)
- Ověřit spuštěním na STOPA samotné

### Priorita 3: Záchvěv harness (po B)

#### Záchvěv pipeline harness
- `.claude/harnesses/zachvev-pipeline/HARNESS.md` — 8 fází s validátory
- Ale NEJDŘÍV musí být hotová Záchvěv Session 8 (topic labeling + UI redesign)
- Checkpoint Záchvěv Session 8 je stále platný — viz níže

### Bonus: Distribuce
- Po B3: přidat `harnesses/` do `stopa-orchestration/` pluginu
- Aktualizovat plugin.json manifest

---

## Aktivní checkpointy jiných projektů

### Záchvěv — Session 8 (NESPLNĚNO)
- **Repo**: `C:\Users\stock\Documents\000_NGM\ZACHVEV`
- **3 úkoly**: Topic labeling fix, growth_ratio guard, UI redesign
- **Detail**: Viz předchozí checkpoint (archivováno v git historii) nebo resume prompt níže

> Záchvěv — Session 8: Topic labeling fix + UI redesign.
> Repo: ZACHVEV (branch main), working dir: `C:\Users\stock\Documents\000_NGM\ZACHVEV`
> Pipeline kompletní end-to-end. Validováno na Letná datech (6615 postů, CRI 0.52).
> Uncommitted: `topics.py` (stopwords), `ui/app.py` (Session 7 UI) — commitni PŘED začátkem.
> **3 úkoly**: 1) Topic labeling hybrid, 2) growth_ratio guard, 3) UI redesign.

---

## Architektura (reference)

```
STOPA/
├── .claude/
│   ├── skills/          # 13 skills (source of truth)
│   ├── hooks/           # 7 hook scripts
│   ├── memory/          # Shared memory (state, decisions, learnings, budget, checkpoint, news)
│   ├── settings.json    # Hooks config
│   ├── rules/           # ← VYTVOŘIT (Fáze A1)
│   └── harnesses/       # ← VYTVOŘIT (Fáze B1)
│       ├── _engine.md
│       └── skill-audit/
├── stopa-orchestration/  # Plugin distribuce (v1.4.0)
├── docs/
│   ├── LEARNINGS.md      # ← NOVÉ (tato session)
│   └── HARNESS_STRATEGY.md  # ← NOVÉ (tato session)
├── input/                # Video přepisy
└── CLAUDE.md
```

## Uncommitted Changes

```
 M .claude/memory/checkpoint.md
 M .claude/memory/learnings.md   # 4 nové vzory
 M .claude/memory/news.md
?? docs/                          # LEARNINGS.md + HARNESS_STRATEGY.md
?? input/                         # Video přepisy + VTT soubory
?? research/
```

## Resume Prompt

> STOPA — Harness Engineering Integration.
> Repo: STOPA (branch main), working dir: `C:\Users\stock\Documents\000_NGM\STOPA`
>
> Analýza + strategie hotová. Klíčový dokument: `docs/HARNESS_STRATEGY.md`
>
> **Implementační plán (v pořadí priority):**
> 1. **Quick Wins (Fáze A)**: Vytvořit `.claude/rules/` (3 soubory), audit 13 skill descriptions (přidat "kdy NEpoužít"), update critic skill
> 2. **Harness Engine (Fáze B)**: `.claude/harnesses/_engine.md` + `/harness` meta-skill + první harness `skill-audit` (5 fází)
> 3. **Záchvěv harness**: Až po Session 8 (topic labeling + UI) — 8 fází pipeline s validátory
>
> Přečti `docs/HARNESS_STRATEGY.md` pro plný kontext. Uncommitted changes — commitni před začátkem práce.
>
> **Paralelně platný**: Záchvěv Session 8 checkpoint (topic labeling + UI redesign v ZACHVEV repo).
