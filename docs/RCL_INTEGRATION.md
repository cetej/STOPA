# RCL Integration Plan — Reflective Context Learning → STOPA

**Source:** Vassilyev et al., arXiv:2604.03189, https://github.com/nvassilyev/RCL
**Date:** 2026-04-07
**Status:** Design — čeká na implementaci

---

## Executive Summary

RCL formalizuje reflect-mutate smyčku pro optimalizaci agentního kontextu (playbooks) pomocí 7 klasických ML optimalizačních primitiv. STOPA má infrastrukturu pro 5 z nich (grouped rollouts, mini-batching, auxiliary losses, batched reflection, partial failure replay). Chybí 3 klíčové věci:

1. **Dual-trace credit assignment** — contrastive success/failure signál
2. **Per-skill optimizer state** — rolling summary / momentum
3. **Systematic failure replay** — re-execution na starých selháních

Plus 4 strukturální gapy zjištěné při auditu:
4. failures/ directory je prázdný — feedback loop neexercitován
5. Trace data se maže po 7 dnech — žádný durable archive
6. Learnings `uses` countery jsou na 0-1 — retrieval loop nezavřený
7. Cross-run mutation ledger neexistuje

---

## Mapování RCL primitiv na STOPA

| RCL primitiv | RCL implementace | STOPA ekvivalent | Stav |
|---|---|---|---|
| Failure Replay | `ReplayBuffer` — sampling failed tasks, graduation after 5 passes, eviction after 3 fails | `failures/` HERA storage + `/learn-from-failure` | **Prázdný** — spec existuje, 0 záznamů |
| Grouped Rollouts | `group_size > 1` — K rolloutů per task | autoloop/autoresearch iterace per hypothesis | OK |
| Mini-batching | `mini_batch` traces per reflection | self-evolve eval batch grading | OK |
| Dual-trace Credit | Baseline + PP trace → contrastive reflector | Chybí úplně | **GAP 1** |
| Optimizer State | `OptimizationStateManager` — rolling JSON, LLM-maintained | learnings/ (bez rolling summary) | **GAP 2** |
| Auxiliary Losses | Enriched reflector: failure_type, root_cause, coverage_gaps | /critic findings, failure_class taxonomy | OK (méně formalizováno) |
| Batched Reflection | All traces in 1 LLM call | Per-iteration reflect | Minor (optimalizace) |

---

## GAP 1: Dual-Trace Credit Assignment

### Problém

STOPA ukládá failure traces (tools.jsonl, diffs) ale NE success traces. Když se něco povede, zachová se jen: (a) git diff, (b) skalární metrika v TSV. Chybí contrastive signál — "co přesně z playbooku/learningu pomohlo?" vs "co přesně selhalo?"

RCL řeší toto dvěma mechanismy:
- **Baseline + PP trace:** Každý task běží 2× — jednou normálně, jednou s PP (Perturbation Probes = XML tagy pro self-report: `<playbook_cite>`, `<uncertainty>`, `<missing_guidance>`)
- **Entry-level helpful/harmful countery** na každém PlaybookEntry

### Návrh pro STOPA

#### A. Success Trace Storage (`outcomes/`)

Nový adresář `.claude/memory/outcomes/` (ne `successes/` — budeme ukládat obojí):

```yaml
---
id: O001
date: 2026-04-07
skill: autoloop
run_id: autoloop-critic-1774987827
task: "Optimize critic skill pass rate"
outcome: success  # success | partial | failure
score_start: 0.65
score_end: 0.92
iterations: 8
kept: 6
discarded: 2
learnings_applied: ["2026-04-03-autoagent-overfitting-guard.md"]
key_mutations: ["Added regression gate at iteration 3", "Simplified output format at iteration 5"]
---

## Trajectory Summary (max 20 lines)
1. Baseline: 65% pass rate, critic skipping tests
2. Iter 1: Added explicit test-running requirement → +10%
3. Iter 3: Regression gate pattern from learning → +8%
...

## What Worked (credit signal)
- Learning `autoagent-overfitting-guard` directly applicable — prevented iteration 4 regression
- Atomic commit pattern essential for clean revert at iteration 6

## What Was Missing
- No guidance on LLM-as-judge calibration — added ad-hoc
```

**Pravidla:**
- Max 100 souborů — archivace nejstarších do `outcomes/archive/`
- Filename: `<date>-<skill>-<outcome>-<short>.md`
- Povinné pole: `outcome`, `learnings_applied`, `key_mutations`
- Skills (autoloop, autoresearch, self-evolve) zapisují outcome po fázi 3 (report)
- `learnings_applied` = které learnings byly načteny a použity (closing the retrieval loop!)

