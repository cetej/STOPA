---
globs: ".claude/memory/**"
---

# Pravidla pro memory soubory

- Max 500 řádků per soubor — při překročení archivuj staré záznamy do `*-archive.md`
- Formát: markdown s jasnou strukturou (headings, tabulky, seznamy)
- Nikdy nemazat historii — přesouvej do archivu
- Datum ve formátu YYYY-MM-DD (absolutní, ne relativní)
- Checkpoint: vždy obsahuje resume prompt pro další session
- Budget: vždy obsahuje aktuální zůstatek a tier

## Section Markers (CPR-inspired)

- `(PROTECTED)` v nadpisu sekce = sekce se nikdy nenavrhuje k archivaci při /sweep nebo /evolve
- `(ARCHIVABLE)` v nadpisu sekce = sekce je safe k přesunu do archive při překročení limitu
- Default (bez markeru) = na dotaz při maintenance
- Markery jsou inline v headinzích: `## My Section (PROTECTED)` nebo `## Old Notes (ARCHIVABLE)`

## Skill State — Post-it Pattern (MBIF-inspired)

- Uloženy v `.claude/memory/intermediate/{skill-name}-state.md`
- Max 30 řádků — force summarization, kdo potřebuje víc, ukládá do intermediate/*.json
- Přepsáno (overwrite) při každém běhu — ne append
- YAML frontmatter: `skill`, `updated`, `phase`, `invocation`
- Skill na začátku čte svůj post-it — pokud existuje a je <1h starý, nabídne pokračování
- Post-it je privátní — ostatní skills/agents ho nečtou (na rozdíl od sdíleného state.md)
- Smaž po úspěšném dokončení tasku (ne po každé invokaci)
- Životnost: automatický cleanup při /sweep (soubory starší 24h)
- Skills které by měly používat post-it: orchestrate, deepresearch, build-project, self-evolve

## Farm Ledger (GEA-inspired group trace sharing)

Shared real-time progress ledger for farm tier agents. Mid-run writes, not final-output-only.
Ref: GEA (arXiv:2602.04837) — 71.0% vs 56.7% SWE-bench, 2× tool diversity, 1.4 vs 5 repair iterations.

- Uložen v `.claude/memory/intermediate/farm-ledger.md`
- Vytvořen orchestrátorem na začátku každého farm sweep (overwrite, ne append)
- Agenti přidávají jeden řádek po dokončení každého souboru (ne až na konci tasku)
- Formát: YAML frontmatter + markdown tabulka s: `ts | worker | file | status | pattern`
- `status` hodnoty: `fixed` | `failed` | `skipped`
- `pattern` = jednolineový popis techniky reusovatelné jinými agenty; `—` pokud žádný
- Agenti čtou ledger každých 5 souborů — aplikují discovered patterns z "Discovered Patterns" sekce
- Orchestrátor čte ledger po sweep 1, extrahuje patterns, injectuje je do sweep 2 promptů
- Archivace: po dokončení tasku rename na `farm-ledger-{task_id}.md`, /sweep cleanup po 24h
- Odlišné od CORAL `shared/notes.md`: ledger je povinný, per-file; CORAL je volitelný, per-pattern

**Formát při vytvoření:**
```markdown
---
task_id: {task_id}
sweep: 1
created: {ISO-timestamp}
task: "{description}"
total_files: {N}
---

## Per-File Progress

| ts | worker | file | status | pattern |
|----|--------|------|--------|---------|

## Discovered Patterns

(Auto-populated by orchestrator after sweep 1 completes)
```

## Truncation Boundaries (CPR-inspired)

- Checkpoint.md používá `## Session Detail Log` heading jako hard truncation boundary
- `/checkpoint resume` načte POUZE text nad touto hlavičkou (~60% token savings)
- Pokud hlavička chybí (starý checkpoint): načte celý soubor (backward compatible)
- Stejný vzor lze aplikovat na jakýkoliv memory soubor kde je potřeba oddělit summary od detailů

## Key Facts (project reference data)

- `key-facts.md` = factual constants: stack, services, endpoints, env vars, conventions
- NOT for decisions (→ decisions.md) or bug patterns (→ learnings/)
- Updated when infrastructure changes, not per-session
- Skills should check key-facts.md before guessing configs or suggesting libraries
- Format: tables grouped by category (Stack, Services, Env Vars, Dependencies, Conventions)
- Max 200 řádků — pokud roste, rozděl na sekce nebo extrahuj do per-project facts

## Learnings (per-file YAML format)

- Uloženy v `.claude/memory/learnings/` jako jednotlivé soubory
- Každý soubor má YAML frontmatter: date, type, severity, component, tags, summary, source, uses, harmful_uses, successful_uses, confidence, maturity, valid_until
- `summary:` = 1-2 věty popisující co se stalo a co dělat (generuje /scribe automaticky)
- `source:` = odkud learning pochází — ovlivňuje write-time gating i retrieval scoring. Hodnoty: `user_correction` (1.5×), `critic_finding` (1.2×), `auto_pattern` (1.0×, default), `agent_generated` (0.8×), `external_research` (0.9×). Soubory bez `source:` se chovají jako `auto_pattern`.
- `uses:` = kolikrát byl learning retrieven a aplikován (počáteční hodnota 0, inkrementuje se při použití)
- `successful_uses:` = kolikrát vedl learning k úspěšnému výsledku (počáteční hodnota 0, inkrementuje se při PASS po aplikaci). `utility = successful_uses / uses` (HERA-inspired empirical success rate). Learnings bez tohoto pole: backward compatible, default 0.
- `harmful_uses:` = kolikrát vedl learning ke špatnému výsledku (počáteční hodnota 0, inkrementuje /critic)
- `supersedes:` = filename staršího learningu, který tento nahrazuje (volitelné, max 1). Superseded soubory se při retrieval přeskakují, ale zůstávají na disku
- `related:` = array filenames souvisejících learnings pro multi-hop retrieval (volitelné, max 3). Pouze 1-hop — žádné řetězení
- `confidence:` = numerické skóre 0.0-1.0 vyjadřující důvěryhodnost learningu. Počáteční hodnota závisí na source: user_correction=0.9, critic_finding=0.8, auto_pattern=0.7, external_research=0.6, agent_generated=0.5. Decay: learnings nepoužité (`uses == 0`) 60+ dní ztrácí 0.1 confidence za každých 30 dní nečinnosti (min 0.1). **Learnings s uses > 0 se nedecayují** — aktivně používané znalosti zůstávají stabilní. Boost: každé `uses` inkrementuje confidence o 0.05 (max 1.0). Každé `harmful_uses` snižuje o 0.15. (Budoucí vylepšení: ACT-R exponenciální decay modulovaný frekvencí přístupu, viz arXiv HAI 2025.)
- `impact_score:` = volitelné pole 0.0-1.0 měřící skutečný dopad learningu na výsledek. Počáteční hodnota 0.0 (neměřeno). Aktualizuje se helpfulness-driven způsobem (SKILL0-inspired):
  - Po aplikaci learningu `/critic` porovná kvalitu výstupu s/bez learningu
  - Pokud critic score se zlepšil ≥ 0.5 bodu: `impact_score += 0.1` (max 1.0)
  - Pokud critic score se nezměnil: `impact_score` beze změny
  - Pokud critic score se zhoršil: `impact_score -= 0.15` (min 0.0)
  - Impact se měří na on-policy výsledcích (aktuální úkol), ne historicky
  - Learnings s `impact_score >= 0.7` a `uses >= 5` = **high-impact** — prioritizovány při retrieval
  - Learnings s `impact_score < 0.2` a `uses >= 8` = **low-impact** — kandidáti na pruning i při vysokém uses
- **Graduation trigger**: (`maturity == core` OR (`uses >= 10` AND `confidence >= 0.8` AND `harmful_uses < 2`)) OR (`impact_score >= 0.7` AND `uses >= 5` AND `harmful_uses < 1`) → `/evolve` navrhne promoci. Maturity tier `core` je prerequisite — learnings s `maturity: draft` se negraduují i když splňují counter thresholds (musí projít validated → core flow). **Graduation routing** (Acemoglu Theorem 3 — lokální > globální): learnings s `skill_scope:` → graduate do `.claude/skills/<name>/learned-rules.md` (skill-lokální pravidla). Learnings BEZ `skill_scope:` → graduate do `critical-patterns.md` (globální). Cross-cutting learnings (platné pro 3+ skills): zůstávají globální i s `skill_scope:` pokud scope obsahuje ≥3 skills. Learning s `confidence < 0.3` OR (`impact_score < 0.2` AND `uses >= 8`) → kandidát na pruning při maintenance.
- `maturity:` = volitelné pole — lifecycle stav learningu. Hodnoty: `draft` (nově zapsaný, nevalidovaný) | `validated` (opakovaně úspěšně aplikovaný) | `core` (kandidát na graduation). Default = `draft`. Přechody:
  - `draft → validated`: `uses >= 5 AND harmful_uses == 0` (learning prokázal užitečnost)
  - `validated → core`: `uses >= 10 AND confidence >= 0.8 AND harmful_uses < 2` (splňuje graduation trigger)
  - `validated → draft` (demotion): `harmful_uses >= 3` (hysteresis — vyžaduje víc evidence pro demotion než pro promotion)
  - `core → validated`: `harmful_uses >= 2` (core pattern se ukázal jako problematický)
  - Retrieval boost: `core` = 1.3×, `validated` = 1.1×, `draft` = 1.0× (draft nemá penalty, jen nemá boost)
  - `/evolve` automaticky aktualizuje maturity based na countery. `/scribe` zapisuje nové learnings jako `draft`.
  - Failure-sourced learnings (type=bug_fix z failure) se zapisují jako `maturity: draft` a přidávají do `memory/replay-queue.md` pro validační replay (HERA-inspired, arXiv:2604.00901).
  - Backward compatible — learnings bez pole se chovají jako `draft`.
  - Ref: ByteRover maturity tiers (arXiv:2604.01599) — -29.4pp ablation on tiered retrieval.
- `valid_until:` = volitelné pole — ISO date (YYYY-MM-DD), po kterém je learning považován za expired. Learnings s `valid_until < today` se přeskakují při retrieval (ve všech retrieval cestách: grep, BM25, hybrid). Zůstávají na disku pro audit trail. Automaticky nastaveno: při zápisu `supersedes: old-file.md` se na old learning nastaví `valid_until: <today>`. Manuálně nastavitelné pro time-limited workaroundy. Backward compatible — learnings bez pole = neomezená platnost (nikdy neexpirují).
  - Ref: Zep bi-temporal model (arXiv:2501.13956) — confidence decay ≠ factual invalidation. Explicit invalidity > probabilistic decay.
- Learnings bez counterů nebo confidence (starší záznamy) zůstávají validní — nová pole jsou volitelné, default confidence = 0.7, default maturity = draft
- Learnings bez `supersedes:`/`related:`/`maturity:`/`valid_until:` polí jsou plně zpětně kompatibilní
- `model_gate:` = volitelné pole — model version, pro kterou learning platí (např. `"sonnet-4.6"`, `"opus-4"`). Learnings s tímto polem jsou auto-flagovány `/evolve` a `verify-sweep.py` když aktuální model neodpovídá gate. Model-specifické workaroundy MUSÍ mít toto pole. Obecné architektonické learnings ho NESMÍ mít. Inspirováno CC `@[MODEL_LAUNCH]` tagging konvencí.
- `verify_check:` = volitelné pole — machine-checkable grep/glob assertion. Format: `"Grep('pattern', path='path') → N+ matches"` nebo `"Glob('pattern') → 1+ matches"` nebo `"manual"` pro behaviorální pravidla. Soubory s `verify_check:` jsou auditovány při SessionStart hookem `verify-sweep.py`. Každý learning by měl mít verify_check — rules without checks are wishes, rules with checks are guardrails.
- `skill_scope:` = volitelné pole — array skill jmen, pro která learning platí (e.g., `[orchestrate, critic]`). Learnings BEZ `skill_scope:` jsou globální — kandidáti na graduation do `critical-patterns.md`. Learnings S `skill_scope:` graduují do `.claude/skills/<name>/learned-rules.md` (lokální pravidla). Lokální graduation je preferována pro skill-specifické poznatky (Acemoglu arXiv:2604.04906 Theorem 3: globální agregátor nutně zhorší ≥1 dimenzi). Cross-cutting poznatky (platné napříč skills) zůstávají bez scope. Backward compatible — starší learnings bez pole se chovají jako globální.
- **Write-time admission control**: Hook `learning-admission.py` provádí gate při zápisu nového learningu: salience scoring (source_reputation × novelty) + contradiction detection + circular validation detection (arXiv:2604.04906) proti existujícím learnings a critical-patterns. Inspirováno A-MAC (arXiv:2603.04549). Mode: `STOPA_ADMISSION_GATE=soft` (default, warning only) | `hard` (blocks write on contradiction OR novelty < 0.2, exit code 1). Ref: A-MAC 31% latency reduction from cleaner memory store.
- `critical-patterns.md` = always-read (max 10 entries, top patterns)
- Retrieval: grep-first přes component/tags, pak čti jen matched soubory. **Supersedes-aware**: pokud learning A má `supersedes: B`, přeskoč B. **Related expansion**: pokud match má `related: [X, Y]`, čti i X a Y (1-hop, max 3 extra per learning)
- **Synonym fallback** (ref: arXiv:2603.19138 — P4 knowledge-guided retrieval misses semantically similar patterns under different keywords): If initial grep returns 0 matches, generate 2-3 synonyms/related terms from the task context and retry. Example: "validation" miss → retry with "sanitization", "input checking". Max 2 retry rounds. This prevents early pruning of relevant learnings due to keyword mismatch.
- **Hybrid retrieval with RRF** (ref: LLM Wiki v2 — Gap 2): When initial grep returns <3 matches OR task tier is `deep`, run full hybrid: `python scripts/hybrid-retrieve.py "<query>" --task-tier <tier> --top 8 --json`. Combines grep + BM25 (`memory-search.py`) + graph walk (`concept-graph.json` 1-hop) via Reciprocal Rank Fusion (k=60). Falls back gracefully if `concept-graph.json` missing or >7 days old. Trigger: grep 0 → synonym fallback first, then hybrid; grep 1-2 → hybrid; tier=deep → always.
- **Graph walk** (ref: LLM Wiki v2 — Gap 1): Expands matched learnings via 1-hop neighbors in `concept-graph.json`. Implemented in `hybrid-retrieve.py` via `graph_walk_from_files()` from `associative_engine.py`. Separate from 2-hop spreading activation (`associative-recall.py`, UserPromptSubmit ambient recall).
- **Time-weighted relevance**: When multiple learnings match, prefer recent ones with trusted sources and high impact. Score: `severity_weight × source_weight × confidence × impact_boost × maturity_boost × (1 / (1 + days_since_date / 60))`. Maturity boost: core=1.3, validated=1.1, draft=1.0 (default). Weights — severity: critical=4, high=3, medium=2, low=1. Source: user_correction=1.5, critic_finding=1.2, auto_pattern=1.0 (default), external_research=0.9, agent_generated=0.8. Impact boost: `1.0 + impact_score` (default impact_score=0.0 → boost=1.0, max impact=1.0 → boost=2.0). Confidence default=0.7 if field missing. Example: a high-impact learning (impact=0.8, boost=1.8) with medium severity gets 2×1.0×0.7×1.8=2.52, beating a zero-impact critical learning at 4×1.0×0.7×1.0=2.8 only when also fresh and from trusted source.
- Filename konvence: `<date>-<short-description>.md`
- Staleness: záznamy starší 90 dní ověřit při maintenance
- Type hodnoty: bug_fix | architecture | anti_pattern | best_practice | workflow
- Severity: critical | high | medium | low
- Component: skill | hook | memory | orchestration | pipeline | general
- `failure_class:` = volitelné pole pro failure-sourced learnings. Klasifikace selhání (HERA-inspired, arXiv:2604.00901). Hodnoty: `logic` (špatný výstup, test fail) | `syntax` (parse/compile/import error) | `timeout` (rate limit, API timeout, 503) | `resource` (ENOENT, EACCES, OOM) | `integration` (component mismatch, API contract broken) | `assumption` (předpoklad o kódu/prostředí byl špatný) | `coordination` (agent interference, špatná delegace). Pole je povinné pro learnings s type=bug_fix nebo type=anti_pattern sourced from failures.
- `failure_agent:` = volitelné pole — který agent/skill způsobil selhání (e.g., `orchestrate`, `scout`, `agent-worker`, `critic`). Používá se pro agent accountability tracking.
- `task_context:` = volitelné pole — kontext úkolu při kterém learning vznikl. Format: `{task_class: single_edit|multi_file|refactor|bug_fix|feature|research|pipeline, complexity: low|medium|high, tier: light|standard|deep|farm}`. Umožňuje HERA-style query characterization pro přesnější retrieval.

## Outcomes (per-run RCL credit records)

RCL-inspired outcome storage (arXiv:2604.03189). Captures both success and failure trajectories for dual-trace credit assignment.

- Stored in `.claude/memory/outcomes/` as individual files
- Filename: `<date>-<skill>-<outcome>-<short>.md` (e.g., `2026-04-07-autoloop-success-critic-optimization.md`)
- Max 100 files — archive oldest to `outcomes/archive/` on overflow
- YAML frontmatter: `skill`, `run_id`, `date`, `task`, `outcome` (success|partial|failure), `score_start`, `score_end`, `iterations`, `kept`, `discarded`, `exit_reason`, `baseline_run`
- `baseline_run:` = volitelné pole — filename předchozího outcome se stejným `skill` + podobným `task` pro contrastive credit assignment (RCL dual-trace, arXiv:2604.03189). Při zápisu outcome hledej nejnovější run se stejným skill. Reflector (`/evolve`) čte oba runs pro attribution — contrastive pár (success + failure na stejný task type) je atomická jednotka credit assignment.
- Body sections: `## Trajectory Summary` (max 15 key iterations), `## Learnings Applied` (file + credit + evidence), `## What Worked`, `## What Failed`, `## Error Localization` (optional)
- **Error Localization format** (SD-ZERO inspired, for failure/partial outcomes): table with columns `| Iteration | Error Location | What Was Wrong | Self-Check Caught? |`. Tracks WHERE errors occurred (file:line) and whether the self-revision step (Step 2.5/3.5) caught them before verify. Enables measuring self-check hit rate across runs.
- **Learnings Applied format**: `- file: <filename.md> | credit: helpful|harmful|neutral | evidence: <1-sentence>`
- Hook `outcome-credit.py` auto-updates learning counters on write
- Hook `failure-recorder.py` auto-creates failure record when outcome = failure|partial
- Skills that write outcomes: autoloop, autoresearch, self-evolve (at their Report/Handoff phase)

## Optimization State (per-skill momentum)

RCL-inspired optimizer state (arXiv:2604.03189). Rolling JSON capturing cross-run learning for each iterative skill.

- Stored in `.claude/memory/optstate/` as JSON files
- Filename: `<skill>.json` (e.g., `autoloop.json`, `autoresearch.json`, `self-evolve.json`)
- Schema: `last_updated`, `total_runs`, `health`, `change_ledger[]` (max 20 FIFO), `strategies_that_work[]`, `strategies_that_fail[]`, `recurring_failure_patterns[]`, `optimization_velocity{stage, trend}`
- Read at skill Phase 0 (Setup) — strategies inform initial approach
- Updated at skill Phase 3 (Report) — merge new run data into existing state
- Haiku summarization for merge if state exceeds 50 lines
- If file doesn't exist: skill proceeds normally (no prior state)

## Failures (per-failure YAML records)

HERA-inspired failure trajectory storage (arXiv:2604.00901). Každý zaznamenaný failure uchovává kompletní rozhodovací řetězec.

- Uloženy v `.claude/memory/failures/` jako jednotlivé soubory
- Filename: `<date>-F<NNN>-<short-description>.md` (e.g., `2026-04-06-F001-auth-session-invalidation.md`)
- Max 50 souborů — při překročení archivuj nejstarší do `failures/archive/`
- Failures starší 60 dní: auto-archivace při `/sweep`

### Failure File Format

```yaml
---
id: F001
date: YYYY-MM-DD
task: "Short task description"
task_class: single_edit | multi_file | refactor | bug_fix | feature | research | pipeline
complexity: low | medium | high
tier: light | standard | deep | farm
failure_class: logic | syntax | timeout | resource | integration | assumption | coordination
failure_agent: orchestrate | scout | critic | agent-worker | <skill-name>
resolved: true | false
resolution_learning: ""  # filename of learning that captured the fix (optional)
---

## Trajectory

1. `orchestrate` → assigned tier:standard, 3 agents
2. `scout` → found auth.py, middleware.py, tests/
3. `agent-2` → edited middleware.py line 45
4. `critic` → FAIL: session token not invalidated on logout

## Root Cause

Agent assumed stateless auth, but app uses server-side sessions.

## Reflexion

Příště přečíst existující testy PŘED editací — testy by odhalily session-based pattern.
```

**TAR trajectory format** (preferred for new failure records, ref: arXiv:2604.01437 Li & Storhaug, ICSE/FSE/ASE review): explicitní 3-section struktura `## Thought` (what agent believed going in) → `## Action` (what it did) → `## Result` (what happened/error). Kompatibilní s existujícím `## Trajectory` — `## Trajectory` zůstává pro chronological rollup, TAR sekce přidávají semantic layering pro cross-run causal analysis. /scribe emituje TAR sections pro nové failure records.

### Failure Retrieval

- Grep-first přes `failure_class:` a `failure_agent:` pro pattern matching
- Orchestrator konzultuje failures PŘED agent assignmentem: `grep -r "failure_class: logic" failures/ | grep "failure_agent: agent-worker"` → zjistí opakující se vzory
- Po 2+ failures se stejným failure_class + failure_agent: trigger `/learn-from-failure` pro systematickou analýzu
- Cross-reference s agent-accountability.md pro per-agent failure rates

## Replay Queue (HERA-inspired replay validation)

Failure-sourced learnings zapsané jako `maturity: draft` se přidávají do replay queue pro validační replay. Ref: HERA (arXiv:2604.00901) — +38.69% SOTA s replay-validated generalization.

- Uloženo v `.claude/memory/replay-queue.md` jako markdown tabulka
- Max 20 entries — při překročení archivuj nejstarší (resolved) do `replay-queue-archive.md`
- Format: `| learning file | failure_class | date added | replay status | replay count |`
- Replay status: `pending` (čeká na 2+ matching failures) | `ready` (2+ failures, připraven na replay) | `replayed` (replay proběhl) | `resolved` (learning validován/upgraded)
- Lifecycle:
  1. `/scribe` zapíše failure learning jako `draft` → přidá do replay queue jako `pending`
  2. Při dalším failure se stejnou `failure_class` → status se změní na `ready`
  3. `/evolve` nebo `/learn-from-failure` provede HERA-style replay (3 varianty: efficiency, thoroughness, risk)
  4. Úspěšný replay → learning upgradován na `maturity: validated`, queue status = `resolved`
  5. Neúspěšný replay → learning zůstává `draft`, queue status = `resolved` (learning je non-generalizable)
- `/dreams` kontroluje replay queue: items starší 14 dní bez replay → flag pro attention
- `/evolve` Step 3e: Replay Queue audit — check pending/ready items, navrhni replay
