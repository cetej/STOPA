# Session Checkpoint

**Saved**: 2026-04-03
**Task**: Skill description quality — follow-up from Hassid/Anthropic audit
**Branch**: main
**Last commit**: `a5dc11b` feat: Skill description audit — routing exclusions, conflict resolution, Anthropic alignment

---

## What Was Done (2026-04-03)

1. **Hassid post audit** — ověřena tvrzení o Claude Skills (header-only load: pravda, open standard: nepravda, token savings: neověřitelné)
2. **Skill description opravy** — 24 souborů (12 skill párů): přidány routing exclusions místo slabých usage constraints
3. **Anthropic skill-creator analýza** — identifikovány 3 gapy: description optimizer, 500-line limit, ALWAYS/NEVER refactoring
4. **Learnings zapsány** — anthropic-skill-creator-patterns.md, description-optimizer-plan.md

## What Remains — 3 follow-up tasks

### Task 1: Refaktorovat dlouhé skills (500-line limit)
5 skills překračuje Anthropic doporučený limit:
- **orchestrate**: 1476 řádků (3× přes limit!) → rozdělit do SKILL.md + references/
- **critic**: 637 → extrahovat gotchas/review-patterns do references/
- **autoloop**: 600 → extrahovat tree-mode/meta-mode docs
- **autoresearch**: 599 → extrahovat experiment patterns
- **eval**: 516 → mírně přes, nízká priorita

Postup: zachovat SKILL.md <500 řádků, extrahovat sekce do `references/` s pointery.

### Task 2: ALWAYS/NEVER refactoring
50+ instancí all-caps ALWAYS/NEVER/MUST across skills. Anthropic guideline: "yellow flag — explain why instead."
Top offenders: orchestrate (14), critic (5), tdd (4), autoloop (3), peer-review (3).
Bezpečnostní pravidla (browse, project-init, sweep) ponechat — tam je caps oprávněný.

### Task 3: Description optimizer implementace
Plán v `.claude/memory/learnings/2026-04-03-description-optimizer-plan.md`.
Option B doporučeno: custom STOPA optimizer s conflict pair awareness.
Vstup: skill name + known conflict pairs. Výstup: optimalizovaný description s měřeným trigger/non-trigger rate.

---

## Resume Prompt

> **Task**: Pokračuj ve vylepšování STOPA skills — 3 follow-up úkoly z auditu:
>
> 1. **Refaktorovat orchestrate** (1476→<500 řádků) — extrahovat do references/. Pak critic (637), autoloop (600), autoresearch (599).
> 2. **ALWAYS/NEVER refactoring** — přeformulovat 50+ instancí s vysvětlením "proč" (vynechat bezpečnostní pravidla).
> 3. **Description optimizer** — implementovat dle plánu v learnings/2026-04-03-description-optimizer-plan.md.
>
> **Kontext**: Commit `a5dc11b`. Přečti si learnings/2026-04-03-anthropic-skill-creator-patterns.md pro detaily.
> Zdroj auditu: Hassid post (Twitter) + github.com/anthropics/skills/tree/main/skills/skill-creator.


