# STOPA — Orchestration System Development

Meta-projekt pro vývoj a údržbu orchestračního systému Claude Code.

## Co je STOPA

STOPA je "source of truth" pro orchestrační systém — sadu skills, sdílenou paměť a workflow pro řízení komplexních úkolů pomocí Claude Code. Odtud se systém vyvíjí a distribuuje do cílových projektů.

## Struktura

```
STOPA/
├── stopa-orchestration/        # Plugin (distribuce)
│   ├── .claude-plugin/
│   │   └── plugin.json         # Manifest
│   ├── skills/                 # Orchestrační skills (subset)
│   ├── hooks/                  # Hook skripty + hooks.json
│   └── README.md
├── .claude/
│   ├── commands/               # KANONICKÉ skill soubory (flat: watch.md, autoloop.md...)
│   ├── skills/                 # KOPIE pro kompatibilitu (dirs: watch/SKILL.md...)
│   │                           # ⚠️ commands/ a skills/ MUSÍ být identické!
│   ├── rules/                  # Pravidla načítaná při každé session
│   ├── hooks/                  # Zdrojové hook skripty
│   ├── settings.json           # Hooks config pro lokální vývoj
│   └── memory/                 # Sdílená paměť systému
│       ├── state.md            # Stav aktuálního úkolu
│       ├── budget.md           # Rozpočtový ledger
│       ├── decisions.md        # Log rozhodnutí
│       ├── key-facts.md        # Referenční data projektu
│       ├── learnings/          # Per-file YAML learnings (grep-first retrieval)
│       ├── checkpoint.md       # Snapshot session
│       ├── news.md             # Výsledky /watch scanů
│       ├── radar.md            # Výsledky /radar evaluací
│       ├── improvement-log.md  # Audit trail cross-project routingu
│       ├── outcomes/           # Per-run RCL credit records
│       ├── failures/           # HERA failure trajectory records
│       └── *-archive.md        # Archivy (decisions, budget)
├── scripts/
│   └── sync-orchestration.sh  # Legacy sync do cílových projektů
└── CLAUDE.md                  # Tento soubor

~/.claude/memory/projects/      # Globální project profiles (YAML)
                                # Stack, domény, cíle, watch_topics pro každý projekt
```

## Cílové projekty

Orchestrační systém se distribuuje do těchto projektů (plný seznam v `~/.claude/memory/projects/`):

| Projekt | Typ | Priorita |
|---------|-----|----------|
| **NG-ROBOT** | content-pipeline | high |
| **ADOBE-AUTOMAT** | automation | medium |
| **ZACHVEV** | social-analysis | medium |
| **POLYBOT** | prediction-markets | medium |
| **MONITOR** | OSINT intelligence | medium |
| **GRAFIK** | image-editing | low |
| **KARTOGRAF** | cartography | low |
| **DANE** | tax-calculator | low |
| **BONANZA** | trading-bot | low |
| **ADVISORS** | personal-AI | low |

## Distribuce do projektů

### Metoda 1: Marketplace přes settings.json (doporučeno)

Přidej do `.claude/settings.json` cílového projektu (mergni s existujícími klíči):

```json
{
  "extraKnownMarketplaces": {
    "stopa-tools": {
      "source": {
        "source": "github",
        "repo": "cetej/STOPA"
      }
    }
  },
  "enabledPlugins": {
    "stopa-orchestration@stopa-tools": true
  }
}
```

Plugin se auto-instaluje z GitHub marketplace. Skills dostupné po restartu CC.

### Metoda 2: Plugin install (CLI)

```bash
/plugin install github.com/cetej/STOPA --subdir stopa-orchestration
```

### Metoda 3: Local directory (vývoj)

```bash
claude --plugin-dir ./stopa-orchestration
```

Plugin balí skills + hooks do jednoho distribučního balíčku. Skills jsou dostupné jako `/stopa-orchestration:orchestrate`, `/stopa-orchestration:scout` atd.

### Metoda 4: Sync skript (legacy)

