# NLAH Implementační Plán — 3 aplikovatelné poznatky

**Zdroj:** arXiv:2603.25723 (Natural-Language Agent Harnesses)
**Datum:** 2026-04-05
**Scope:** STOPA orchestration system

---

## Poznatek 1: Self-Evolution jako Acceptance-Gated Disciplína

### Co paper říká
Self-evolution modul přidal **+4.8%** na SWE-bench Verified — nejsilnější jednotlivý modul.
Klíč: "disciplined acceptance-gated attempts rather than expanding search trees."
Ne víc pokusů, ale **přísnější filtr** na to, co se přijme.

### Stav v STOPA
`/self-evolve` už má robustní acceptance-gating:
- Curriculum Critic Gate (≥3/5 skóre)
- Critic Gate (každé 2 kola, FAIL → revert)
- Keep/Revert po každém editu (pass_rate pokles → revert)
- 3 consecutive reverts → STOP

**Mezera:** Self-evolution se aplikuje jen na skills. Paper naznačuje, že stejný
pattern (acceptance-gated iterace) by měl být aplikován na **libovolný artefakt**.

### Implementace

#### 1a. Generalizovaný acceptance-gate hook (nový)

**Soubor:** `.claude/hooks/acceptance-gate.py` (PostToolUse na Write/Edit)

```python
# Acceptance Gate — NLAH-inspired
# Po KAŽDÉ editaci sledovaného artefaktu (ne jen skills):
# 1. Detekuj typ artefaktu (skill, hook, config, pipeline)
# 2. Spusť odpovídající validaci
# 3. Pokud FAIL → auto-revert + log
#
# Konfigurace v settings.json:
# "acceptance_gate": {
#   "skills": "critic",        — /critic po editaci SKILL.md
#   "hooks": "syntax",         — python -c "import ast; ast.parse(...)"
#   "configs": "schema",       — JSON schema validace
#   "pipelines": "dry-run"     — harness --dry-run
# }
```

**Effort:** 4h
**Impact:** Rozšíří self-evolution disciplínu z 1 artefaktu na celý systém.

#### 1b. Self-evolution pro hooky a recepty (rozšíření)

Aktuálně `/self-evolve` funguje jen na SKILL.md. Přidat support pro:
- **Hook skripty** (`.claude/hooks/*.py`) — eval = "hook se spustí bez chyby na test inputu"
- **Recepty** (`.claude/recipes/*.yaml`) — eval = "recipe dry-run projde validací"

**Změna v:** `.claude/skills/self-evolve/SKILL.md` — přidat artifact-type detection v Phase 1.

**Effort:** 3h

---

## Poznatek 2: Path-Addressable File-Backed State

### Co paper říká
File-backed state přidal **+5.5%** na OSWorld (nejsilnější modul pro computer-use)
a **+1.6%** na SWE-bench. Tři požadavky:
1. **Externalized** — artefakty na disku, ne jen v kontextu
2. **Path-addressable** — znovuotevření přesného objektu přes cestu
3. **Compaction-stable** — přežívá truncation

### Stav v STOPA

| Požadavek | Stav | Grade |
|-----------|------|-------|
| Externalized | ✅ Plně: `.claude/memory/` na disku, 7.5 MB | A |
| Path-addressable | ⚠️ Částečně: learnings ano, state/checkpoint ne | C+ |
| Compaction-stable | ✅ Plně: `/compact` + intermediate JSON | A |

**Hlavní mezera:** `state.md` a `checkpoint.md` jsou prózou — nelze strojově adresovat
konkrétní subtask nebo stav. Při obnově session musí agent "číst a chápat" místo
"otevřít objekt na cestě."

### Implementace

#### 2a. Strukturovaný state.md s anchor IDs (refactor)

**Aktuální formát:**
```markdown
## Aktivní úkol
Popis úkolu prózou...

| # | Subtask | Status |
|---|---------|--------|
| 1 | Něco    | done   |
```