#### B. Entry-level Credit Counters na Learnings

Rozšíření stávajícího `uses`/`successful_uses`/`harmful_uses` systému:

```yaml
# V outcome záznamu:
learnings_applied:
  - file: "2026-04-03-autoagent-overfitting-guard.md"
    credit: helpful    # helpful | neutral | harmful
    evidence: "Prevented regression at iteration 4"
```

Post-run hook (`outcome-credit.py`, PostToolUse/Write na outcomes/):
1. Načte outcome soubor
2. Pro každý learning v `learnings_applied`:
   - `helpful` → `uses += 1`, `successful_uses += 1`, `confidence += 0.05`
   - `harmful` → `uses += 1`, `harmful_uses += 1`, `confidence -= 0.15`
   - `neutral` → `uses += 1`
3. Aktualizuje learning soubor

**Toto zavře retrieval-use-feedback loop**, který je v STOPA navržený ale neexercitovaný.

#### C. Perturbation Probes (PP) — volitelné, Fáze 2

RCL's PP systém (XML tagy pro self-report) je elegantní ale drahý (2× execution). Pro STOPA pragmatičtější varianta:

**Lightweight PP:** Místo 2× execution přidej reflexní krok PO každé iteraci v autoloop/autoresearch:

```
Po každém KEEP: 1-sentence attribution
"Iteration 5 succeeded because [specific learning/pattern] from [source]."

Po každém DISCARD: 1-sentence diagnosis
"Iteration 6 failed because [specific gap/wrong assumption]."
```

Toto se už částečně děje v `proposals.jsonl` (pole `trace_evidence`), ale není strukturované pro credit assignment. Rozšíření:

```jsonl
{"iteration": 5, "status": "keep", "attribution": {"learning": "overfitting-guard.md", "credit": "helpful", "evidence": "..."}}
{"iteration": 6, "status": "discard", "diagnosis": {"gap": "no calibration guidance", "failure_class": "assumption"}}
```

---

## GAP 2: Per-Skill Optimizer State (Rolling Summary / Momentum)

### Problém

RCL udržuje `OptimizationStateManager` — strukturovaný JSON dokument aktualizovaný LLM po každé iteraci. Obsahuje: playbook health assessment, change ledger, open hypotheses, interference patterns, strategy memory, optimization velocity.

STOPA má:
- `learnings/` — per-file, grep-first, ale žádný rolling summary
- `intermediate/<skill>-state.md` — post-it pattern (max 30 řádků), ale per-invocation, ne per-skill-history
- `autoresearch-strategy-<hash>.json` — per-target cross-session state, ale jen pro autoresearch

Chybí: **per-skill optimization memory** které říká "co jsme zkoušeli, co funguje, co ne, kam směřujeme."

### Návrh pro STOPA

#### A. Skill Optimization State (`memory/optstate/`)

Nový adresář `.claude/memory/optstate/` s per-skill JSON soubory:

```json
// optstate/autoloop.json
{
  "last_updated": "2026-04-07",
  "total_runs": 3,
  "health": "developing",

  "change_ledger": [
    {
      "date": "2026-04-05",
      "run_id": "autoloop-critic-1774987827",
      "mutations": ["Added regression gate", "Simplified output"],
      "effect": "+27% pass rate",
      "outcome": "success"
    }
  ],

  "strategies_that_work": [
    "Atomic commits before verification — enables clean revert",
    "Regression gate at iteration 3+ — prevents late-stage degradation"
  ],

  "strategies_that_fail": [
    "Aggressive multi-file edits in single iteration — too many variables"
  ],

  "open_hypotheses": [
    "Spot-check gate might be too aggressive for small eval sets"
  ],

  "recurring_failure_patterns": [
    "Exit code success but empty/malformed output (3 occurrences)"
  ],

  "optimization_velocity": {
    "stage": "exploration",
    "trend": "improving",
    "runs_at_stage": 3
  }
}
```

**Update protocol:**
1. Skill (autoloop/autoresearch/self-evolve) čte `optstate/<skill>.json` při Phase 0 (Setup)
2. Condensed state → kontext pro rozhodování o strategii
3. Po Phase 3 (Report): skill aktualizuje optstate soubor
4. LLM summarizace (Haiku): merge nového run do existujícího state — max 50 řádků JSON
5. `change_ledger` max 20 entries — FIFO archivace

