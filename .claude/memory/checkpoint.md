# Session Checkpoint

**Saved**: 2026-03-19
**Task**: Karpathy AutoResearch research + /autoloop skill + news items zapracování
**Branch**: main
**Progress**: All tasks complete — session closing

## What Was Done This Session

- **Karpathy AutoResearch research**: 3 parallel agents researched original concept, community reactions, competing tools. Full synthesis delivered.
- **M5 Hybrid metric design**: Analyzed 5 candidate metrics, selected structural heuristic + 1× LLM validation (22/25 score)
- **`/autoloop` skill created**: Karpathy Loop pattern for autonomous file optimization. 230 lines, built-in SKILL.md scorer.
- **PoC: dependency-audit 12→15/15**: First real autoloop run, 3 iterations, 3 kept.
- **All 11 skills optimized to 15/15**: Batch autoloop across all skills — added error handling, process sections, shortened descriptions, model: fields.
- **Plugin v1.3.0**: git-subdir source type, updated install docs, repeated --plugin-dir note, autoloop + project-init added to manifest.
- **model: field on all skills**: orchestrate→opus, critic→sonnet, skill-generator→sonnet, autoloop→sonnet (others already had it).
- **2 new hooks**: TaskCompleted (auto-scribe reminder), StopFailure (error recovery guidance).
- **2× /watch full scan**: Morning + afternoon. v2.1.79 found (/remote-control, deny fix), FlashAttention-4, ViFeEdit.
- **GitHub push + Google Drive backup**: All committed and pushed. ZIP backup in STOPA-BACKUP/ on GDrive.
- **NG-ROBOT synced**: All skills, hooks, settings, memory synced and committed.

## What Remains (for next session)

| # | Item | Priority | Effort | Notes |
|---|------|----------|--------|-------|
| 1 | `${CLAUDE_PLUGIN_DATA}` persistent state | medium | medium | Design decision: migrate plugin memory from `.claude/memory/` to plugin-specific storage? Needs analysis of what should be shared vs. plugin-local. |
| 2 | Agent Teams native API | high | high | Replace manual Agent() calls in /orchestrate deep tier with native coordination. Needs `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`. Research preview — test stability first. |
| 3 | Remaining hook events | medium | low | InstructionsLoaded, TeammateIdle, Elicitation — decide which are useful for orchestration. |
| 4 | Skills `maxTurns` + `disallowedTools` | low | low | Add per-skill limits. E.g. scout maxTurns:10, budget disallowedTools:[Agent]. |
| 5 | Extended thinking `display: "omitted"` | medium | low | Add to /orchestrate as optimization for deep tier. Saves tokens on thinking blocks. |
| 6 | API code execution pricing | low | low | Update /budget cost estimation — code execution free with web search/fetch. |
| 7 | Autoloop Fáze 2: skill-generator audit integration | medium | medium | Wire autoloop scoring into `/skill-generator audit` so it uses the same M5 metric. |
| 8 | Autoloop Fáze 3: NG-ROBOT pipeline optimization | medium | high | Create referenční dataset + composite score for article processing. |

## Key Context

- STOPA is the meta-project — source of truth for orchestration, distributes to NG-ROBOT, test1, ADOBE-AUTOMAT
- All 11 skills now at 15/15 structural score with model: and effort: fields
- Plugin v1.3.0 with git-subdir source, 11 skills, 5 hooks
- Sync script still works as fallback (`./scripts/sync-orchestration.sh --all --commit`)
- /autoloop is proven (PoC: dependency-audit 12→15 in 3 iterations)
- User is beginner with Claude Code — keep explanations simple

## Git State

- Branch: main
- Uncommitted changes: `.claude/memory/news.md` (minor — news status updates)
- Last commit: `c963df3` feat: zapracování /watch novinek

## Budget State

- No active task budget
- Session total: 3 research agents (Karpathy) + 2 /watch scans

## Resume Prompt

> Resume work on the STOPA orchestration meta-project. Read: `CLAUDE.md`, `.claude/memory/checkpoint.md`, `.claude/memory/news.md`.
>
> Previous session completed: Karpathy AutoResearch research, /autoloop skill creation (proven on all 11 skills → 15/15), plugin v1.3.0 with git-subdir, model: fields on all skills, TaskCompleted + StopFailure hooks, 2× /watch scan.
>
> Remaining work (prioritized):
> 1. **Agent Teams native API** (#2) — replace manual Agent() in /orchestrate deep tier with native coordination. Needs experimental flag testing.
> 2. **`${CLAUDE_PLUGIN_DATA}`** (#1) — design decision: what memory stays in `.claude/memory/` vs. plugin-specific storage?
> 3. **Remaining hook events** (#3) — evaluate InstructionsLoaded, TeammateIdle, Elicitation for orchestration use.
> 4. **Skills maxTurns + disallowedTools** (#4) — add per-skill resource limits.
> 5. **Extended thinking display:omitted** (#5) — token optimization for /orchestrate.
> 6. **Autoloop Fáze 2** (#7) — integrate M5 metric into /skill-generator audit.
> 7. **Autoloop Fáze 3** (#8) — article processing optimization for NG-ROBOT.
>
> All code is on GitHub (cetej/STOPA), synced to NG-ROBOT. Plugin is v1.3.0.
> Key constraint: User is learning Claude Code — keep explanations simple and step-by-step.
