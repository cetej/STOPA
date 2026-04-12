# Intelligence Architecture — Od hierarchie k inteligenci

**Inspirace:** Block "From Hierarchy to Intelligence" (2026-04-11)
**Cíl:** Transformovat STOPA z reaktivního skill systému na proaktivní intelligence layer s compound feedback loops.

---

## Současný stav vs. cílový stav

| Dimenze | Dnes | Cíl |
|---------|------|-----|
| Skill invokace | Reaktivní (uživatel volá) | Proaktivní (systém rozpozná moment) |
| Outcome data | 1 záznam (sparse) | Každý skill run zanechá stopu |
| Failure → Learning | Manuální /learn-from-failure | Auto-trigger po 2+ same-class |
| World model | Fragmentovaný (12 souborů, per-project) | Unified pulse + cross-project view |
| Roadmap | Uživatel vymýšlí co dál | Capability gaps generují backlog |
| Signal quality | Corrections (negative-only) | Dual-trace: success + failure |
| Feedback latency | Session-end (scribe) | Real-time (hooks) |

---

## Fáze implementace

### Fáze 1: Signal Foundation (effort: low, impact: high)
**Cíl:** Každý skill run generuje outcome signal. Bez dat nemá intelligence co zpracovávat.

### Fáze 2: Trigger Intelligence (effort: medium, impact: high)
**Cíl:** Systém rozpozná vzory v signálech a automaticky spustí akce.

### Fáze 3: Unified World Model (effort: medium, impact: medium)
**Cíl:** Single-read artifact o stavu celého systému across projektů.

### Fáze 4: Proactive Composition (effort: high, impact: high)
**Cíl:** Intelligence layer navrhuje akce na základě momentu, ne na základě user invokace.

### Fáze 5: Capability Gap Detection (effort: low, impact: medium)
**Cíl:** Systém identifikuje co chybí a generuje vlastní backlog.

---

## Fáze 1: Signal Foundation

### Problém
Outcome recording existuje jako infrastruktura (hook outcome-credit.py, failure-recorder.py, formát v memory-files.md), ale adoption je téměř nulová — 1 záznam za 40+ sessions. Skills nemají povinnost outcome zapsat. Bez dat je vše ostatní mrtvé.

### Řešení: Lightweight outcome obligation

**Princip:** Outcome zápis musí být tak levný, že nemá cenu ho přeskočit. Ne plný outcome soubor (32 řádků), ale minimal signal (5 řádků).

#### 1.1 Minimal Outcome Format (micro-outcome)

```yaml
---
skill: orchestrate
date: 2026-04-11
outcome: success
exit_reason: convergence
one_line: "3 subtasks, all PASS, no replans needed"
---
```

5 řádků. Žádný trajectory, žádné learnings_applied. To je pro skills které nemají iterativní loop (orchestrate, scout, critic, triage, brainstorm). Iterativní skills (autoloop, self-evolve, autoresearch) zapisují full outcome jako dosud.

#### 1.2 PostSkillRun Hook — `outcome-writer.py`

**Trigger:** PostToolUse na Skill tool (již existuje skill-usage-tracker)
**Logika:**
1. Detekuj skill name z tool result
2. Detekuj outcome status z posledního výstupu (regex: PASS/FAIL/DONE/BLOCKED/partial)
3. Zapiš micro-outcome do `.claude/memory/outcomes/YYYY-MM-DD-<skill>-<outcome>-<N>.md`
4. Pokud detekce selže → nezapiš nic (ne-blocking, best-effort)

**Klíčové rozhodnutí:** Hook vs. in-skill obligation?
- Hook: automatické, žádná změna skills, ale heuristic detection (nepřesné)
- In-skill: přesné, ale vyžaduje edit 50 skills

**Verdikt:** Hybrid approach.
- Hook detekuje a zapíše micro-outcome (best-effort, ~70% accuracy)
- Tier 1+2 skills dostanou explicitní instrukci v SKILL.md: "Write outcome" na konci
- Postupně: skill-chain-engine.json přidá "write outcome" jako implicitní krok po každém skillu

#### 1.3 Outcome Aggregator — `outcomes-summary.json`

