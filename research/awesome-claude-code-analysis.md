# Awesome Claude Code — Competitive Analysis & Adoption Plan

**Datum**: 2026-03-23
**Zdroj**: https://github.com/hesreallyhim/awesome-claude-code (30.7k★)
**Analyzováno**: 7 projektů, 7 paralelních agentů

---

## Executive Summary

Z 200+ projektů v awesome-claude-code bylo vytipováno 7 nejrelevantnějších pro STOPA.
Analýza identifikovala **8 adoptovatelných patterns** seřazených podle impact × feasibility.

### Verdikt per projekt

| Projekt | Stars | Verdict | Hlavní přínos |
|---------|-------|---------|---------------|
| **Context Engineering Kit** | 693 | ✅ ADOPT 3 patterns | Commands-over-skills split, complexity triage, rubric scoring |
| **Trail of Bits Skills** | 3,837 | ✅ ADOPT 3 patterns | Rationalizations to Reject, progressive disclosure, safety gates |
| **Infrastructure Showcase** | 9,317 | ✅ ADOPT 1 pattern | Skill auto-suggest hook (UserPromptSubmit) |
| **Compound Engineering** | 10,924 | ✅ ADOPT 2 patterns | Schema-enforced learnings, staleness refresh |
| **Dippy** | 125 | ✅ ADOPT as tool | AST-based bash auto-approve (replace permission hook) |
| **Session Restore** | — | 📋 STUDY | Git cross-reference v checkpointu (partial adopt) |
| **Parry** | 23 | ❌ SKIP | Windows nepodporuje, early alpha |

---

## Pattern 1: Commands-over-Skills Split (CEK)

### Problém
STOPA má 23 skills. Každý skill s `description` polem auto-loaduje svůj popis do kontextu **každé session**. To je ~2-3k tokenů jen na skill descriptions, i když většina skills se nepoužije.

### Řešení
Rozlišit **skills** (always-present behavior) vs **commands** (on-demand workflows). Skills by měly být jen ty, které genuinně potřebují být vždy aktivní.

### Audit 23 skills → doporučení

| Skill | Typ | Důvod |
|-------|-----|-------|
| `/orchestrate` | ✅ Skill | Tier 1, always-suggest |
| `/scout` | ✅ Skill | Tier 1, always-suggest |
| `/critic` | ✅ Skill | Tier 1, always-suggest |
| `/checkpoint` | ✅ Skill | Tier 1, session management |
| `/scribe` | ✅ Skill | Tier 1, auto-invoked |
| `/verify` | ✅ Skill | Tier 2, auto-invoked po editech |
| `/fix-issue` | ✅ Skill | Tier 2, trigger na GitHub issues |
| `/incident-runbook` | ✅ Skill | Tier 2, trigger na chyby |
| `/brainstorm` | → Command | On-demand, user explicitly asks |
| `/pr-review` | → Command | On-demand, user provides PR |
| `/prp` | → Command | On-demand, context packet |
| `/harness` | → Command | On-demand, specific pipeline |
| `/security-review` | → Command | On-demand |
| `/dependency-audit` | → Command | On-demand |
| `/nano` | → Command | On-demand, creative |
| `/klip` | → Command | On-demand, creative |
| `/skill-generator` | → Command | On-demand, meta |
| `/autoloop` | → Command | On-demand, optimization |
| `/project-init` | → Command | On-demand, one-time |
| `/watch` | → Command | On-demand, weekly |
| `/budget` | → Command | On-demand |
| `/browse` | → Command | On-demand |
| `/youtube-transcript` | → Command | On-demand |
| `/tdd` | → Command | On-demand, methodology |
| `/systematic-debugging` | → Command | On-demand, methodology |

**Výsledek**: 8 skills (always-loaded) + 15 commands (on-demand) = ~60% redukce auto-loaded descriptions.

### Implementace
- Přesunout 15 skills z `.claude/skills/` do `.claude/commands/`
- Commands nemají `description` field → nezatěžují kontext
- Uživatel je invokuje přes `/command-name`
- Skill tier rule updatovat

