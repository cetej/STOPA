# Intelligence Architecture — Zadání pro sessions

**Plán:** `docs/INTELLIGENCE_ARCHITECTURE.md`
**Hotové:** Fáze 1 (Signal Foundation), Fáze 2 (Trigger Intelligence), Fáze 3 (World Model)
**Zbývá:** 3 sessions → 3 fáze

---

## Session A: Trigger Intelligence (Fáze 2)

**Prerekvizita:** outcomes-summary.json má ≥5 záznamů (ověř `python -c "import json; print(json.load(open('.claude/memory/outcomes-summary.json'))['total_runs'])"`)

**Co udělat:**

1. Vytvořit `.claude/hooks/trigger-rules.yaml` — deklarativní pravidla Event-Condition-Action:
   - `failure-pattern-detected`: 2+ failures se stejným failure_class + failure_agent za 7 dní → auto `/learn-from-failure`
   - `success-rate-drop`: 7d success rate < 60% → notify uživatele
   - `stale-world-model`: outcomes-summary.json starší 3 dní → notify
   - `graduation-ready`: learning s uses≥10 AND confidence≥0.8 → suggest `/evolve`
   - `compound-success`: 5+ consecutive successes → `/scribe success-pattern`
   - `capability-gap-repeated`: 3x stejný triage no-match → zápis do capability-gaps.md

2. Vytvořit `.claude/hooks/trigger-engine.py` — PostToolUse hook (matcher: Write na outcomes/ a learnings/):
   - Load rules z trigger-rules.yaml
   - Vyhodnoť conditions (čte outcomes-summary.json, failures/, learnings/)
   - Cooldown per-rule + per-context v `trigger-state.json`
   - Akce: `inject_skill` (additionalContext), `notify` (print), `append_file`
   - Max trigger depth = 1 (trigger nesmí triggerovat trigger)
   - Max 3 triggers per session
   - Log fires do `trigger-log.jsonl`

3. Vytvořit `.claude/hooks/trigger-state.json` — počáteční stav (prázdný `{}`)

4. Registrovat hook v settings.json (PostToolUse, matcher na Write do outcomes/ a learnings/)

5. Rozšířit `/status` o trigger health: `triggers: <N fires 7d> | last: <date> | pending: <conditions close to threshold>`

6. Validovat:
   - Simuluj outcome write s failure → ověř že trigger NENASTANE (jen 1 failure, threshold je 2)
   - Simuluj 2. failure se stejným class → ověř trigger fire
   - Ověř cooldown (2. fire se stejným kontextem → skip)
   - Ověř max 3 triggers per session cap

**Klíčové rozhodnutí:** Trigger actions jsou konzervativní — nové rules začínají jako `notify` (ne auto-execute). Teprve po validaci se přepnou na `inject_skill`.

**Soubory k editaci:** settings.json, status.md (+ skills/status/SKILL.md sync)
**Soubory k vytvořit:** trigger-rules.yaml, trigger-engine.py, trigger-state.json, trigger-log.jsonl

---

## Session B: Ambient Advisor (Fáze 4a)

**Prerekvizita:** Žádná (nezávisí na Fázi 2, ale benefituje z outcomes dat)

**Co udělat:**

1. Vytvořit `.claude/hooks/advisor.py` — PostToolUse hook (throttled: every 10th tool call):
   - Počítadlo tool calls v env/temp souboru, fire jen každý 10. call
   - 5 initial patterns:

   | Pattern | Detekce | Návrh |
   |---------|---------|-------|
   | Opakovaný manuální grep (5+) | Počet Grep/Read calls bez aktivního skillu | `/scout` |
   | Multi-file edit bez plánu (3+ soubory) | Počet Edit/Write calls, žádný TodoWrite | `/orchestrate retrospective` |
   | Test fail po editu | Bash exit≠0 po Edit | `/systematic-debugging` |
   | Session bez outcomes (3+ skills) | skill_count z usage tracker, 0 outcomes | "Write outcomes" reminder |
   | Context 70%+ bez checkpointu | session-stats.json pct | `/checkpoint save` |

   - Output: `{"additionalContext": "Advisor: ..."}` (non-blocking suggestion)
   - Tracking: `advisor-log.jsonl` pro měření acceptance rate
   - Max 1 suggestion per 5 minut (cooldown)

2. Registrovat hook v settings.json (PostToolUse, všechny tools, s throttle logikou uvnitř)

3. Vytvořit `.claude/hooks/advisor-state.json` — runtime state (call counter, last suggestion time)

4. Po 1 týdnu: audit advisor-log.jsonl, spočítat acceptance rate, vyřadit annoying patterns

**Klíčové rozhodnutí:** Advisor NIKDY auto-executuje. Vždy jen navrhne. Uživatel rozhodne.