Rolling summary aktualizovaný hookem po každém outcome write:
```json
{
  "last_updated": "2026-04-11",
  "total_runs": 47,
  "success_rate": 0.78,
  "by_skill": {
    "orchestrate": {"runs": 12, "success": 10, "partial": 1, "failure": 1},
    "critic": {"runs": 8, "success": 7, "failure": 1}
  },
  "by_exit_reason": {
    "convergence": 25,
    "budget_exceeded": 3,
    "crash_loop": 2
  },
  "last_7_days": {"success": 15, "partial": 2, "failure": 1},
  "failure_streak": 0
}
```

Účel: `/status` čte tento jediný soubor místo scannování celé outcomes/ directory.

#### 1.4 Success Metrics pro Fázi 1

| Metrika | Baseline | Target |
|---------|----------|--------|
| Outcomes per session | 0.025 (1/40) | ≥3 |
| Skills s outcome coverage | 1 (self-evolve) | ≥10 Tier 1+2 |
| Aggregate JSON accuracy | N/A | Updated after every skill run |

#### 1.5 Implementační kroky

1. Vytvořit `outcome-writer.py` hook (PostToolUse Skill) — micro-outcome best-effort
2. Vytvořit `outcomes-summary.json` + update logiku v outcome-writer
3. Přidat micro-outcome instrukci do Tier 1 skills (orchestrate, scout, critic, checkpoint, scribe, status, triage)
4. Rozšířit skill-chains.json: po každém Tier 2 skill → implicitní outcome write
5. Aktualizovat `/status` aby četl outcomes-summary.json

#### 1.6 Rizika a mitigace

| Riziko | Dopad | Mitigace |
|--------|-------|----------|
| Heuristic detection špatně klasifikuje | Špatná data v aggregátoru | Conservative regex: radši nezapsat než zapsat špatně |
| 78 hooks + nový = latency | Pomalá response | outcome-writer async (fire-and-forget, no blocking) |
| Outcome soubory zaplaví disk | 500+ files | Auto-archive po 100 souborech (jako failures/) |
| Skills ignorují in-skill obligation | Nízká coverage | Hook jako safety net — zachytí i bez explicitního zápisu |

---

## Fáze 2: Trigger Intelligence

### Problém
Dnes: skill-chains.json je statický rule engine (20 pravidel, pattern→next). Reaguje na skill completion, ne na patterns v datech. Chybí: "viděl jsem 3 failures se stejným vzorem → spusť akci" nebo "success rate klesla pod 60% → upozorni".

### Řešení: Event-Condition-Action (ECA) engine

#### 2.1 Trigger Rules Format

```yaml
# .claude/hooks/trigger-rules.yaml
rules:
  - id: failure-pattern-detected
    description: "2+ same-class failures from same agent → auto learn"
    event: outcome_written
    condition:
      type: aggregate_query
      query: "failures with same failure_class AND failure_agent in last 7 days >= 2"
    action:
      type: inject_skill
      skill: "/learn-from-failure --class {failure_class} --agent {failure_agent}"
    cooldown: 24h  # don't re-trigger for same pattern within 24h

  - id: success-rate-drop
    description: "7-day success rate < 60% → alert user"
    event: outcome_written
    condition:
      type: threshold
      metric: "outcomes_summary.last_7_days.success_rate"
      operator: "<"
      value: 0.6
    action:
      type: notify
      message: "System health warning: success rate dropped below 60% ({value}%)"
    cooldown: 48h

  - id: stale-world-model
    description: "No outcomes written in 3+ sessions → remind"
    event: session_start
    condition:
      type: staleness
      file: ".claude/memory/outcomes-summary.json"
      max_age_days: 3
    action:
      type: notify
      message: "World model is stale — no outcomes recorded in {days} days"
    cooldown: 72h

  - id: graduation-ready
    description: "Learning ready for graduation → suggest evolve"
    event: learning_updated
    condition:
      type: threshold
      metric: "learning.uses >= 10 AND learning.confidence >= 0.8"
    action:
      type: notify
      message: "Learning '{filename}' ready for graduation. Consider /evolve."
    cooldown: 168h  # weekly

  - id: capability-gap-repeated
    description: "Same 'no skill matches' pattern 3x → create backlog item"
    event: triage_no_match
    condition:
      type: count
      pattern: "same unmatched query pattern"
      threshold: 3
      window: 30d
    action:
      type: write_file
      target: ".claude/memory/capability-gaps.md"
      content: "- [{date}] Gap: {query_pattern} (triggered {count}x)"
    cooldown: 0  # always write

  - id: compound-success
    description: "5+ consecutive successes → record winning strategy"
    event: outcome_written
    condition:
      type: streak
      metric: "consecutive_successes"
      threshold: 5
    action:
      type: inject_skill
      skill: "/scribe success-pattern"
    cooldown: 168h
```