**Effort**: Medium (přesun souborů + frontmatter úprava)
**Impact**: HIGH — okamžitá redukce tokenů o ~60%

---

## Pattern 2: Rationalizations to Reject (Trail of Bits)

### Problém
Claude má tendenci racionalizovat shortcuts — "tohle nepotřebuje review", "testy by byly overkill", "kód vypadá ok na první pohled". STOPA má anti-rationalization tables v critic, verify, orchestrate (adoptováno z superpowers), ale Trail of Bits má propracovanější systém.

### Řešení
Rozšířit anti-rationalization tables o ToB vzor: dvousloupcová tabulka **Rationalization | Why It's Wrong | Required Action**.

### Příklad pro `/critic`:

```markdown
## Rationalizations to Reject

| Rationalization | Why It's Wrong | Required Action |
|-----------------|----------------|-----------------|
| "The change is too small to review" | Small changes cause 40% of production incidents | Review ALL changes, no exceptions |
| "It's just a refactor, no behavior change" | Refactors introduce subtle regressions | Verify with before/after tests |
| "The author is senior, they know what they're doing" | Seniority doesn't prevent bugs | Apply same rigor regardless |
| "We're under time pressure" | Rushed reviews miss critical issues | Flag time pressure, don't reduce quality |
| "It passed CI so it's fine" | CI catches syntax, not logic errors | Review logic independently |
| "Similar code exists elsewhere" | Existing code may also be wrong | Evaluate on merit, not precedent |
```

### Implementace
- Přidat/rozšířit tabulky v `/critic`, `/verify`, `/orchestrate`, `/pr-review`
- Přidat do `/scout` (proti "I already know enough")
- Přidat do `/fix-issue` (proti "quick fix is sufficient")

**Effort**: LOW (text edits v existujících skills)
**Impact**: MEDIUM-HIGH — snižuje hallucinated LGTM

---

## Pattern 3: Complexity Triage (CEK + Trail of Bits)

### Problém
`/critic` a `/orchestrate` běží vždy na plný výkon, i pro triviální změny. To plýtvá tokeny a zpomaluje workflow.

### Řešení
Tři úrovně dle CEK reflexion patternu:

```
QUICK PATH (< 5s):
  Trigger: single file edit, < 20 lines changed, no API/DB changes
  Action: inline check, no subagents

STANDARD PATH:
  Trigger: 2-5 files, logic changes, new functions
  Action: full critic pass, 1 subagent

DEEP PATH:
  Trigger: 6+ files, security/auth/payment, cross-cutting
  Action: multi-agent review, architecture analysis
```

### Implementace
- Přidat decision tree na začátek `/critic` SKILL.md
- Přidat do `/orchestrate` jako budget tier auto-detection
- Přidat do `/verify` (quick syntax check vs full E2E)

**Effort**: LOW (text additions)
**Impact**: HIGH — dramaticky zrychluje jednoduché reviews

---

## Pattern 4: Skill Auto-Suggest Hook (Infrastructure Showcase)

### Problém
STOPA má 23 skills (resp. 8 after split), ale Claude musí sám rozpoznat, který skill použít. Tier system pomáhá, ale není deterministický.

### Řešení
UserPromptSubmit hook, který analyzuje user prompt a doporučí relevantní skills.

### Architektura (Python, ne TypeScript — Windows kompatibilita)

```python
# .claude/hooks/skill-suggest.py
import json, sys, re

RULES = {
    "orchestrate": {
        "keywords": ["plan this", "break down", "complex task", "rozlož", "naplánuj"],
        "patterns": [r"(implement|add|create|build).{5,30}(feature|system|module)"],
        "tier": "critical"
    },
    "scout": {
        "keywords": ["what do we have", "map this", "scope this", "co máme"],
        "patterns": [r"(explore|understand|find).{5,30}(codebase|code|architecture)"],
        "tier": "high"
    },
    # ... 6 dalších skills
}

def suggest(prompt):
    matches = []
    prompt_lower = prompt.lower()
    for skill, rule in RULES.items():
        if any(kw in prompt_lower for kw in rule["keywords"]):
            matches.append((skill, rule["tier"]))
        elif any(re.search(p, prompt_lower) for p in rule["patterns"]):
            matches.append((skill, rule["tier"]))
    return matches

hook_input = json.load(sys.stdin)
prompt = hook_input.get("message", {}).get("content", "")
matches = suggest(prompt)
if matches:
    lines = [f"💡 Suggested: /{s} [{t}]" for s, t in matches[:3]]
    print(json.dumps({"additionalContext": "\n".join(lines)}))
```

