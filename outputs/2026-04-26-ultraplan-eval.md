---
date: 2026-04-26
status: blocked-by-access
issue: https://github.com/cetej/STOPA/issues/21
related_news: news.md 2026-04-21 row 73 + Morning Watch #107
---

# CC Ultraplan — Evaluation (BLOCKED)

## Verdict

**Preview není dostupný na tomto účtu.** Re-evaluate při GA.

## Důkaz nedostupnosti

Tested 2026-04-26 in worktree `quirky-robinson-b93507` (CC current install):

### Test 1 — `claude ultraplan`
```
$ claude ultraplan
`ultraplan` není v dostupných skills. Nejbližší odpovídající skills jsou:
- `/orchestrate` — multi-step task decomposition + agent plan
- `/plan` (subagent type) — implementation planning
- `/build-project` — end-to-end autonomous project builder
```
CC sám hlásí že žádný takový skill/command nezná — fuzzy match selhal.

### Test 2 — `claude --help | grep -i ultraplan`
0 matches. Help neobsahuje žádný Ultraplan subcommand ani flag.

### Test 3 — `claude --help` Commands sekce
Dostupné top-level commands: `agents`, `auth`, `auto-mode`, `doctor`, `install`, `mcp`, `plugin|plugins`, `setup-token`, `update|upgrade`. Žádný `ultraplan`.

### Test 4 — `--permission-mode` choices
Mód `plan` existuje (existing `EnterPlanMode` flow), ale to je něco jiného — interactive plan-then-confirm v rámci jedné session, ne cloud drafting + remote execution.

## Co tedy news.md popisoval

News.md 2026-04-21 row 73 + #107 v Morning Watch zmiňují "CC /ultraplan — cloud planning sessions" jako WATCH-priority signál. Buď:
1. Preview je gated (jako Project Glasswing #110), my v invite waveu nejsme
2. Feature byl rebrandován / odložen
3. Watch report citoval tweet/announce, který nereflektoval skutečný release stav

## Re-evaluation triggers

Sleduj v `/watch` scanech:
- "ultraplan" jako CC subcommand v `claude --help`
- Anthropic docs.claude.com/claude-code stránku o cloud plan execution
- GA announcement pro `/ultraplan` (changelog CC)

Při kterémkoliv signálu: re-spawn issue #21 evaluation s plnou pilot úlohou (`cross-project-improve-sweep`), kompletním comparison vs current `scheduled-tasks/` + `RemoteTrigger` pattern, hooks/memory access matrix.

## Status pro issue

**Issue zůstává OPEN** — toto není negativní rozhodnutí, jen blocked-by-access. Uživatel rozhodne migration plán až když bude preview dostupný.