#### 2.2 Trigger Engine — `trigger-engine.py`

**Trigger:** PostToolUse (outcome writes + learning updates) + SessionStart
**Architektura:**
1. Load rules from `trigger-rules.yaml`
2. On event: evaluate all matching conditions
3. Check cooldown (per-rule state in `trigger-state.json`)
4. Execute action: inject_skill | notify | write_file
5. Log trigger fire to `trigger-log.jsonl`

**Důležité:** Engine je stateless observer — čte outcomes-summary.json a failures/ directory, vyhodnocuje conditions, ale nikdy nemutuje source data.

#### 2.3 Skill Chain Integration

Trigger engine DOPLŇUJE skill-chains.json, nenahrazuje ho:
- **Skill chains** = deterministické: skill A done → vždy spusť B
- **Trigger rules** = condition-based: pattern detected → spusť akci

Oba systémy mohou navrhnout akci. Conflict resolution: skill chain má přednost (deterministic > probabilistic).

#### 2.4 Cooldown & Dedup mechanismus

```json
// trigger-state.json
{
  "failure-pattern-detected": {
    "last_fired": "2026-04-10T14:30:00",
    "context": {"failure_class": "logic", "failure_agent": "agent-worker"},
    "fire_count": 3
  }
}
```

Cooldown je per-rule + per-context. Stejné pravidlo se může triggerovat pro různé kontexty (různý failure_class) bez cooldown konfliktu.

#### 2.5 Success Metrics pro Fázi 2

| Metrika | Baseline | Target |
|---------|----------|--------|
| Auto-triggered actions per week | 0 | ≥5 |
| False positive triggers | N/A | <20% |
| Trigger → resolution latency | manual (hours/days) | <1 session |
| Rules count | 0 | ≥8 production rules |

#### 2.6 Implementační kroky

1. Definovat `trigger-rules.yaml` s 6 initial rules (výše)
2. Implementovat `trigger-engine.py` (PostToolUse hook na outcome/learning writes)
3. Implementovat `trigger-state.json` cooldown tracking
4. Přidat trigger check do SessionStart (pro staleness rules)
5. Rozšířit `/status` o trigger health: last fires, pending conditions
6. Po 2 týdnech: audit trigger accuracy, tune thresholds

#### 2.7 Rizika a mitigace

| Riziko | Dopad | Mitigace |
|--------|-------|----------|
| Trigger spam (příliš mnoho fires) | Alert fatigue | Cooldown + max 3 triggers per session |
| False positive → wrong action | Špatná data, zbytečná práce | Conservative thresholds + notify (ne auto-execute) pro nové rules |
| YAML parsing complexity | Engine bugs | Strict schema validation + unit tests |
| Circular triggers (A triggers B triggers A) | Infinite loop | Max trigger depth = 1 (trigger nemůže triggerovat trigger) |
| Cooldown state corruption | Triggers přestanou fungovat | Fallback: pokud state neparsable, reset |

---

## Fáze 3: Unified World Model

### Problém
Informace o stavu systému je roztříštěná across 12+ souborů, 5+ projektů. Žádný single artifact neposkytuje "co se děje teď, co je health, kde jsou blockers". `/status` čte lokálně per-project. Žádný cross-project view.

### Řešení: System Pulse + Cross-Project Registry

#### 3.1 System Pulse — `pulse.json`

Automaticky aktualizovaný artifact (ne ruční):