### Implementace
1. Vytvořit `skill-rules.json` s keywords/patterns per skill
2. Python hook script (~50 řádků)
3. Registrovat v `settings.json` jako UserPromptSubmit hook
4. České + anglické triggery

**Effort**: MEDIUM (nový hook + rules JSON)
**Impact**: HIGH — proaktivní skill suggestions bez manuálního /help

---

## Pattern 5: Weighted Rubric Scoring pro /critic (CEK)

### Problém
`/critic` produkuje free-form text. Není jasné, zda je výsledek PASS nebo FAIL, ani jak závažné jsou problémy.

### Řešení
Explicitní rubrika s váhami (inspirace CEK reflexion + ToB fp-check):

```markdown
## Scoring Rubric

| Criteria | Weight | Score (1-5) |
|----------|--------|-------------|
| Correctness (logic, edge cases) | 0.30 | ? |
| Completeness (all requirements met) | 0.25 | ? |
| Code Quality (readability, patterns) | 0.20 | ? |
| Safety (no regressions, no security holes) | 0.15 | ? |
| Test Coverage (adequate tests) | 0.10 | ? |

**Default score: 2** — require evidence to score higher.
**PASS threshold: weighted avg ≥ 3.5**
**FAIL threshold: any criteria < 2 OR weighted avg < 3.0**
```

### Implementace
- Přidat rubric section do `/critic` SKILL.md
- Výstup critic vždy obsahuje filled tabulku + PASS/FAIL verdict
- `/orchestrate` parsuje verdict pro rozhodování

**Effort**: LOW (text addition + output format)
**Impact**: MEDIUM-HIGH — objektivní měřitelnost kvality

---

## Pattern 6: Schema-Enforced Learnings (Compound Engineering)

### Problém
`learnings.md` je flat append-only soubor (~142 řádků). Není queryable, záznamy nemají strukturovaná pole, retrieval je "přečti posledních 10".

### Řešení
Přejít z flat souboru na **per-learning soubory** s YAML frontmatter. Zachovat jednoduchost (ne Rails-specific schema jako Compound).

### Schema pro STOPA:

```yaml
---
date: 2026-03-23
type: bug_fix | architecture | anti_pattern | best_practice | workflow
severity: critical | high | medium | low
component: skill | hook | memory | orchestration | pipeline | general
tags: [tag1, tag2]
---

## Problém
Co se stalo.

## Root Cause
Proč se to stalo.

## Řešení
Co pomohlo.

## Prevence
Jak tomu příště předejít.
```

### Struktura:
```
.claude/memory/learnings/
├── critical-patterns.md    ← always-read (max 10 entries)
├── 2026-03-23-skill-description-shortcut.md
├── 2026-03-22-hook-timeout-issue.md
└── ...
```

### Retrieval (v /scout, /orchestrate, /scribe):
1. Vždy přečti `critical-patterns.md`
2. Grep frontmatter `component:` a `tags:` pro task-relevant matches
3. Přečti jen matched soubory

### Implementace
1. Vytvořit `learnings/` directory
2. Migrovat existujících ~142 řádků do per-file formátu
3. Updatovat `/scribe` pro nový formát
4. Přidat grep-first retrieval do `/scout` a `/orchestrate`
5. Přidat `/scribe maintenance` pro staleness check

**Effort**: HIGH (migration + skill updates)
**Impact**: HIGH — škálovatelný knowledge base, queryable

