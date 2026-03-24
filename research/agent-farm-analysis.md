# Agent Farm Analysis — claude_code_agent_farm

**Datum:** 2026-03-24
**Zdroj:** [Dicklesworthstone/claude_code_agent_farm](https://github.com/Dicklesworthstone/claude_code_agent_farm)
**Reddit:** [r/Anthropic thread](https://www.reddit.com/r/Anthropic/comments/1lpa7kx/claude_code_agent_farm/)

## Co to je

Orchestrační framework pro spouštění 20-50 paralelních Claude Code sessions přes tmux.
Agenti systematicky vylepšují codebase — buď fixí bugy, nebo implementují best practices.

- **Autor:** Jeffrey Emanuel
- **Licence:** MIT + OpenAI/Anthropic Rider
- **Hlavní soubor:** `claude_code_agent_farm.py` (132 KB, monolitický)
- **Prerequisity:** Python 3.13+, tmux, Linux/macOS

## 3 Workflow módy

### 1. Bug Fixing
- Spustí linter/type-checker → vygeneruje problems file
- Agenti si berou random chunky → markují [COMPLETED]
- Vhodné pro: tisíce linter warnings, chybějící type hints

### 2. Best Practices Implementation
- Nakopíruje best practices guide do projektu
- Agenti systematicky implementují → trackují progress %
- 35 předpřipravených guides (Next.js, Python, Rust, Go, Java, C++...)

### 3. Cooperating Agents (nejzajímavější)
- Lock-based coordination přes `/coordination/` directory
- Agenti si claimují soubory, žádné merge conflicty
- **Implementováno ČISTĚ promptem** — žádný orchestrační kód, LLM je dost chytrý
- Lock structure:
  ```
  /coordination/
  ├── active_work_registry.json
  ├── completed_work_log.json
  ├── agent_locks/{agent_id}_{timestamp}.lock
  └── planned_work_queue.json
  ```

## Architektura — klíčové vzory

| Vzor | Detail |
|------|--------|
| **Tmux multiplexing** | Každý agent = 1 tmux pane, monitor dashboard v controller window |
| **Lock-based coordination** | File locks brání concurrent přístupu ke stejným souborům |
| **Heartbeat monitoring** | Detekce stuck agentů (>2 min), auto-restart s exponential backoff |
| **Context management** | Sleduje % context window, auto-clear pod prahem (default 20%) |
| **Adaptive stagger** | Launch delay se zkracuje při úspěchu, prodlužuje při selhání |
| **Settings backup** | Automaticky zálohuje `.claude/settings.json`, rotace posledních 10 |
| **HTML reports** | Run report na konci s per-agent statistikami |

## Rozsah dodávky

| Resource | Počet |
|----------|-------|
| Tech stacků | 34 |
| Config souborů | 37 |
| Prompt templates | 37 |
| Best practices guides | 35 |
| Tool setup scriptů | 24 |

## Omezení a rizika

- **`--dangerously-skip-permissions`** — běží bez bezpečnostních kontrol
- **Linux/macOS only** (tmux) — na Windows nefunguje nativně
- **~500 MB RAM per agent** — 20 agentů = 10 GB RAM
- **Monolitický Python** (132 KB single file) — těžké na údržbu
- **Není Agent Teams/SDK** — tmux wrapper okolo CLI `claude`, ne nativní API
- **API rate limits** — 20+ paralelních sessions = rychlý náraz do limitů

## Kde dává farm přístup smysl

### Ideální use cases

1. **Legacy codebase cleanup** — tisíce linter warnings, Python 2→3 migrace, TS strict mode
2. **Best practices sweep** — konzistentní error handling, logging, testy přes 500+ souborů
3. **Monorepo s nezávislými balíčky** — každý agent = jeden package, nulové konflikty
4. **Test coverage boost** — každý agent generuje testy pro jiný modul, z 30% → 70%
5. **Framework migrace** — React class→hooks, Express→Fastify, mechanická práce

### Kde NEDÁVÁ smysl

- Malé projekty (<50 souborů) — overhead > přínos
- Tightly coupled kód — agenti si šlapou po sobě
- Architektonické změny — potřebuješ jednu vizi, ne 20 různých
- Kreativní práce — nový feature design, UX rozhodnutí

### Klíčový insight

Farm řeší "embarrassingly parallel" problémy v kódu — práci, která je:
- **Mechanická** (pravidlo je jasné, jen to chce aplikovat)
- **Partitionovatelná** (soubor = nezávislá jednotka)
- **Verifikovatelná** (linter/testy potvrdí správnost)

To je překvapivě velká část údržby reálných projektů.

## Srovnání s STOPA orchestrací

| Aspekt | Agent Farm | STOPA |
|--------|-----------|-------|
| Scale | 20-50 agentů | 1-8 agentů |
| Koordinace | File locks + prompts | Agent Teams SDK (nativní) |
| Permissions | Skipped (dangerous) | Normální CC permissions |
| Platform | Linux (tmux) | Cross-platform |
| Distribuce | Standalone script | Plugin systém |
| Flexibility | Config JSON + prompt files | Skills + memory + hooks |
| Use case | Bulk mechanical improvements | Quality-focused orchestrace |

## Inspirace pro STOPA

### 1. Cooperating Agents prompt pattern
Prompt-only coordination je validace STOPA přístupu (skill-driven orchestrace).
Stojí za studium: `prompts/cooperating_agents_improvement_prompt_for_python_fastapi_postgres.txt`

### 2. Farm tier v orchestrátoru
Nový tier v `/orchestrate` pro bulk improvements — viz `/farm` skill design.

### 3. Best practices guides jako reusable assets
35 technologických guides by mohly být distribuovány jako standalone resource.

### 4. Heartbeat + auto-restart pattern
Monitoring s exponential backoff je robustní — aplikovatelné na Agent Teams.

## Relevance pro naše projekty

| Projekt | Farm potenciál | Proč |
|---------|---------------|------|
| NG-ROBOT | Střední | Pipeline scripty, konzistenční sweep |
| ADOBE-AUTOMAT | Nízký | Malý projekt |
| STOPA | Nízký | Meta-projekt, malé soubory |
| Budoucí velký projekt | Vysoký | Pokud 200+ souborů |

## Závěr

Agent Farm je brute-force nástroj pro kvantitativní vylepšení. STOPA je kvalitativní orchestrátor.
Nejsou to protiklady — mohou koexistovat. Farm tier v STOPA by přinesl best of both worlds:
nativní Agent Teams koordinaci (bez tmux, cross-platform) s farm-style bulk processing.