```json
{
  "generated": "2026-04-11T15:30:00",
  "projects": {
    "STOPA": {
      "last_activity": "2026-04-11",
      "active_task": "Intelligence Architecture",
      "health": "green",
      "outcomes_7d": {"success": 5, "partial": 1, "failure": 0},
      "open_failures": 0,
      "stale_learnings": 3,
      "budget_remaining": "~$2.50"
    },
    "NG-ROBOT": {
      "last_activity": "2026-04-09",
      "active_task": null,
      "health": "yellow",
      "outcomes_7d": {"success": 2, "partial": 0, "failure": 1},
      "open_failures": 1,
      "stale_learnings": 7,
      "budget_remaining": "~$1.00"
    }
  },
  "system_health": {
    "overall": "green",
    "signal_coverage": 0.45,
    "trigger_fires_7d": 3,
    "graduation_candidates": 2,
    "capability_gaps": 1
  },
  "alerts": [
    {"level": "info", "message": "NG-ROBOT has 1 unresolved failure (logic, agent-worker)"},
    {"level": "warn", "message": "7 stale learnings in NG-ROBOT (>90 days)"}
  ]
}
```

#### 3.2 Pulse Generator — `pulse-generator.py`

**Trigger:** SessionStart + Stop (2x per session min)
**Zdroje:**
- Lokální: outcomes-summary.json, failures/, checkpoint.md, budget.md, state.md
- Cross-project: čte checkpoints z registrovaných projektů (via projects.json path registry)

**Důležité:** Pulse je read-only snapshot. Nikdy nemutuje zdrojové soubory. Generuje se za <2s.

#### 3.3 Project Registry — `projects.json`

```json
{
  "projects": [
    {
      "name": "STOPA",
      "path": "C:/Users/stock/Documents/000_NGM/STOPA",
      "role": "meta",
      "github": "cetej/STOPA"
    },
    {
      "name": "NG-ROBOT",
      "path": "C:/Users/stock/Documents/000_NGM/NG-ROBOT",
      "role": "primary",
      "github": "cetej/NG-ROBOT"
    }
  ]
}
```

Existuje pravděpodobně v `~/.claude/memory/projects.json` (skill-chain reference naznačuje). Pulse generator čte cesty a scanuje `.claude/memory/` v každém projektu.

#### 3.4 `/status --pulse` rozšíření

Místo čtení 12 souborů → čte pulse.json (1 soubor, pre-computed). Přidá cross-project view do výstupu:

```
pulse:          green | 6 success, 1 partial, 0 fail (7d)
cross_project:  STOPA green | NG-ROBOT yellow (1 open failure)
alerts:         1 warn (stale learnings in NG-ROBOT)
```

#### 3.5 Success Metrics pro Fázi 3

| Metrika | Baseline | Target |
|---------|----------|--------|
| Time to understand system state | ~30s (read multiple files) | <5s (read pulse.json) |
| Cross-project visibility | None | All registered projects |
| Stale information detection | Manual | Automatic (pulse alerts) |

#### 3.6 Implementační kroky

1. Ověřit/vytvořit `projects.json` s cestami ke všem projektům
2. Implementovat `pulse-generator.py` (SessionStart hook)
3. Uložit výstup do `~/.claude/memory/pulse.json` (globální, ne per-project)
4. Rozšířit `/status` o `--pulse` mode (čte pulse.json)
5. Přidat pulse alerts do SessionStart outputu (jako evolve-trigger dnes)

#### 3.7 Rizika a mitigace

| Riziko | Dopad | Mitigace |
|--------|-------|----------|
| Cross-project paths neexistují | Pulse nevidí jiné projekty | Graceful fallback: zobraz jen lokální |
| Čtení cizích .claude/ dirs je pomalé | SessionStart lag | Async + cache (regeneruj jen pokud >1h starý) |
| Projekty mají různé memory formáty | Parse errors | Defensive parsing + skip on error |
| Pulse.json stale (session crash) | Misleading info | Timestamp + "stale" alert pokud >24h |

---

## Fáze 4: Proactive Composition

### Problém
Block model: intelligence layer rozpozná moment a složí řešení proaktivně. STOPA: orchestrate čeká na explicitní příkaz, triage vyžaduje dotaz, skills se neinvokují samy.

