# STOPA Restructure Plan — 2026-04-14

## Motivace

STOPA měla být self-improving meta-agent. Audit odhalil:
- 65 skills, reálně používáno ~9
- 70 hooks, většina sbírá data která nikdo nečte
- 1 outcome record, 0 failure records — systém se neměří
- skill-usage-tracker nefunguje (sessions.jsonl: skills=0 vždy)
- 778 neprocessovaných raw captures
- 155 learnings (target 70) — overengineered YAML schema
- Cirkulární závislost: self-improvement engine nemá palivo (žádné measurable outcomes)

## Architektonická vize

```
STOPA (meta-agent)              KODER (execution agent)
├── Rozhodování                  ├── Kód napříč projekty
├── Komunikace (TG, mail)        ├── Testy, CI, deployment
├── Memory & knowledge           ├── Bug fixy, features
├── Scheduling & triggers        ├── Refactoring, quality
└── Deleguje → KODER             └── Reportuje → STOPA
```

Realizace: ne jako nový git repo, ale jako persona/profil s vlastním CLAUDE.md.
Handoff přes scheduled tasks / remote triggers.

---

## Fáze 1: Opravit senzory (tento týden)

### 1.1 Opravit skill-usage-tracker ✅ DONE
- [x] Bug: `session-summary.sh` line 35 grepuje `| Skill |` ale activity-log píše `| Skill:name |`
- [x] Fix: Regex změněn na `\| Skill[: ]` v session-summary.sh
- [x] Ověření: syntakticky OK, bude ověřeno při příštím skill invocation

### 1.2 Opravit failure-recorder ✅ DONE
- [x] Bug: failure-recorder.py triggeruje na `Write(**/outcomes/**)`, ale outcome-writer.py píše přes `path.write_text()` (ne Write tool)
- [x] Fix: Integrováno `_record_failure_inline()` přímo do outcome-writer.py — bypass rozbitého triggeru
- [x] failure-recorder.py hook deaktivován (nyní redundantní)

### 1.3 Ořezat hooks ✅ DONE (82 → 57, -25 hooks)
Hooks k deaktivaci (sbírají data bez čtenáře):
- trace-capture.py — trace data nikdo nečte
- session-trace.py — duplicitní s trace-capture
- stagnation-detector.py — detekuje, ale co pak?
- suggest-compact.py — suggesce které se ignorují
- file-read-dedup.py — micro-optimalizace
- uses-tracker.py — inkrementuje uses, ale na to stačí retrieval
- model-perf-tracker.py — sbírá data, nikdo neanalyzuje
- generation-tracker.py — specifický pro nano/klip
- skill-chain-engine.sh — chaining který se nepoužívá
- skill-context-tracker.sh — kontext který nikdo nečte
- impact-tracker.py — sbírá data bez analýzy
- auto-relate.py — automatické relace, questionable quality
- graduation-check.py — duplicitní s evolve
- trigger-engine.py — meta-trigger systém
- eval-trigger.sh — eval se nespouští
- critic-accuracy-tracker.py — sbírá, neanalyzuje

### 1.4 Archivovat mrtvé skills ✅ DONE (65 → 45 skills)
Přesunuto do `.claude/archive/skills/` a `.claude/archive/commands/`:
20 skills archivováno (oba kopie — commands/ i skills/)

### 1.5 Batch zpracování raw captures ✅ DONE (781 → 179)
- [x] 602 captures starší než 2 dny přesunuto do raw/archive/
- [x] Ponecháno 179 recent captures (13.-14. dubna)

---

## Fáze 2: Rozdělit STOPA a KODER (příští týden)

### 2.1 STOPA profil (zůstává)
Skills:
- orchestrate, triage, council, brainstorm, scenario
- scribe, evolve, dreams, compile, ingest, capture, brain-capture
- watch, radar, deepresearch, fetch, browse
- checkpoint, handoff, compact, status, budget, sweep
- discover, learn-from-failure
- nano, klip (generativní)

Hooks: ~30 (po ořezu z Fáze 1)

### 2.2 KODER profil (nový)
Skills přesunuté ze STOPA:
- fix-issue, autofix, tdd, generate-tests, reproduce
- critic, verify, security-review, dependency-audit
- autoloop, autoresearch, self-evolve, autoreason, autoharness
- project-sweep, xsearch

Vlastní CLAUDE.md s:
- Zaměření na execution, ne na rozhodování
- Přístup ke všem projektům (NG-ROBOT, ADOBE-AUTOMAT, test1, ZACHVEV, POLYBOT)
- Outcome-writing povinné po každém tasku
- Jednodušší memory (žádné 20-field YAML learnings)

### 2.3 Handoff protokol
```
STOPA vytvoří task:
  → .claude/tasks/koder-queue/<date>-<task-id>.md
  → Obsah: co, proč, v jakém projektu, acceptance criteria
  → Trigger: scheduled task nebo manuální /koder <task>

KODER zpracuje:
  → Čte task z queue
  → Provede v cílovém projektu
  → Zapíše outcome do STOPA .claude/memory/outcomes/
  → Commitne a reportuje

STOPA vyhodnotí:
  → Čte outcome
  → Aktualizuje learnings
  → Případně re-assignuje pokud FAIL
```