**Nový formát:**
```yaml
# state.md — structured task state
active_task:
  id: task-nlah-impl
  description: "Implementace NLAH poznatků"
  created: 2026-04-05
  branch: feat/nlah-patterns
  subtasks:
    - id: st-1
      description: "Acceptance gate hook"
      status: pending
      assignee: null
    - id: st-2
      description: "Path-addressable state"
      status: in_progress
      artifacts:
        - path: .claude/hooks/acceptance-gate.py
          type: hook
```

**Proč:** Každý subtask má `id` → lze adresovat `state.md#st-2`.
Artefakty mají `path` → zpětný odkaz na soubor.

**Effort:** 3h (refactor state.md + update /orchestrate, /checkpoint, /status skills)

#### 2b. Strukturovaný checkpoint.md (refactor)

**Aktuální formát:**
```markdown
Saved: 2026-04-04
Task: Nějaký popis prózou...
Resume Prompt: Udělej tohle a tohle...
```

**Nový formát:**
```yaml
# checkpoint.md — machine-readable session snapshot
saved: 2026-04-05T14:30:00
session_id: s-20260405-nlah
task_ref: state.md#task-nlah-impl
branch: feat/nlah-patterns
context:
  completed: [st-1, st-3]
  in_progress: [st-2]
  blocked: []
  artifacts_modified:
    - .claude/hooks/acceptance-gate.py
    - .claude/memory/state.md
resume:
  next_action: "Dokončit 2b (strukturovaný checkpoint)"
  blockers: []
  decisions_pending: []
  warnings:
    - "Verifier divergence — viz Poznatek 3"
```

**Proč:** `task_ref: state.md#task-nlah-impl` = path-addressable odkaz.
`completed: [st-1, st-3]` = strojově čitelné, ne prose.
`resume.next_action` = stále lidsky čitelné, ale strukturované.

**Effort:** 3h (refactor checkpoint.md + update /checkpoint skill)

#### 2c. Auto-checkpoint cadence (nový)

Paper předpokládá, že state je vždy aktuální. STOPA checkpointuje jen manuálně.

**Implementace:** Hook `auto-checkpoint.py` (Notification event, interval 30 min):
- Pokud se state.md změnil od posledního checkpointu → auto-save
- Pokud context > 70% kapacity → auto-save (už existuje v /checkpoint, ale ne jako hook)
- Lightweight: jen zapíše YAML, nespouští agenty

**Effort:** 2h

---

## Poznatek 3: Verifier Divergence Detection

### Co paper říká
Verifier modul způsobil **-0.8%** na SWE-bench. Příčina: "local success differs from
evaluator alignment" — verifier optimalizuje vlastní kritéria, která divergují od
toho, co benchmark (= uživatel) skutečně chce.

### Stav v STOPA
`/critic` má silné anti-divergence mechanismy:
- Milestone-driven (z diffu, ne z abstraktních pravidel)
- Assignment goals (specifické pass/fail na TUTO změnu)
- Anti-leniency (default score 2, borderline = FAIL)
- Dynamic verifier override (runtime evidence > statická analýza)

**Ale chybí:**
1. **Feedback loop** — žádný mechanismus detekuje, zda critic verdikt odpovídá
   tomu, co uživatel skutečně chtěl (no retrospective accuracy tracking)
2. **Proxy metric detection** — critic může maximalizovat "code quality score"
   místo "user task satisfaction"
3. **Verifier-user alignment check** — po critic PASS/FAIL nikdo neověřuje,
   zda uživatel souhlasí

### Implementace

#### 3a. Critic Accuracy Ledger (nový)

**Soubor:** `.claude/memory/critic-accuracy.jsonl`

**Formát:**
```jsonl
{"date":"2026-04-05","task":"nlah-impl","verdict":"PASS","score":3.8,"user_outcome":"accepted","aligned":true}
{"date":"2026-04-04","task":"sweep-fix","verdict":"FAIL","score":2.1,"user_outcome":"overridden","aligned":false,"note":"user said the fix was fine, critic was too strict on test coverage"}
```