### Řešení: Ambient Intelligence — Session Advisor

#### 4.1 Koncept

Ne plný autonomní agent (příliš riskantní, nepredikovatelný). Místo toho: **advisor pattern** — systém v pozadí sleduje kontext a na klíčových momentech navrhne akci.

Inspirace: Block nemá plně autonomní AI. Má intelligence layer, která NAVRHUJE složené řešení. Člověk (nebo interface) ho doručí.

#### 4.2 Ambient Advisor Hook — `advisor.py`

**Trigger:** PostToolUse (every N-th call, e.g., every 10th to reduce overhead)
**Vstup:** Aktuální kontext (tool results, file paths, patterns)
**Výstup:** Suggestion injected jako system message (ne blocking)

**Rozhodovací logika:**

```python
def should_advise(context):
    """Vyhodnoť zda je moment pro proaktivní radu."""
    
    # Pattern 1: User dělá manuálně co by skill udělal lépe
    if context.repeated_grep_count > 5 and not context.skill_active:
        return Suggestion("/scout", "Vidím opakovaný manuální grep — /scout by to udělal systematičtěji")
    
    # Pattern 2: Změna ve více souborech bez plánu
    if context.files_edited > 3 and not context.has_todo_list:
        return Suggestion("/orchestrate retrospective", "3+ soubory editovány bez dekompozice")
    
    # Pattern 3: Test failure po editu
    if context.last_bash_exit != 0 and context.last_edit_was_code:
        return Suggestion("/systematic-debugging", "Test fail po editu — root cause first")
    
    # Pattern 4: Session bez outcome záznamu
    if context.session_skills_run > 3 and context.outcomes_this_session == 0:
        return Suggestion("write outcomes", "3+ skills bez outcome — signal se ztrácí")
    
    # Pattern 5: Approaching context limit without checkpoint
    if context.context_usage > 0.7 and not context.checkpoint_saved:
        return Suggestion("/checkpoint save", "Context 70%+ bez checkpointu")
    
    return None
```

#### 4.3 Proaktivní Skill Composition

Vyšší level než advisor (Fáze 4b — implementovat až po validaci 4a):

```yaml
# composition-rules.yaml
compositions:
  - name: "Post-research synthesis"
    trigger:
      event: skill_complete
      skill: deepresearch
      outcome: success
    compose:
      - "/ingest {output_file}"        # Extract entities
      - "/compile --incremental"        # Update wiki
      - "/scribe research-complete"     # Record
    description: "After research, auto-compose ingest+compile+scribe"

  - name: "Failure recovery"
    trigger:
      event: outcome_written
      outcome: failure
      failure_class: logic
    compose:
      - "/reproduce {task}"            # Create failing test
      - "/systematic-debugging"        # Find root cause
    description: "After logic failure, compose repro+debug"
```

Toto je rozšíření skill-chains — místo single next skill, kompozice více skills v sekvenci.

#### 4.4 Boundary: Advise vs. Execute

**Kritické rozhodnutí:** Kdy advisor jen navrhne vs. automaticky spustí?

| Akce | Chování | Důvod |
|------|---------|-------|
| Suggest skill | Jen notify (uživatel potvrdí) | Nechceme přerušit tok |
| Write micro-outcome | Auto-execute | Zero risk, no user impact |
| Trigger /learn-from-failure | Auto-execute | Backround analysis, non-destructive |
| Trigger /checkpoint | Auto-execute | Protective, uživatel chce |
| Trigger /orchestrate | NIKDY auto | High impact, needs user intent |
| Trigger /evolve | Auto (scheduled) | Already has scheduled task |

**Pravidlo:** Auto-execute jen pro idempotentní, non-destructive akce. Vše co mění workflow → suggest only.

#### 4.5 Success Metrics pro Fázi 4

| Metrika | Baseline | Target |
|---------|----------|--------|
| Proactive suggestions per session | 0 | 2-4 (quality over quantity) |
| Suggestion acceptance rate | N/A | >50% |
| False/annoying suggestions | N/A | <1 per session |
| Auto-composed sequences per week | 0 | ≥3 |

#### 4.6 Implementační kroky