---

## Pattern 7: Dippy — AST-Based Permission Auto-Approve

### Problém
STOPA má `permission-auto-approve` hook (pravděpodobně regex-based). Regex hooks:
- Nechytí injection přes command substitution (`git $(echo push)`)
- False positives na legitimní pipelines
- Neumí per-subcommand granularitu (`git stash list` vs `git stash drop`)

### Řešení
Nahradit existující permission hook Dippy (`pip install dippy`).

### Výhody Dippy:
- Full bash AST parser (recursive descent, 428KB Parable engine)
- 150+ safe commands auto-approved (read-only ops)
- 80+ CLI-specific handlers (git, docker, aws, npm, kubectl subcommand-level)
- Redirect detection (`curl x > .env` → ask)
- Injection detection (`git $(echo rm)` → ask)
- 14,000+ testů, Beta quality
- Per-project `.dippy` config pro custom rules
- Zero external dependencies (pure Python stdlib)

### Integrace:
```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{ "type": "command", "command": "dippy" }]
    }]
  }
}
```

Per-project `.dippy` file pro STOPA:
```
# Allow common STOPA operations
allow git log **
allow git diff **
allow python -c "import *"
allow pip install dippy

# Block dangerous
deny rm -rf / "Never delete root"
deny-redirect **/.env* "Never write to .env files"
```

### Implementace
1. `pip install dippy`
2. Nahradit stávající permission-auto-approve hook
3. Vytvořit `.dippy` config pro STOPA
4. Otestovat na běžných workflow

**Effort**: LOW (install + config)
**Impact**: MEDIUM-HIGH — bezpečnější auto-approve s nižšími false positives

---

## Pattern 8: Git Cross-Reference v /checkpoint (Session Restore)

### Problém
`/checkpoint` ukládá stav session, ale nekontroluje co je skutečně commitnuto vs. co je WIP.

### Řešení
Přidat krok do `/checkpoint`: po uložení stavu spustit `git log --oneline --since="8 hours ago"` a `git status` pro cross-reference.

### Doplnění do checkpoint SKILL.md:

```markdown
## Step: Git Cross-Reference
After saving session state:
1. Run `git log --oneline --since="8 hours ago"` to list commits from this session
2. Run `git status` to identify uncommitted changes
3. In the checkpoint file, separate:
   - **Committed work**: list of commits with one-line descriptions
   - **Uncommitted WIP**: list of modified/untracked files
   - **Next steps**: what needs to be done with the WIP
```

**Effort**: VERY LOW (text addition to skill)
**Impact**: MEDIUM — lepší session continuity

---

## Implementační Roadmap

### Wave 1 — Quick Wins (effort: LOW, 1 session)
1. ✅ Pattern 2: Rationalizations to Reject → rozšířit tabulky v critic, verify, orchestrate
2. ✅ Pattern 3: Complexity Triage → přidat decision tree do critic, orchestrate
3. ✅ Pattern 5: Weighted Rubric Scoring → přidat do critic
4. ✅ Pattern 8: Git Cross-Reference → doplnit checkpoint

### Wave 2 — Medium Effort (1-2 sessions)
5. Pattern 7: Dippy install + config
6. Pattern 4: Skill Auto-Suggest hook (Python)
7. Pattern 1: Commands-over-Skills split (15 skills → commands)

### Wave 3 — Structural (2-3 sessions)
8. Pattern 6: Schema-Enforced Learnings migration

---

## Projekty k monitorování

| Projekt | Proč | Kdy znovu |
|---------|------|-----------|
| **Parry** | Prompt injection scanner, čeká na Windows support | Check v1.0 |
| **Session Restore** | Rust binary pro JSONL parsing | Pokud potřeba sofistikovanější checkpoint |
| **Claude Squad** | Multi-agent terminal orchestration | Pokud STOPA potřebuje parallel sessions |
| **Compound Engineering** | Schema evolution, new agents | Monthly check |
| **Trail of Bits** | New security skills, workflow-skill-design updates | Monthly check |
