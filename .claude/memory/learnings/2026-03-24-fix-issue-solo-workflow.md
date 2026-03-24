---
date: 2026-03-24
type: workflow
severity: medium
component: skill
tags: [fix-issue, git, solo-development, workflow-simplification]
---

## Problém
/fix-issue skill automaticlaly vytváří feature branch (fix/issue-N), commituje, pushuje, merguje do main, a mažemaže branch. Pro sólo vývojáře to přidává zbytečné složitost (5+ git příkazů namísto 2).

## Root Cause
Skill byl navržen pro týmový workflow s code review (PR potřeba). Solo vývojář bez review nepotřebuje izolaci featurebranch.

## Řešení
U solo projektů: commitovat přímo na main.
- Změna: edit files → `git commit` → `git push` (3 kroky)
- Stačí pro jednu osobu bez review procesu

## Prevence
Při konfiguraci /fix-issue: vždy se ptej "Je to code review potřeba?" Pokud ne → simplified workflow.
