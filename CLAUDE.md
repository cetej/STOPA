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
│   ├── skills/                 # 9 orchestračních skills
│   ├── hooks/                  # Hook skripty + hooks.json
│   └── README.md
├── .claude/
│   ├── skills/                 # Zdrojové skills (source of truth)
│   ├── hooks/                  # Zdrojové hook skripty
│   ├── settings.json           # Hooks config pro lokální vývoj
│   └── memory/                 # Sdílená paměť systému
│       ├── state.md            # Stav aktuálního úkolu
│       ├── budget.md           # Rozpočtový ledger
│       ├── decisions.md        # Log rozhodnutí
│       ├── learnings.md        # Pointer → learnings/ directory
│       ├── learnings/          # Per-file YAML learnings (grep-first retrieval)
│       ├── checkpoint.md       # Snapshot session
│       ├── news.md             # Výsledky /watch scanů
│       ├── decisions-archive.md  # Archiv starých rozhodnutí
│       └── budget-archive.md     # Archiv budget historie
├── scripts/
│   └── sync-orchestration.sh  # Legacy sync do cílových projektů
└── CLAUDE.md                  # Tento soubor
```

## Cílové projekty

Orchestrační systém se distribuuje do těchto projektů:
- **NG-ROBOT** — https://github.com/cetej/NG-ROBOT (hlavní projekt na desktopu)
- **test1** — https://github.com/cetej/test1 (Pyramid Flow, web session)
- **ADOBE-AUTOMAT** — https://github.com/cetej/ADOBE-AUTOMAT (Adobe automatizace)

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

### Metoda 2: Sync skript (legacy)

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
| Tier | Agenti | Critic | Scout | Kdy |
|------|--------|--------|-------|-----|
| light | 0-1 | 1× na konci | povrchový | Jednoduchý fix |
| standard | 2-4 | 2× | hloubkový | Víc souborů |
| deep | 5-8 | 3× | plný mapping | Cross-cutting změna |

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

### /watch novinky
- Týdenní scan novinek (Claude Code, API, AI/ML ekosystém)
- Orchestrátor připomene pokud poslední scan > 7 dní
- `/watch quick` jen Anthropic novinky, `/watch full` vše

## Konvence vývoje

- Skills formát: `.claude/skills/<name>/SKILL.md` s YAML frontmatter
- Memory: markdown soubory v `.claude/memory/`
- Jazyk: česky pro uživatelské texty, anglicky pro technické instrukce v skills
- Git: commit česky, branch naming standardní
