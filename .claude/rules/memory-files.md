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
- Každý soubor má YAML frontmatter: date, type, severity, component, tags, summary, source, uses, harmful_uses, successful_uses, confidence
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
- **Graduation trigger**: (`uses >= 10` AND `confidence >= 0.8` AND `harmful_uses < 2`) OR (`impact_score >= 0.7` AND `uses >= 5` AND `harmful_uses < 1`) → `/evolve` navrhne promoci do `critical-patterns.md` nebo `rules/`. Learning s `confidence < 0.3` OR (`impact_score < 0.2` AND `uses >= 8`) → kandidát na pruning při maintenance.
- Learnings bez counterů nebo confidence (starší záznamy) zůstávají validní — nová pole jsou volitelné, default confidence = 0.7
- Learnings bez `supersedes:`/`related:` polí jsou plně zpětně kompatibilní
- `model_gate:` = volitelné pole — model version, pro kterou learning platí (např. `"sonnet-4.6"`, `"opus-4"`). Learnings s tímto polem jsou auto-flagovány `/evolve` a `verify-sweep.py` když aktuální model neodpovídá gate. Model-specifické workaroundy MUSÍ mít toto pole. Obecné architektonické learnings ho NESMÍ mít. Inspirováno CC `@[MODEL_LAUNCH]` tagging konvencí.
- `verify_check:` = volitelné pole — machine-checkable grep/glob assertion. Format: `"Grep('pattern', path='path') → N+ matches"` nebo `"Glob('pattern') → 1+ matches"` nebo `"manual"` pro behaviorální pravidla. Soubory s `verify_check:` jsou auditovány při SessionStart hookem `verify-sweep.py`. Každý learning by měl mít verify_check — rules without checks are wishes, rules with checks are guardrails.
- **Write-time admission control**: Hook `learning-admission.py` provádí soft gate při zápisu nového learningu: salience scoring (source_reputation × novelty) + contradiction detection proti existujícím learnings se stejným component/tags. Inspirováno A-MAC (arXiv:2603.04549). Hook neblokuje zápis — vypisuje varování. Ref: UMG/FMP research (2026-04-05).
- `critical-patterns.md` = always-read (max 10 entries, top patterns)
- Retrieval: grep-first přes component/tags, pak čti jen matched soubory. **Supersedes-aware**: pokud learning A má `supersedes: B`, přeskoč B. **Related expansion**: pokud match má `related: [X, Y]`, čti i X a Y (1-hop, max 3 extra per learning)
- **Synonym fallback** (ref: arXiv:2603.19138 — P4 knowledge-guided retrieval misses semantically similar patterns under different keywords): If initial grep returns 0 matches, generate 2-3 synonyms/related terms from the task context and retry. Example: "validation" miss → retry with "sanitization", "input checking". Max 2 retry rounds. This prevents early pruning of relevant learnings due to keyword mismatch.
- **Time-weighted relevance**: When multiple learnings match, prefer recent ones with trusted sources and high impact. Score: `severity_weight × source_weight × confidence × impact_boost × (1 / (1 + days_since_date / 60))`. Weights — severity: critical=4, high=3, medium=2, low=1. Source: user_correction=1.5, critic_finding=1.2, auto_pattern=1.0 (default), external_research=0.9, agent_generated=0.8. Impact boost: `1.0 + impact_score` (default impact_score=0.0 → boost=1.0, max impact=1.0 → boost=2.0). Confidence default=0.7 if field missing. Example: a high-impact learning (impact=0.8, boost=1.8) with medium severity gets 2×1.0×0.7×1.8=2.52, beating a zero-impact critical learning at 4×1.0×0.7×1.0=2.8 only when also fresh and from trusted source.
- Filename konvence: `<date>-<short-description>.md`
- Staleness: záznamy starší 90 dní ověřit při maintenance
- Type hodnoty: bug_fix | architecture | anti_pattern | best_practice | workflow
- Severity: critical | high | medium | low
- Component: skill | hook | memory | orchestration | pipeline | general
- `failure_class:` = volitelné pole pro failure-sourced learnings. Klasifikace selhání (HERA-inspired, arXiv:2604.00901). Hodnoty: `logic` (špatný výstup, test fail) | `syntax` (parse/compile/import error) | `timeout` (rate limit, API timeout, 503) | `resource` (ENOENT, EACCES, OOM) | `integration` (component mismatch, API contract broken) | `assumption` (předpoklad o kódu/prostředí byl špatný) | `coordination` (agent interference, špatná delegace). Pole je povinné pro learnings s type=bug_fix nebo type=anti_pattern sourced from failures.
- `failure_agent:` = volitelné pole — který agent/skill způsobil selhání (e.g., `orchestrate`, `scout`, `agent-worker`, `critic`). Používá se pro agent accountability tracking.
- `task_context:` = volitelné pole — kontext úkolu při kterém learning vznikl. Format: `{task_class: single_edit|multi_file|refactor|bug_fix|feature|research|pipeline, complexity: low|medium|high, tier: light|standard|deep|farm}`. Umožňuje HERA-style query characterization pro přesnější retrieval.

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

### Failure Retrieval

- Grep-first přes `failure_class:` a `failure_agent:` pro pattern matching
- Orchestrator konzultuje failures PŘED agent assignmentem: `grep -r "failure_class: logic" failures/ | grep "failure_agent: agent-worker"` → zjistí opakující se vzory
- Po 2+ failures se stejným failure_class + failure_agent: trigger `/learn-from-failure` pro systematickou analýzu
- Cross-reference s agent-accountability.md pro per-agent failure rates