**Rozdíl od RCL:** RCL updatuje state v background threadu s plným LLM call po každé iteraci. STOPA varianta je lehčí — update jednou per run, ne per iteration. Důvod: STOPA skills běží méně často (1-5× za den vs RCL's 50+ iterací).

#### B. Shared Optimization Context pro Mutator

Když skill dělá reflect krok, přidej optstate jako kontext:

```
## Optimization History (from optstate/autoloop.json)
- 3 prior runs, current stage: exploration
- Works: atomic commits, regression gates
- Fails: multi-file edits in single iteration
- Hypothesis: spot-check gate too aggressive for small sets
```

Toto nahrazuje RCL's `get_shared_context()` metodu.

---

## GAP 3: Systematic Failure Replay

### Problém

RCL má `ReplayBuffer` — failed tasks se vrací do budoucích batch execution, graduated po 5 consecutive passes, evicted po 3 fails. STOPA má `failures/` (prázdný) a `/learn-from-failure` (nikdy nespuštěn).

### Návrh pro STOPA

#### A. Aktivace failures/ pipeline

**Krok 1: Auto-write failure records**

Nový hook `failure-recorder.py` (PostToolUse na skill output):
- Trigger: skill output obsahuje `outcome: failure` nebo `exit_reason: crash_loop|budget_exceeded|stuck`
- Parsuje: skill name, task description, failure_class, iterations
- Zapisuje do `failures/<date>-F<NNN>-<short>.md` v HERA formátu
- Inkrementuje failure counter per (failure_class, skill)

```python
# Trigger podmínka (PostToolUse/Write na outcomes/ nebo intermediate/)
if "outcome: failure" in content or "exit_reason: crash" in content:
    write_failure_record(...)
```

**Krok 2: Automatic learn-from-failure trigger**

V `failure-recorder.py` po zápisu:
```python
same_class_count = count_failures(failure_class=fc, failure_agent=skill)
if same_class_count >= 2:
    print(f"⚠️ {same_class_count}× {fc} failure in {skill} — consider /learn-from-failure")
```

#### B. Replay Buffer pro Self-Evolve

Self-evolve dnes generuje eval cases ad-hoc. RCL-inspired upgrade:

```
Phase 0 (Setup) rozšíření:
1. Načti outcomes/ kde skill == target AND outcome == failure
2. Extrahuj failing eval patterns → replay_buffer
3. Vždy zahrň 30% replay cases + 70% fresh/escalation
4. Graduation: case projde 3× consecutive → vyřaď z replay
5. Eviction: case selže 5× po reflexi → označ jako "intractable", vyřaď
```

**Implementace v SKILL.md:**
```markdown
### Phase 0.5: Replay Buffer Construction
1. Read outcomes/ filtered by skill == <target> AND outcome != success
2. Extract task descriptions and failure patterns
3. Cross-reference with existing eval cases — avoid duplicates
4. Reserve 30% of eval budget for replay cases
5. Track per-case: consecutive_passes, consecutive_failures, reflected
6. Graduate at 3 passes, evict at 5 post-reflection failures
```

#### C. Cross-Run Mutation Ledger

`optstate/<skill>.json` (viz GAP 2) slouží zároveň jako mutation ledger — `change_ledger` array uchovává co bylo zkoušeno. Skill při reflect kroku čte tento ledger:

```
"Iterace 3 zvažuje přidání regression gate.
CHECK: change_ledger says regression gate was tried in run autoloop-critic-1774987827 with +27% effect.
DECISION: apply, evidence supports it."
```

---

## Implementační plán — 3 fáze

### Fáze 1: Outcomes + Credit Loop (nejnižší effort, nejvyšší ROI)

| # | Úkol | Effort | Soubory |
|---|------|--------|---------|
| 1.1 | Vytvořit `memory/outcomes/` directory + `.gitkeep` | trivial | filesystem |
| 1.2 | Rozšířit autoloop Phase 3 o zápis outcome záznamu | small | `skills/autoloop/SKILL.md` |
| 1.3 | Rozšířit autoresearch Phase 3 o zápis outcome záznamu | small | `skills/autoresearch/SKILL.md` |
| 1.4 | Rozšířit self-evolve Phase 2 o zápis outcome záznamu | small | `skills/self-evolve/SKILL.md` |
| 1.5 | Hook `outcome-credit.py` — aktualizuje learnings countery | medium | `hooks/outcome-credit.py` |
| 1.6 | Rozšířit proposals.jsonl o `attribution`/`diagnosis` pole | small | všechny 3 skills |
| 1.7 | Aktualizovat memory-files.md pravidla | small | `rules/memory-files.md` |

**Výstup Fáze 1:** Zavřený retrieval-use-feedback loop. Každý run zanechá strukturovaný outcome. Learnings dostávají credit/blame signál. `uses` a `impact_score` začnou reálně akumulovat.

### Fáze 2: Optimizer State + Failure Pipeline

| # | Úkol | Effort | Soubory |
|---|------|--------|---------|
| 2.1 | Vytvořit `memory/optstate/` directory + template JSON | small | filesystem |
| 2.2 | Rozšířit autoloop Setup o čtení optstate | medium | `skills/autoloop/SKILL.md` |
| 2.3 | Rozšířit autoloop Report o update optstate | medium | `skills/autoloop/SKILL.md` |
| 2.4 | Totéž pro autoresearch a self-evolve | medium | 2 skills |
| 2.5 | Hook `failure-recorder.py` — auto-write failure records | medium | `hooks/failure-recorder.py` |
| 2.6 | Aktivace learn-from-failure trigger (2+ same class) | small | v failure-recorder.py |
| 2.7 | Aktualizovat memory-files.md pravidla pro optstate + failures | small | `rules/memory-files.md` |

**Výstup Fáze 2:** Každý skill má momentum/history. Failures se automaticky zaznamenávají. Opakující se problémy triggerují systematickou analýzu.

### Fáze 3: Replay Buffer + Advanced Credit (optional, po validaci Fáze 1-2)

| # | Úkol | Effort | Soubory |
|---|------|--------|---------|
| 3.1 | Self-evolve replay buffer z outcomes/ | medium | `skills/self-evolve/SKILL.md` |
| 3.2 | Graduation/eviction logika | medium | v self-evolve SKILL.md |
| 3.3 | Lightweight PP: reflexní attribution krok per iteraci | small | všechny 3 skills |
| 3.4 | Cross-run mutation ledger query v reflect kroku | small | všechny 3 skills |
| 3.5 | Durable trace archive (7d → 30d pro outcomes: success) | small | sweep SKILL.md pravidla |

**Výstup Fáze 3:** Plný RCL-level optimization pipeline. Self-evolve systematicky retestuje starší failures. Credit assignment na úrovni jednotlivých learningu. Optimization momentum across runs.

---

## Metriky úspěchu

| Metrika | Baseline (dnes) | Po Fázi 1 | Po Fázi 3 |
|---------|----------------|-----------|-----------|
| outcomes/ záznamy | 0 | 1+ per run | 1+ per run |
| Learnings s `uses > 0` | ~2/65 | 10+/65 | 30+/65 |
| Learnings s `impact_score > 0` | 0/65 | 5+/65 | 15+/65 |
| failures/ záznamy | 0 | auto-written | auto-written |
| Graduation events | 0 | 1+ per month | 3+ per month |
| optstate/ coverage | 0 skills | 3 skills | 3+ skills |

---

## Design Decisions

### Proč NE plný RCL port?

1. **RCL je batch framework** — spouští 50+ iterací s tisíci tasks. STOPA skills běží 1-5× za den na jednom úkolu.
2. **RCL má vlastní execution environment** — AppWorld/BrowseComp sandbox. STOPA operuje v živém kódu.
3. **RCL's dual-trace je drahý** — 2× execution per task. Pro STOPA lépe lightweight PP (attribution krok).
4. **RCL's playbook je JSON** — STOPA's equivalent (SKILL.md) je markdown s YAML frontmatter. Konverze by byla destructive.

### Co přebíráme doslovně?

1. **Helpful/harmful countery** → už existují v learnings spec, jen nejsou exercitované
2. **Conservative mutation philosophy** (0-3 changes per iteration, prefer update over delete) → validuje STOPA's atomic edit pattern
3. **Optimizer state structure** — change_ledger, strategies_that_work/fail, recurring_failure_patterns
4. **Replay buffer graduation/eviction** — 5 passes graduate, 3 post-reflection fails evict
5. **Entry design principles** — EXPLICIT > IMPLICIT, PROCEDURAL > DECLARATIVE, DEFENSIVE > OPTIMISTIC

### Co adaptujeme?

1. PP traces → lightweight attribution krok (ne 2× execution)
2. Background thread state update → per-run state update (méně frequent)
3. `ReplayBuffer` class → outcome-based replay v self-evolve Phase 0
4. `OptimizationStateManager` → `optstate/*.json` soubory (file-backed, ne in-memory)

---

## Závislosti a rizika

| Riziko | Mitigace |
|--------|----------|
| Outcomes/ inflate memory | Max 100 souborů, FIFO archivace |
| optstate JSON corruption | Backup before LLM update, validate JSON schema |
| Hook chain complexity (outcome-credit + failure-recorder) | Lightweight hooks, fail-open (chyba = warning, ne block) |
| Attribution noise (skill misattributes credit) | Low stakes — countery se zprůměrují over time |
| Adoption — skills musí aktivně zapisovat outcomes | Fáze 1 mění jen 3 skill soubory |
