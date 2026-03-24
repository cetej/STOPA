# Plugin v2.0.0 — Test Plan pro cílové projekty

**Datum**: 2026-03-23
**Plugin verze**: 2.0.0 (commit 801f80a)
**Co se změnilo od v1.9.0**: Wave 1-3 z awesome-claude-code analýzy

---

## Přehled změn k otestování

| # | Změna | Dopad | Priorita |
|---|-------|-------|----------|
| 1 | Commands-over-Skills split (8+17) | Token reduction ~60% | HIGH |
| 2 | Complexity Triage v /critic | QUICK/STANDARD/DEEP routing | MEDIUM |
| 3 | Weighted Rubric Scoring v /critic | 5 criteria, PASS ≥ 3.5 | MEDIUM |
| 4 | Rationalizations to Reject (critic, verify, orchestrate) | Anti-shortcut defense | LOW (passive) |
| 5 | Git Cross-Reference v /checkpoint | Committed vs WIP tracking | LOW |
| 6 | Dippy AST bash auto-approve | Auto-approve safe bash commands | HIGH |
| 7 | Skill Auto-Suggest hook | Keyword-based skill suggestion | MEDIUM |
| 8 | Schema-Enforced Learnings | Per-file YAML + grep-first retrieval | MEDIUM |

---

## NG-ROBOT — Testovací zadání

**Projekt**: Desktop aplikace, hlavní vývojový projekt
**Repo**: https://github.com/cetej/NG-ROBOT
**Charakteristika**: Komplexní, multi-file, Python + JS

### Příprava

```bash
# V NG-ROBOT projektu — aktualizuj plugin referenci v .claude/settings.json:
# Ověř že enabledPlugins obsahuje "stopa-orchestration@stopa-tools": true
# Restartuj Claude Code session
```

### Test 1: Plugin install & token reduction (HIGH)
**Cíl**: Ověřit že se loaduje jen 8 skills, ne 25

1. Spusť novou session v NG-ROBOT
2. Napiš: "jaké skills máš k dispozici?"
3. **Očekávání**: Vypíše 8 skills (orchestrate, scout, critic, scribe, checkpoint, verify, fix-issue, incident-runbook)
4. Napiš: "/brainstorm" — mělo by fungovat jako command (on-demand)
5. **PASS pokud**: 8 skills v kontextu, commands fungují on-demand

### Test 2: Dippy auto-approve (HIGH)
**Cíl**: Ověřit že bezpečné bash příkazy se auto-schválí

1. Požádej o: "spusť git status"
2. **Očekávání**: Příkaz proběhne bez permission promptu
3. Požádej o: "spusť python script.py" (nějaký existující)
4. **Očekávání**: Příkaz proběhne bez permission promptu
5. Požádej o: "smaž soubor X" (destruktivní)
6. **Očekávání**: Permission prompt SE zobrazí (Dippy neschválí)
7. **PASS pokud**: Safe commands auto-approved, destructive commands blocked
8. **Prerekvizita**: `pip install git+https://github.com/ldayton/Dippy.git` (NE PyPI "dippy"!)

### Test 3: Skill Auto-Suggest (MEDIUM)
**Cíl**: Ověřit že hook navrhuje relevantní skills

1. Napiš: "potřebuju naplánovat velkou změnu v auth modulu"
2. **Očekávání**: Hook navrhne `/orchestrate` nebo `/scout`
3. Napiš: "je v tom bug, nefunguje to"
4. **Očekávání**: Hook navrhne `/incident-runbook` nebo `/systematic-debugging`
5. **PASS pokud**: Relevantní návrhy, ne spam

### Test 4: /critic s Complexity Triage (MEDIUM)
**Cíl**: Ověřit QUICK/STANDARD/DEEP routing

1. Udělej triviální edit (jeden řádek, jeden soubor)
2. Spusť `/critic`
3. **Očekávání**: QUICK mode (1 min, povrchový review)
4. Udělej větší edit (3+ soubory)
5. Spusť `/critic`
6. **Očekávání**: STANDARD nebo DEEP mode, rubric scoring tabulka ve výstupu
7. **PASS pokud**: Triage odpovídá scope, rubric scoring viditelný