---

## Fáze 3: Jeden měřitelný feedback loop (za 2 týdny)

### Vybraný workflow: watch → ingest → actionable learnings

**Baseline metrika:** Kolik % z watch findings vede k actionable změně (commit, skill update, decision)
- Odhad baseline: ~10%
- Cíl: 50% do konce dubna

**Jak měřit:**
1. watch generuje findings do news.md
2. Tagovat každý finding: actionable=yes/no
3. Sledovat kolik actionable findings vedlo k reálné akci (commit, learning, decision)
4. Weekly report: actionable_rate = acted / total_actionable

**Self-evolve loop:**
- self-evolve na watch skill s KPI = actionable_rate
- self-evolve na ingest skill s KPI = learning_quality (measured by uses/harmful_uses)

---

## Skill klasifikace (reference)

### CORE (9) — ponechat
orchestrate, scout, critic, checkpoint, deepresearch, watch, scribe, fetch, ingest

### INFRASTRUCTURE (7) — ponechat
evolve, dreams, compile, status, budget, sweep, compact

### SPÍCÍ s potenciálem (13) — probudit v Fázi 2-3
autoloop, self-evolve, autoresearch, autoreason, autoharness,
learn-from-failure, eval, discover, council, scenario, prompt-evolve, radar, harness

### MRTVÉ (20) — archivovat v Fázi 1.4
project-init, build-project, design, recipe, prp, reproduce, generate-tests,
tdd, dependency-audit, security-review, seo-audit, xsearch, ftip, promote,
clean-writing, incident-runbook, liveprompt, peer-review, pr-review, brain-gmail

### Přesun do KODER (16) — Fáze 2.2
fix-issue, autofix, tdd, generate-tests, reproduce, critic, verify,
security-review, dependency-audit, autoloop, autoresearch, self-evolve,
autoreason, autoharness, project-sweep, xsearch

(Některé skills jsou v obou seznamech — ty co jsou "mrtvé" v STOPA kontextu
ale dávají smysl v KODER kontextu, se přesunou místo archivace.)

---

## Metriky úspěchu

| Metrika | Teď | Cíl (konec dubna) |
|---------|-----|-------------------|
| Skills v STOPA | 65 | ~30 |
| Hooks aktivních | ~70 | ~30 |
| Outcomes/měsíc | 1 | 10+ |
| Failures zachycených | 0 | reálný počet |
| sessions.jsonl skills tracking | broken | working |
| Raw captures backlog | 778 | <50 |
| watch actionable rate | ~10% | 50% |

---

## Session handoff prompts

### Pro Fázi 1.1-1.2 (sensor fix):
```
Pokračuj v STOPA restructure plánu (outputs/stopa-restructure-plan.md).
Fáze 1: Opravit senzory.

Úkol 1: Diagnostikuj proč .claude/memory/sessions.jsonl má vždy skills=0.
Zkontroluj hook .claude/hooks/skill-usage-tracker.sh — jak se triggeruje,
co zapisuje, proč nefunguje. Oprav a ověř na 3 skill invokacích.

Úkol 2: Diagnostikuj proč .claude/memory/failures/ je prázdné.
Zkontroluj hook .claude/hooks/failure-recorder.py — trigger podmínky.
Simuluj failure a ověř záznam.
```

### Pro Fázi 1.3 (hook pruning):
```
Pokračuj v STOPA restructure plánu (outputs/stopa-restructure-plan.md).
Fáze 1.3: Ořezat hooks.

V .claude/settings.json deaktivuj hooks dle seznamu v plánu (sekce 1.3).
Metoda: přesunout do komentáře nebo do separate "disabled-hooks" pole.
Zachovej hook soubory pro případ obnovení.
Po ořezu ověř že systém stále funguje: spusť /status, edituj soubor,
zkontroluj že critic a checkpoint stále fungují.
```

### Pro Fázi 1.4 (skill archivace):
```
Pokračuj v STOPA restructure plánu (outputs/stopa-restructure-plan.md).
Fáze 1.4: Archivovat mrtvé skills.

Vytvoř .claude/archive/skills/ a přesuň 20 skills dle seznamu v plánu.
Pro KAŽDÝ skill: přesuň commands/<name>.md i skills/<name>/ do archive.
Nemazat — jen přesunout. Po přesunu ověř že zbývající skills fungují.
```

### Pro Fázi 2 (STOPA/KODER split):
```
Pokračuj v STOPA restructure plánu (outputs/stopa-restructure-plan.md).
Fáze 2: Rozdělit STOPA a KODER.

Vytvoř KODER profil jako nový adresář v STOPA:
  koder/
  ├── CLAUDE.md (execution-focused instrukce)
  ├── skills/ (přesunuté execution skills)
  └── templates/task-template.md

KODER CLAUDE.md musí obsahovat:
- Zaměření na execution (kód, testy, deployment)
- Povinný outcome zápis po každém tasku
- Přístup ke všem cílovým projektům
- Jednodušší memory model

Definuj handoff protokol: STOPA → task queue → KODER → outcome.
```