```bash
# Z STOPA do cílového projektu:
./scripts/sync-orchestration.sh /cesta/k/cilovemu/projektu --dry-run
./scripts/sync-orchestration.sh /cesta/k/cilovemu/projektu --commit
./scripts/sync-orchestration.sh --all --commit
```

Sync kopíruje skills, hooks, settings a memory soubory přímo do `.claude/` cílového projektu. Skills jsou pak dostupné bez namespace (`/orchestrate` místo `/stopa-orchestration:orchestrate`). CLAUDE.md cílového projektu se nekopíruje (je projekt-specifický).

## Orchestrační systém — pravidla

### Kdy orchestrovat automaticky
- Úkol má 3+ kroků nebo zasahuje do víc souborů → `/orchestrate`
- Jednokrokový edit nebo jednoduchá otázka → přímo bez orchestrace
- Při pochybnostech → raději orchestrovat

### Budget tiers
| Tier | Agenti | Critic | Scout | Model | Kdy |
|------|--------|--------|-------|-------|-----|
| light | 0-1 | 1× na konci | povrchový | haiku | Jednoduchý fix |
| standard | 2-4 | 2× | hloubkový | sonnet | Víc souborů |
| deep | 5-8 | 3× | plný mapping | opus | Cross-cutting změna |
| farm | 5-8 (Teams) | 1× post-sweep | minimální | sonnet | Bulk mechanical improvement (20+ souborů, linter fixy, migrace) |

### Model selection: one-shot vs iterativní

| Typ úlohy | Model | Důvod |
|-----------|-------|-------|
| One-shot generování (single edit, scaffold) | haiku/sonnet | Scale nepomáhá při absenci feedbacku |
| Iterativní oprava (autoloop, autoresearch) | sonnet/opus | Větší model lépe exploituje execution feedback |
| Validace, kontrola (critic, verify) | haiku/sonnet | Read-only, stačí menší model |
| Sub-agent s repair loop (self-evolve, tdd) | sonnet+ | Repair loop = iterativní → silnější model |

### Circuit breakers
- Agent loop: 3× stejný agent na stejný subtask → STOP
- Critic loop: 2× FAIL na stejný cíl → STOP, ptej se uživatele
- Budget exceeded → STOP
- Nesting depth > 2 → STOP
- Memory soubor > 500 řádků → údržba

### Session continuity
- Na začátku session přečti `.claude/memory/checkpoint.md` — pokud existuje, nabídni pokračování
- Při velkém kontextu (>70% subtasků, 3+ agentů) → auto-checkpoint
- `/checkpoint save` pro ruční uložení

### Cross-project improvement routing
- `/improve <finding>` — skóruje finding × project profiles, vytváří GitHub issues
- `/improve sweep` — proaktivní scan neodeslených findings z news.md, radar.md, learnings/
- `/watch` a `/radar` automaticky volají `/improve` po nalezení relevantních novinek
- Project profiles: `~/.claude/memory/projects/*.yaml` (priority thresholds: high >= 3, medium >= 5, low >= 7)
- Scheduled task `cross-project-improve-sweep` běží St+So 10:00

### /watch novinky
- Týdenní scan novinek (Claude Code, API, AI/ML ekosystém)
- Orchestrátor připomene pokud poslední scan > 7 dní
- `/watch quick` jen Anthropic novinky, `/watch full` vše

## Dev workflow

```bash
# Validace skill souboru (sync check)
diff .claude/commands/improve.md .claude/skills/improve/SKILL.md

# Spuštění Python hooků lokálně
python .claude/hooks/learning-admission.py < test-input.json

# Kontrola memory health
wc -l .claude/memory/*.md  # žádný soubor > 500 řádků

# Distribuce do cílového projektu
./scripts/sync-orchestration.sh /cesta/k/projektu --dry-run
```

## Konvence vývoje

- Skills formát: `.claude/skills/<name>/SKILL.md` s YAML frontmatter
- Memory: markdown soubory v `.claude/memory/`
- Jazyk: česky pro uživatelské texty, anglicky pro technické instrukce v skills
- Git: commit česky, branch naming standardní
