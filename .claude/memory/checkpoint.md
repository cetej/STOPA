# Session Checkpoint

**Saved**: 2026-03-19 (late evening session)
**Task**: Agent Teams test + quick wins (TeammateIdle hook, sync, plugin bump)
**Branch**: main
**Progress**: 4/5 tasks complete, 1 deferred (Autoloop Fáze 3)

## What Was Done This Session

1. **Agent Teams live test** — TeamCreate + 2 Sonnet teammates (Explore agents), parallel skill audit. Windows in-process mode confirmed working. Found: Explore agents can't respond to shutdown_request (lack SendMessage), spawn prompt sufficient (no extra SendMessage needed to start).
2. **TeammateIdle hook** — `teammate-idle.sh` created. Checks: Python syntax, YAML frontmatter, debug artifacts. Exit 2 sends feedback. Wired in settings.json + plugin hooks.json.
3. **disallowedTools audit** — Agent Teams audit found 5 skills missing the field. Fixed: autoloop (Agent), critic (Write, Edit), orchestrate (""), scout (""), watch (""). skill-generator template updated with maxTurns + disallowedTools.
4. **NG-ROBOT sync** — 21 files synced total (15 initial + 6 fixes from audit).
5. **Plugin v1.4.0** — Version bumped from 1.3.0.

## What Remains (for next session)

| # | Item | Priority | Effort | Notes |
|---|------|----------|--------|-------|
| 1 | Autoloop Fáze 3 implementation | high | high | Build referenční dataset (5 articles), composite score script, run autoloop on Phase 3 TermVerifier prompt. Best done in NG-ROBOT context. |
| 2 | ~~Agent Teams — Explore shutdown fix~~ | ~~low~~ | ~~low~~ | DONE — All Explore refs replaced with general-purpose in orchestrate + scout skills |
| 3 | git push STOPA + NG-ROBOT | low | trivial | Push commits to remote. |

## Key Context

- All 11 skills now have complete frontmatter: description, model, effort, maxTurns, disallowedTools
- Agent Teams: working on Windows in-process mode. Use general-purpose subagent_type for tasks needing shutdown.
- Plugin v1.4.0 with TeammateIdle hook
- NG-ROBOT fully synced with latest STOPA state
- Autoloop Fáze 3: TermVerifier class is in `claude_processor.py` (line 2621+), two-call approach (Research → Apply)

## Git State

- Branch: main
- Last commit: 7eb918d — feat: Agent Teams live test, TeammateIdle hook, disallowedTools audit, plugin v1.4.0
- 1 commit ahead of origin/main (not pushed)

## Resume Prompt

> Resume work on the STOPA orchestration meta-project. Read: `CLAUDE.md`, `.claude/memory/checkpoint.md`.
>
> Previous session completed 4/5 tasks: Agent Teams live test (working on Windows), TeammateIdle hook, disallowedTools audit (5 fixes), NG-ROBOT sync, plugin v1.4.0.
>
> Remaining: **Autoloop Fáze 3** — build referenční dataset (5 NG-ROBOT articles), composite quality score for TermVerifier, then autoloop iterations on Phase 3 prompt. Work in NG-ROBOT context (`C:\Users\stock\Documents\000_NGM\NG-ROBOT`), TermVerifier class at `claude_processor.py:2621`.