### Test 5: Learnings grep-first retrieval (MEDIUM)
**Cíl**: Ověřit že /scout a /orchestrate používají grep-first

1. Vytvoř testovací learning v `.claude/memory/learnings/`:
   ```
   ---
   date: 2026-03-23
   type: best_practice
   severity: high
   component: general
   tags: [ng-robot, auth, test]
   ---
   ## Problém
   Test learning pro NG-ROBOT.
   ## Řešení
   Toto je testovací záznam.
   ```
2. Spusť `/scout auth modul`
3. **Očekávání**: Scout zmíní nebo aplikuje testovací learning (grep by měl matchnout `tags:.*auth`)
4. **PASS pokud**: Learning nalezen a zmíněn v scout reportu

### Test 6: /checkpoint s Git Cross-Reference (LOW)
**Cíl**: Ověřit committed vs WIP tracking

1. Udělej nějakou práci (edituj soubory, commitni část)
2. Spusť `/checkpoint save`
3. **Očekávání**: Checkpoint rozlišuje committed work vs uncommitted WIP
4. **PASS pokud**: Committed Work a Uncommitted WIP sekce v checkpointu

---

## ADOBE-AUTOMAT — Testovací zadání

**Projekt**: Adobe automatizace (ExtendScript, Python orchestrace)
**Repo**: https://github.com/cetej/ADOBE-AUTOMAT
**Charakteristika**: Menší projekt, specifický tech stack

### Příprava

Stejná jako NG-ROBOT — ověř plugin referenci v settings.json.

### Test 1: Plugin install & commands (HIGH)
Stejný jako NG-ROBOT Test 1. Ověř 8 skills + 17 commands.

### Test 2: Dippy auto-approve (HIGH)
Stejný jako NG-ROBOT Test 2. Ověř safe/destructive routing.

### Test 3: /orchestrate na reálném tasku (MEDIUM)
**Cíl**: End-to-end orchestrace na skutečném úkolu

1. Vyber reálný task pro ADOBE-AUTOMAT (bug fix nebo small feature)
2. Spusť `/orchestrate <task>`
3. **Sleduj**:
   - Complexity tier assignment (light/standard/deep)
   - Grep-first learnings retrieval
   - Subtask decomposition
   - Budget tracking
   - Critic s rubric scoring
4. **PASS pokud**: Celý flow proběhne bez manuálních zásahů

### Test 4: Skill-suggest v kontextu Adobe (MEDIUM)
**Cíl**: Ověřit skill-suggest s doménovými klíčovými slovy

1. Napiš: "ExtendScript padá při exportu PDF"
2. **Očekávání**: Hook navrhne `/incident-runbook` nebo `/systematic-debugging`
3. Napiš: "potřebuju review PR #X"
4. **Očekávání**: Hook navrhne `/pr-review`
5. **PASS pokud**: Relevantní návrhy

---

## Společné post-testy (oba projekty)

### Regrese check
Po všech testech ověř:
- [ ] Session start hook chain funguje (checkpoint-check → memory-maintenance → memory-brief)
- [ ] Activity log se zapisuje (PostToolUse)
- [ ] Ruff lint funguje na Python souborech (PostToolUse Write|Edit)
- [ ] Stop hook (scribe-reminder) funguje
- [ ] Memory soubory nepřekročily 500 řádků

### Srovnání s v1.9.0
- [ ] Token usage per session nižší (kontroluj v budget.md)
- [ ] Žádné chybějící skills/commands (nic se neztratilo při migraci)
- [ ] Hooks neblokují session start (timeout 5s dodržen)

---

## Verdikt

| Test | NG-ROBOT | ADOBE-AUTOMAT |
|------|----------|---------------|
| Plugin install | | |
| Dippy | | |
| Skill-suggest | | |
| Critic triage | | |
| Learnings retrieval | | |
| Checkpoint git-ref | | |
| Orchestrate e2e | — | |
| Regressions | | |

**PASS**: Všechny HIGH testy projdou + žádná regrese
**PARTIAL**: HIGH projdou, MEDIUM mají issues → fix a re-test
**FAIL**: HIGH testy selhávají → rollback na v1.9.0, debug v STOPA
