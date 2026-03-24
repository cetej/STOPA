# Session Checkpoint

**Saved**: 2026-03-24
**Task**: Agent Teams upgrade z videa Nate Herk (Wave 1-2 continuity)
**Branch**: main
**Commits**: 5e69118 (pushed)
**Status**: COMPLETE ✓

## What Was Done This Session

- **YouTube transkript**: "How to Build Claude Agent Teams Better Than 99% of People" (Nate Herk, 16:29)
  - Extracted 3 praktické vzory: TeamCreate standard tier, spawn template, clean shutdown
  - Transkript: `input/vDVSGVpB2vc_transcript.txt` (22K znaků)

- **Agent Teams upgrade v `/orchestrate` skill**:
  - TeamCreate pro standard tier (3+ subtasks) — decision tree rozšířen
  - **Spawn template**: Goal → Role → Owns → Produces → Communication (30+ řádků)
  - **Clean shutdown protocol**: 5 kroků s retry + timeout (15 řádků)
  - **Plan Approval Mode**: deep tier teammates plánují → lead schvaluje (8 řádků)
  - **Lite vs Full varianta**: tabulka pro standard (4 teammates, bez QA) vs deep (8 teammates, QA)

- **Gotchas +2**: file ownership conflicts, idle agent waste

- **Learning**: MCP youtube-transcript broken → vždy `/youtube-transcript` skill (yt-dlp)

- **Feedback updated**: auto-commit+push po práci, bez potvrzování

**Files**: orchestrate/SKILL.md + gotchas.md × 2 (source + plugin), learnings/2026-03-23-youtube-transcript-yt-dlp.md

## What Remains (Wave 3 roadmap)

| # | Subtask | Tier | Method |
|---|---------|------|--------|
| 1 | Plugin sync v2.0.0 | low | Agent Teams config do stopa-orchestration plugin |
| 2 | Real-world testing | medium | Deploy na NG-ROBOT / ADOBE-AUTOMAT, test standard tier |
| 3 | Wave 3 learnings | medium | Per-file YAML learnings schema + grep-first retrieval |

## Immediate Next Action

Pokud pokračuješ: **Wave 3 learnings migration**. Migruj `learnings.md` (flat, ~142 řádků) do `learnings/` directory s per-learning YAML frontmatter. Vytvoř `critical-patterns.md` (always-read, 10 entries max). Update `/scribe` skill pro nový formát.

## Git State

- **Branch**: main
- **Last commit**: `5e69118 feat: Agent Teams upgrade — standard tier, spawn template, shutdown protocol` ✓ PUSHED
- **Uncommitted**: 4 research files (unrelated z Wave 1-2, ignoruj)

## Key Context

- **Video learnings**: CC v2.1.77+ má Agent Teams nativně, jsou powerful pro 3+ paralelních subtasks
- **Sync status**: `.claude/skills/orchestrate/` ← → `stopa-orchestration/skills/orchestrate/` obě synced
- **Budget intuice**: light (1) < standard (2-4, now 3+ teams) < deep (5-8, teams + QA + plan approval)
- **Approval fatigue**: uživatel chce autonomní commit+push bez otázky po hotové práci

## Resume Prompt

> STOPA — orchestrační systém (source of truth)
> Repo: cetej/STOPA (branch main)
>
> **Poslední session (2026-03-24)**: Agent Teams upgrade z videa Nate Herk ✓ DONE
> - TeamCreate nově pro standard tier (3+ subtasks)
> - Spawn template + clean shutdown protocol + Plan Approval Mode
> - Commit 5e69118 (pushed)
>
> **Zbývá** (Wave 3 roadmap):
> 1. Plugin sync — Agent Teams config do plugin
> 2. Real-world testing — NG-ROBOT / ADOBE-AUTOMAT deployment
> 3. Wave 3 learnings — schema-enforced YAML per-file learnings
>
> **Když resumeš**:
> - Přečti `.claude/CLAUDE.md` + `CLAUDE.md` (projektu)
> - Zkontroluj `.claude/memory/state.md` (aktivní task?)
> - Pokud pokračuješ Wave 3: `research/awesome-claude-code-analysis.md` → Wave 3 sekce
>
> Viz: `research/awesome-claude-code-analysis.md` (kompletní 3-wave roadmap)