**Zdroje dat:**
- `verdict` + `score` — z critic outputu
- `user_outcome` — detekce z následné akce:
  - Uživatel commitne po PASS → `accepted` (aligned)
  - Uživatel commitne po FAIL → `overridden` (misaligned)
  - Uživatel revertne po PASS → `rejected` (misaligned)
  - Uživatel fixne po FAIL → `accepted` (aligned)

**Hook:** `critic-accuracy-tracker.py` (PostToolUse na git commit po /critic) —
zapíše záznam do ledgeru.

**Effort:** 4h

#### 3b. Divergence Alert v /evolve (rozšíření)

`/evolve` při pravidelném maintenance review:
1. Načti `critic-accuracy.jsonl`
2. Spočítej alignment rate (posledních 20 verdiktů)
3. Pokud alignment < 80% → varování: "Critic diverguje od uživatelských preferencí"
4. Identifikuj pattern: které dimenze (safety? test coverage? code quality?) způsobují
   největší misalignment
5. Navrhni úpravu critic vah pro daný task-type

**Změna v:** `.claude/skills/evolve/SKILL.md` — přidat critic accuracy audit krok.

**Effort:** 2h

#### 3c. Lightweight user signal po critic verdiktu (UX)

Po každém `/critic` verdiktu přidat jednu otázku:

```
Critic verdict: PASS (score 3.8)
Souhlasíš s verdiktem? [y/n/skip]
```

- `y` → záznam `aligned: true`
- `n` → záznam `aligned: false` + prompt pro důvod (1 věta)
- `skip` / timeout → žádný záznam (neblokuje workflow)

**Kritické:** Musí být opt-in a neblokující. Uživatel nesnáší krok-po-kroku
schvalování (viz `feedback_approval_fatigue.md`). Proto default = skip,
signál se sbírá jen když uživatel chce.

Alternativa: **implicit signal** — sleduj jestli uživatel po critic PASS commitne
(= souhlas) nebo dál edituje (= nesouhlas). Žádná otázka, zero friction.

**Doporučení:** Implementovat OBOJÍ — implicit jako default, explicit jako `--feedback` flag.

**Effort:** 3h (implicit) + 1h (explicit flag)

---

## Implementační Prioritizace

| # | Změna | Impact | Effort | Priorita |
|---|-------|--------|--------|----------|
| 2a | Strukturovaný state.md | Vysoký — základ pro vše ostatní | 3h | **P1** |
| 2b | Strukturovaný checkpoint.md | Vysoký — session continuity | 3h | **P1** |
| 3a | Critic Accuracy Ledger | Střední — detekce divergence | 4h | **P2** |
| 1a | Acceptance gate hook | Střední — rozšíří self-evolution | 4h | **P2** |
| 3c | Implicit user signal | Střední — zero-friction feedback | 3h | **P2** |
| 2c | Auto-checkpoint cadence | Nízký — convenience | 2h | **P3** |
| 1b | Self-evolve pro hooky/recepty | Nízký — niche use case | 3h | **P3** |
| 3b | Divergence alert v /evolve | Nízký — závisí na 3a data | 2h | **P3** |

**Celkový effort:** ~24h
**Doporučený postup:** P1 (6h) → P2 (11h) → P3 (7h)

---

## Validace úspěšnosti

Jak ověříme, že implementace funguje:

1. **Path-addressable state:** Nový checkpoint musí být strojově parsovatelný —
   `python -c "import yaml; yaml.safe_load(open('state.md'))"` musí projít
2. **Acceptance gate:** 10 testovacích editací → hook správně detekuje typ a spustí validaci
3. **Critic accuracy:** Po 20 critic verdiktech → ledger má ≥15 záznamů s user_outcome
4. **Alignment rate:** Po 50 verdiktech → alignment > 85% (jinak critic váhy potřebují úpravu)