**Fáze 4a (Advisor — 2 týdny):**
1. Implementovat `advisor.py` s 5 initial patterns (viz výše)
2. Registrovat jako PostToolUse hook (throttled: every 10th call)
3. Output: system-reminder injection (non-blocking suggestion)
4. Sledovat acceptance rate (user follows suggestion vs. ignores)
5. Tune patterns po 2 týdnech based on acceptance data

**Fáze 4b (Composition — 4 týdny po 4a validaci):**
1. Definovat `composition-rules.yaml` s 3 initial compositions
2. Rozšířit trigger-engine o composition execution
3. Compositions respektují cooldown a budget limits
4. Přidat composition log do pulse.json

#### 4.7 Rizika a mitigace

| Riziko | Dopad | Mitigace |
|--------|-------|----------|
| Advisor je annoying | User frustrace | Max 1 suggestion per 5 min + "dismiss" tracking |
| Suggestions are wrong | Trust erosion | Conservative patterns, high threshold |
| Auto-execute breaks flow | Přerušení práce | Only background tasks (outcome write, checkpoint) |
| Composition creates unexpected work | Budget waste | Budget cap per composition (max 0.5$) |
| Advisor overhead (every 10th call) | Latency | Lightweight check (<100ms), no LLM calls in advisor |

---

## Fáze 5: Capability Gap Detection

### Problém
Block: "When intelligence layer can't compose a solution because capability doesn't exist, that failure signal IS the future roadmap." STOPA: když `/triage` nenajde vhodný skill, jen řekne "no match" a nic se nezapíše.

### Řešení: Gap Registry + Auto-Backlog

#### 5.1 Capability Gap Registry — `capability-gaps.md`

```markdown
# Capability Gaps

Automaticky generovaný backlog — situace kdy systém nemohl pomoci.

| Date | Query/Need | Times | Status | Resolution |
|------|-----------|-------|--------|------------|
| 2026-04-11 | "optimize database schema" | 3 | open | — |
| 2026-04-08 | "generate API docs from code" | 2 | open | — |
| 2026-04-05 | "monitor production errors" | 4 | resolved | Created /incident-runbook |
```

#### 5.2 Gap Detection Points

Kde zachytit "systém nemůže"?

1. **Triage no-match:** `/triage` nenajde odpovídající skill → gap
2. **Orchestrate capability miss:** Orchestrátor potřebuje operaci, kterou žádný skill neumí → gap
3. **User workaround:** Uživatel dělá manuálně (5+ Bash commands pro něco co by měl skill) → potential gap
4. **Repeated manual pattern:** Stejná sekvence akcí opakována 3x across sessions → automation candidate

#### 5.3 Gap Recorder — logika v trigger-engine

```yaml
# In trigger-rules.yaml
- id: triage-no-match
  event: skill_complete
  condition:
    type: output_pattern
    skill: triage
    pattern: "no.*match|žádný skill|unclear|manual"
  action:
    type: append_file
    target: ".claude/memory/capability-gaps.md"
    content: "| {date} | {query} | 1 | open | — |"
  cooldown: 0

- id: gap-threshold
  event: gap_recorded
  condition:
    type: count
    same_pattern: true
    threshold: 3
  action:
    type: notify
    message: "Capability gap '{pattern}' hit 3x — consider creating a skill"
  cooldown: 720h  # monthly
```

#### 5.4 Gap → Skill Pipeline (manuální s asistencí)

Když gap dosáhne threshold (3+ occurrences):
1. System navrhne: "Opakující se potřeba: '{gap}'. Chceš vytvořit skill? (/skill-generator)"
2. Poskytne kontext: co uživatel dělal manuálně v minulých sessions (z trace dat)
3. Uživatel rozhodne: ano → /skill-generator s pre-filled spec, ne → dismiss

#### 5.5 Success Metrics pro Fázi 5

| Metrika | Baseline | Target |
|---------|----------|--------|
| Captured gaps per month | 0 | ≥5 |
| Gaps resolved (new skill created) | 0 | ≥1 per quarter |
| Gap detection accuracy | N/A | >70% (real gaps, ne noise) |
| Time from gap detection to resolution | N/A | <30 days for top gaps |

#### 5.6 Implementační kroky

