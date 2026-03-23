# Session Checkpoint

**Saved**: 2026-03-23
**Task**: Awesome Claude Code competitive analysis + pattern adoption (Wave 1-2)
**Branch**: main
**Repo**: https://github.com/cetej/STOPA
**Status**: Wave 1 + Wave 2 kompletní. Wave 3 pending.

## What Was Done This Session

- Competitive analysis 7 projektů z awesome-claude-code (30.7k★) — 7 paralelních research agentů
- Research dokument: `research/awesome-claude-code-analysis.md` (8 patterns, 3 waves)
- **Wave 1** (4 skill improvements):
  - Complexity Triage (QUICK/STANDARD/DEEP) v `/critic`
  - Weighted Rubric Scoring (5 criteria, PASS ≥ 3.5) v `/critic`
  - Rozšířené Rationalizations to Reject v `/critic` (10), `/verify` (8), `/orchestrate` (8)
  - Git Cross-Reference v `/checkpoint` (committed vs WIP)
- **Wave 2** (3 structural changes):
  - Dippy v0.2.7 AST-based bash auto-approve (PreToolUse hook)
  - Skill Auto-Suggest hook (UserPromptSubmit, Python, keyword+regex)
  - Commands-over-Skills split: 8 skills + 17 commands (~60% token reduction)

## What Remains

| # | Subtask | Status | Method |
|---|---------|--------|--------|
| 1 | Wave 3: Schema-Enforced Learnings | pending | Migration learnings.md → per-file YAML + grep-first retrieval |
| 2 | Plugin sync (v2.0.0) | pending | Sync commands + skills to stopa-orchestration plugin |
| 3 | Reálné testování na NG-ROBOT/ADOBE-AUTOMAT | pending | Deploy + verify on target projects |

## Immediate Next Action

Wave 3: Migrate `learnings.md` (flat, ~142 řádků) to `learnings/` directory with per-learning YAML frontmatter files. Create `critical-patterns.md` always-read file. Update `/scribe` skill for new format.

## Key Context

- Commands-over-Skills z CEK — skills auto-load descriptions, commands don't
- Dippy install: `pip install git+https://github.com/ldayton/Dippy.git` (PyPI "dippy" je jiný!)
- Skill-suggest hook: `.claude/hooks/skill-suggest.py` + `skill-rules.json`
- Plugin NENÍ synchronizován s Wave 2 změnami
- Parry (injection scanner) přeskočen — Windows nepodporuje

## Committed Work

```
0a1a1f8 feat: Wave 2 — Dippy, skill-suggest hook, commands-over-skills split
aae9789 feat: Wave 1 — 4 patterns z awesome-claude-code analýzy
```

## Uncommitted WIP

3 unrelated research files (cascade-monitor, claude-thinking, crucix-integration)

## System State

- **8 skills**: checkpoint, critic, fix-issue, incident-runbook, orchestrate, scout, scribe, verify
- **17 commands**: autoloop, brainstorm, browse, budget, dependency-audit, harness, klip, nano, pr-review, project-init, prp, security-review, skill-generator, systematic-debugging, tdd, watch, youtube-transcript
- **14 hooks**: +dippy (PreToolUse/Bash), +skill-suggest (UserPromptSubmit)
- **4 rules**: python-files, skill-files, memory-files, skill-tiers

## Resume Prompt

> STOPA — orchestrační systém, source of truth.
> Repo: cetej/STOPA (branch main), dir: `C:\Users\stock\Documents\000_NGM\STOPA`
>
> Systém: 8 skills, 17 commands, 14 hooks, 4 rules.
> Wave 1+2 z awesome-claude-code analýzy kompletní (commit `0a1a1f8`).
>
> **Nové od v1.9.0:**
> - Complexity Triage + Weighted Rubric Scoring v `/critic`
> - Rationalizations to Reject rozšířeny (critic, verify, orchestrate)
> - Git Cross-Reference v `/checkpoint`
> - Dippy v0.2.7 AST bash auto-approve (PreToolUse hook)
> - Skill Auto-Suggest hook (UserPromptSubmit)
> - Commands-over-Skills split (8 skills + 17 commands, ~60% token reduction)
>
> **Další kroky:**
> 1. **Wave 3**: Schema-Enforced Learnings — migrate learnings.md → per-file YAML frontmatter + grep-first retrieval + critical-patterns.md
> 2. **Plugin sync v2.0.0** — sync commands + skills structure to stopa-orchestration plugin
> 3. **Reálné testování** na NG-ROBOT nebo ADOBE-AUTOMAT
>
> Viz: `research/awesome-claude-code-analysis.md` pro kompletní roadmap.
> Viz: `.claude/memory/checkpoint.md` pro detailní stav.
