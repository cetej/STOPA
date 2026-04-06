# Project Health Sweep — 2026-04-06

## Summary

| Projekt | Uncommitted | Stale branches | Poslední commit | Issues |
|---------|-------------|----------------|-----------------|--------|
| STOPA | 11 souborů | 4 local | 4 min ago | Learnings + branches |
| NG-ROBOT | clean | 4 local | 2h ago | Stale branches |
| ADOBE-AUTOMAT | 5 untracked | 2 local | 12h ago | Backend deps untracked, stale checkpoint |
| ZACHVEV | 1 untracked | 0 | 2d ago | .claude/ untracked |
| POLYBOT | 3 untracked | 0 | 2d ago | Stale checkpoint (Mar 28) |
| MONITOR | 1 untracked | 0 | 15h ago | Untracked doc |
| GRAFIK | 1M + 2 untracked | 0 | 2d ago | Modified upload.py uncommitted |
| terminology-db | clean | 0 | 8d ago | Chybí CLAUDE.md |

## Findings

### STOPA
- 11 uncommitted souborů: learnings/*.md (9 souborů), news.md, radar.md — generované memory soubory, nezacommitované
- 4 stale local branches: `autoloop/batch-all-1773931835`, `autoloop/dependency-audit-1773930602`, `autoloop/watch-1773931685`, `claude/tender-bardeen`
- Checkpoint z 2026-04-04 (2 dny starý — OK)

### NG-ROBOT
- Clean working tree
- 4 stale local branches: `claude/relaxed-lamport`, `claude/reverent-jennings`, `feature/mcp-optimization`, `master`
- Aktivní checkpoint z dnešního dne (2026-04-06) — session probíhala

### ADOBE-AUTOMAT
- 5 untracked souborů v `backend/`: `annotated_types/`, `pydantic/`, `pydantic_core/`, `typing_extensions.py`, `typing_inspection/` — vendorované Python packages, měly by být v .gitignore
- 2 stale local branches: `claude/kind-noyce`, `claude/priceless-blackwell`
- Checkpoint z 2026-04-02 (4 dny) — pravděpodobně stale/abandoned session

### ZACHVEV
- Untracked `.claude/` directory — buď chybí .gitignore entry nebo je třeba commitnout
- Žádný checkpoint

### POLYBOT
- 3 untracked: `settings.local.json`, `data/research/`, `docs/WALLET_SETUP_PLAN.md`
- Checkpoint z 2026-03-28 (9 dní starý) — stale, pravděpodobně abandoned session "Signal Layer Upgrade"

### MONITOR
- 1 untracked: `docs/ANALYTICAL_SOURCES.md` — nový doc nezacommitovaný

### GRAFIK
- 1 modified: `grafik/fal/upload.py` — nezacommitovaná změna
- 2 untracked: `settings.local.json`, `Stará iterace modulu critic.txt`

### terminology-db
- Chybí `CLAUDE.md` — jediný projekt bez instrukcí pro Claude Code
- Poslední commit 8 dní ago — zatím nedosahuje 30-denního dormancy thresholdu

## Recommendations

1. **STOPA**: Commitni learnings/news.md/radar.md — jsou to auto-generated soubory, ale mají být v gitu. Smaž stale autoloop/* branches.
2. **NG-ROBOT**: Smaž stale `claude/*` a `feature/mcp-optimization` branches. `master` branch je redundantní (hlavní je `main`).
3. **ADOBE-AUTOMAT**: Přidej `backend/` do `.gitignore` (vendorované deps). Zvaž cleanup stale checkpoint (Apr 2).
4. **ZACHVEV**: Přidej `.claude/` do `.gitignore` nebo commitni settings.
5. **POLYBOT**: Cleanup stale checkpoint ze Mar 28. Přidej `settings.local.json` do `.gitignore`.
6. **MONITOR**: Commitni nebo gitignore `docs/ANALYTICAL_SOURCES.md`.
7. **GRAFIK**: Commitni `grafik/fal/upload.py` změnu. Smaž `Stará iterace modulu critic.txt`.
8. **terminology-db**: Přidej `CLAUDE.md` s popisem projektu a stack info.