1. Vytvořit `capability-gaps.md` template
2. Přidat gap detection rule do trigger-rules.yaml
3. Rozšířit `/triage` o explicitní "no match" signál (dnes jen textový výstup)
4. Přidat gap summary do pulse.json
5. Přidat gap-to-skill suggestion do advisor.py (Fáze 4)

#### 5.7 Rizika a mitigace

| Riziko | Dopad | Mitigace |
|--------|-------|----------|
| Noise: vágní queries counted as gaps | Bloated backlog | Min 3 occurrences + similar pattern matching |
| Skill proliferation | Too many skills, hard to maintain | Monthly review: merge related gaps, archive resolved |
| Gap detection misses context | Wrong classification | Capture full query context, not just keywords |

---

## Závislosti mezi fázemi

```
Fáze 1 (Signal) ──────────┐
                           ├──→ Fáze 2 (Triggers) ──→ Fáze 4b (Composition)
Fáze 3 (World Model) ─────┘                    │
                                                ├──→ Fáze 5 (Gap Detection)
                                                │
Fáze 4a (Advisor) ─────────────────────────────┘
```

- **Fáze 1 je prerekvizita pro vše** — bez dat žádná inteligence nefunguje
- **Fáze 2 závisí na Fázi 1** — triggers vyhodnocují outcomes-summary.json
- **Fáze 3 je nezávislá na 2** — může běžet paralelně s Fází 2
- **Fáze 4a je nezávislá** — advisor patterns nevyžadují outcomes (ale benefitují z nich)
- **Fáze 4b závisí na 2** — composition rules jsou rozšíření trigger engine
- **Fáze 5 závisí na 2** — gap detection je special case trigger rule

## Timeline (realistický odhad)

| Fáze | Start | Effort | Deliverable |
|------|-------|--------|-------------|
| 1: Signal Foundation | Ihned | 1-2 sessions | outcome-writer hook + aggregator |
| 3: World Model | Po Fázi 1 | 1 session | pulse-generator + projects.json |
| 2: Trigger Intelligence | Po Fázi 1 | 2-3 sessions | trigger-engine + 6 rules |
| 4a: Advisor | Kdykoliv | 1-2 sessions | advisor.py + 5 patterns |
| 5: Gap Detection | Po Fázi 2 | 1 session | gap registry + triage integration |
| 4b: Composition | Po validaci 4a | 2 sessions | composition-rules + executor |

**Celkově:** ~8-12 sessions rozložených přes 3-4 týdny.

## Validační strategie

Po každé fázi: 1 týden observace bez zásahů. Měříme:
1. Generuje systém data? (Signal coverage)
2. Jsou triggery přesné? (False positive rate)
3. Jsou návrhy užitečné? (Acceptance rate)
4. Zlepšuje se compound výkon? (Success rate trend)

Pokud metrika nesplní target po 1 týdnu → tune, ne nová fáze.

## Architektonická invarianta

**Systém NIKDY nekoná destruktivně proaktivně.**

Proaktivní akce jsou omezeny na:
- Zápis do outcomes/ (append-only)
- Notify uživatele (non-blocking)
- Spuštění read-only analýzy (learn-from-failure, status)
- Zápis do gaps registry (append-only)

NIKDY proaktivně:
- Edit kódu
- Delete souborů
- Git operace
- Skill s side-effects (fix-issue, autofix)
- Budget-heavy operace (deepresearch, build-project)

---

## Shrnutí: Od STOPA 1.0 k STOPA 2.0

| STOPA 1.0 (dnes) | STOPA 2.0 (cíl) |
|-------------------|------------------|
| User → Skill → Result | User → Skill → Result → Outcome → Signal → Trigger → Action |
| Flat skill catalog | Intelligence layer composing skills |
| Per-project state | Cross-project world model |
| Manual maintenance | Self-maintaining (evolve, compile, sweep auto-triggered) |
| Corrections only | Dual-trace (success signals equally valued) |
| Reactive | Ambient (advisor + triggers + compositions) |

Block volá tomuto "company organized as intelligence." My tomu říkáme **orchestrační systém s compound feedback loops**. Princip je stejný: informace generují akce, akce generují informace, loop se zrychluje.
