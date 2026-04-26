# CC Ultraplan — Evaluation Report

**Date:** 2026-04-26
**Issue:** [#21 cetej/STOPA](https://github.com/cetej/STOPA/issues/21)
**Status:** ⚠️ Blocked by access — preview not available on user account

## TL;DR

Preview feature `claude ultraplan` (announced 2026-04-21 per news.md #107) **není dostupné** na tomto Claude Code instalaci. Vyhodnocení odloženo do GA release.

## Verification

```bash
$ claude --version
2.1.104 (Claude Code)

$ claude ultraplan --help
# Returns generic --help (no ultraplan subcommand)

$ claude --help | grep -i ultraplan
# No matches
```

V `claude --help` existuje jen `--permission-mode plan` (preexisting plan-mode flag, **ne** Ultraplan). Žádný `ultraplan` subcommand, žádné cloud-drafting flagy.

## News.md Reference

```
| 2026-04-21 | WATCH | CC /ultraplan — cloud planning sessions | med | No |

#107 | CC Ultraplan preview | Cloud plan drafting z CLI, review v web editoru,
       remote run nebo pull back local — nová hybridní orchestrace |
       Prozkoumat pro STOPA remote scheduled tasks
```

Označeno "preview" — pravděpodobně gated na konkrétní účty / tier. Spuštěno před 5 dny (relativně k 2026-04-26).

## STOPA Relevance (theoretical, pending access)

Pokud by Ultraplan poskytoval:
- **Cloud execution** scheduled tasks → mohl by nahradit aktuální `RemoteTrigger` pattern
- **Web editor pro review plánu** → vizuální debug pro kompletní orchestrace
- **Pull-back local** → testování v cloud + commit local

…pak by stálo za migraci 1 pilot tasku (návrh: `cross-project-improve-sweep`).

Ale dokud `claude ultraplan` nemá help text, nemá smysl spekulovat o:
- Hooks support (kritické pro STOPA — 70+ hooks)
- Memory access (čte `.claude/memory/brain/`?)
- Cost model (je cloud execution účtováno separately?)

## Recommendation

**Wait for GA.** Re-evaluate když:
1. `claude ultraplan --help` vrátí non-empty help text, NEBO
2. Anthropic officially oznámí GA release v changelogu

Kontrolovat měsíčně přes `/watch` (které novinky kolem CC sleduje).

**Do NOT** speculate na hypothetical capabilities — STOPA má funkční `RemoteTrigger` + 38 scheduled-tasks SKILLs, není urgentní.

## Action Items

- [x] Verify access (failed — command absent)
- [x] Write report
- [ ] Comment na issue #21 s linkem na tento report (next step)
- [ ] **Issue zůstává OPEN** — uživatel zavře po GA evaluation
- [ ] Add `ultraplan` keyword do `/watch` watchlist pro auto-detection GA