**Soubory k vytvořit:** advisor.py, advisor-state.json
**Soubory k editaci:** settings.json

---

## Session C: Capability Gap Detection (Fáze 5)

**Prerekvizita:** Fáze 2 hotová (trigger-engine existuje)

**Co udělat:**

1. Vytvořit `.claude/memory/capability-gaps.md` — registry template:
   ```markdown
   # Capability Gaps

   Automaticky generovaný backlog — situace kdy systém nemohl pomoci.

   | Date | Query/Need | Times | Status | Resolution |
   |------|-----------|-------|--------|------------|
   ```

2. Rozšířit `/triage` skill — přidat explicitní "no match" signál:
   - Pokud triage nenajde vhodný skill → na konec výstupu přidat: `[TRIAGE_NO_MATCH: "<query summary>"]`
   - Tento tag zachytí trigger-engine (viz krok 3)

3. Přidat gap detection rules do `trigger-rules.yaml`:
   ```yaml
   - id: triage-no-match
     event: skill_complete
     condition:
       type: output_pattern
       skill: triage
       pattern: "TRIAGE_NO_MATCH"
     action:
       type: append_file
       target: ".claude/memory/capability-gaps.md"
   
   - id: gap-threshold
     event: gap_recorded
     condition:
       type: count
       same_pattern: true
       threshold: 3
     action:
       type: notify
       message: "Capability gap hit 3x — consider /skill-generator"
   ```

4. Rozšířit trigger-engine.py o `append_file` action type (pokud ještě nemá)

5. Přidat gap summary do pulse-generator.py:
   - Čti capability-gaps.md, počítej open gaps
   - Přidej do pulse.json: `"capability_gaps": N`

6. Rozšířit `/status` o: `gaps: <N open> | top: <most frequent gap>`

**Soubory k editaci:** trigger-rules.yaml, trigger-engine.py, pulse-generator.py, status.md, triage.md (+ sync)
**Soubory k vytvořit:** capability-gaps.md

---

## Session D: Proactive Composition (Fáze 4b)

**Prerekvizita:** Fáze 2 hotová + Fáze 4a validovaná (advisor běží ≥1 týden)

**Co udělat:**

1. Vytvořit `.claude/hooks/composition-rules.yaml`:
   ```yaml
   compositions:
     - name: "Post-research synthesis"
       trigger:
         skill: deepresearch
         outcome: success
       sequence:
         - "/ingest {output_file}"
         - "/compile --incremental"
         - "/scribe research-complete"
       budget_cap: 0.5
       cooldown: 24h

     - name: "Failure recovery"
       trigger:
         skill: "*"
         outcome: failure
         failure_class: logic
       sequence:
         - "/reproduce {task}"
         - "/systematic-debugging"
       budget_cap: 1.0
       cooldown: 12h

     - name: "Post-build verification"
       trigger:
         skill: build-project
         outcome: success
       sequence:
         - "/critic"
         - "/verify"
         - "/checkpoint save"
       budget_cap: 0.5
       cooldown: 0
   ```

2. Rozšířit trigger-engine.py o composition execution:
   - Nový action type: `compose` — sekvenčně injektuje skills z `sequence[]`
   - Budget cap per composition (čte budget.md, nespouští pokud exceeded)
   - Cooldown per composition
   - Log do `composition-log.jsonl`

3. Rozšířit `/status` o: `compositions: <N fired 7d> | last: <name> (<date>)`

4. Rozšířit pulse-generator.py o composition stats (reads composition-log.jsonl)

**Boundary pravidlo:** Compositions NIKDY obsahují destruktivní skills (fix-issue, autofix, git push). Jen analýza, verifikace, zápis.

**Soubory k editaci:** trigger-engine.py, status.md, pulse-generator.py
**Soubory k vytvořit:** composition-rules.yaml, composition-log.jsonl

---

## Pořadí a timing

```
Teď → normální práce (outcomes se sbírají automaticky)
     ↓
Session A (Trigger Intelligence) — po ~5 sessions / ~15 outcomes
     ↓
Session B (Advisor) — kdykoliv, nezávislá
     ↓
Session C (Gap Detection) — po Session A
     ↓
Session D (Composition) — po validaci Session B (≥1 týden)
```

Sessions A a B mohou běžet paralelně (nezávisí na sobě).
Session C závisí na A (potřebuje trigger-engine).
Session D závisí na validaci B (potřebuje advisor data).

## Validace celku (po Session D)

Po dokončení všech 4 sessions spusť `/status` a ověř:
- `outcomes:` má ≥20 runs
- `signal_7d:` ukazuje mix success/partial/failure
- `triggers:` má ≥3 fires
- `pulse:` ukazuje cross-project health
- `gaps:` existuje (i kdyby 0)
- `compositions:` má ≥1 fire

Pokud všechno svítí → Intelligence Architecture je live. Flywheel běží.
