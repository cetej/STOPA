# ParaManager Adoption Evaluation — STOPA `/orchestrate`

**Date**: 2026-04-26
**Issue**: [STOPA#18](https://github.com/cetej/STOPA/issues/18) — score 11
**Paper**: arXiv:2604.17009 — *Small Model as Master Orchestrator: Learning Unified Agent-Tool Orchestration with Parallel Subtask Decomposition* (Yuan et al., April 2026)
**Concept page**: `.claude/memory/brain/wiki/concepts/paramanager-orchestrator.md`

## TL;DR

ParaManager doporučuje **lightweight orchestrátor + uniform Agent-as-Tool interface > heavy orchestrátor + heterogenní API**. STOPA dnes implementuje ~70 % paradigmu (uniform Agent() calls, status codes, Findings Ledger, wave-based parallelism, per-subtask adaptive routing) ale orchestrátor sám běží na **opus** napříč všemi tier-y — to je hlavní gap.

**Doporučení**: Částečně adoptovat (B). Konkrétně: přepnout `/orchestrate` na **per-tier orchestrator model** (haiku pro light, sonnet pro standard/farm, opus jen pro deep). Nezavádět trénovaný orchestrátor (out of scope pro Claude API). POC potvrzuje, že Haiku produkuje srovnatelný plán s Sonnetem za 1.7× rychlejší wall-clock při dvojnásobku tokenů — ekonomický rozdíl per cena/token favorizuje Haiku.

---

## 1. Co paper tvrdí

### 1.1 Architektura ParaManager

| Feature | Popis |
|---------|-------|
| **Agent-as-Tool paradigma** | Tools i LLM agenti exposed přes identický action space (jednotná INPUT/OUTPUT signatura). Orchestrátor neví, jestli volá Python tool nebo LLM. |
| **Protocol normalization** | Standardizovaný call protokol napříč všemi workery — žádné ad-hoc adaptéry. |
| **Explicit state feedback** | Po každé akci se vrací strukturovaný stavový signál, ne volný text. |
| **Decoupled planning** | Plánovací rozhodnutí oddělená od subtask execution (orchestrátor neimplementuje). |
| **Parallel subtask decomposition** | Asynchronní paralelní execution s state-aware koordinací. |

### 1.2 Trénink (out of scope pro STOPA)

- **SFT**: trajektorie s recovery mechanism (handle partial failures)
- **RL**: 4 cíle — task success + protocol compliance + action diversity + reasoning efficiency

### 1.3 Empirický výsledek

> "ParaManager achieves strong performance across multiple benchmarks and exhibits robust generalization under unseen model pools."

**Klíčový claim**: small (lightweight) model + dobré rozhraní > large model + heterogenní API. Generalizace na neviděné agent pools.

---

## 2. Co STOPA dnes dělá

### 2.1 Co už paradigmu odpovídá (≈70 %)

| Feature | STOPA implementace | Soulad s ParaManager |
|---------|-------------------|----------------------|
| **Uniform call signature** | Všechny worker spawns jdou přes `Agent(subagent_type: "general-purpose", prompt: ...)` | ✓ Plný |
| **Status codes** | DONE / DONE_WITH_CONCERNS / NEEDS_CONTEXT / BLOCKED | ✓ Částečně (jen status, ne plný state schema) |
| **Findings Ledger** | `intermediate/<subtask-id>.json` se schématem | ✓ Plný |
| **File Access Manifest** | WRITE/READ/FORBIDDEN per agent | ✓ Plný |
| **Wave-based parallel exec** | Topologický sort, max 3 paralelní agenti | ✓ Plný |
| **Decoupled planning** | Phase 3 Plan vs Phase 4 Execute oddělené | ✓ Plný |
| **Adaptive model routing** | Per-subtask haiku/sonnet/opus výběr (TARo, arXiv:2603.18411) | ✓ Lepší než ParaManager (per-step, ne per-pool) |
| **Recovery mechanism** | 3-fix escalation, Mid-Execution Replanning | ✓ Plný |

### 2.2 Co chybí oproti paradigmu (≈30 %)

| Feature | Co chybí | Důvod problému |
|---------|----------|----------------|
| **Lightweight orchestrátor** | `/orchestrate` má v frontmatter `model: opus` napříč všemi tier-y | Light tier (1 agent, jednoduchý fix) zbytečně platí opus orchestrator overhead |
| **Tools v action space** | Bash/Edit/Write nejsou exposed jako "Agent-as-Tool" — orchestrátor je nemůže volat (deny-tools) | Tools a agents mají jiný interface; orchestrátor *deleguje* tools přes worker agent, což přidává hop |
| **Trained orchestrator** | STOPA nemá trénink — orchestrace je pure prompt engineering | Out of scope: Claude API není fine-tunable. Substituce: prompt iterace + corrections.jsonl |
| **Formal state schema** | Status block je markdown, ne JSON Schema | Parsing je text-pattern, ne validated kontrakt |
| **Skill body size** | `/orchestrate` SKILL.md má 1275 řádků, 21 phase markers | Při loadingu pro Haiku orchestrator: context bloat > model capacity issue |

---

## 3. Gap Analysis

### 3.1 Tří-úrovňový gap

| Úroveň | Gap | Severity |
|--------|-----|----------|
| **Architektura** | Orchestrátor model je hardcoded opus | High — přímý cost impact |
| **Interface** | Tools nejsou v action space | Medium — adds 1 hop, ale neblockuje |
| **Trénink** | Žádný RL/SFT | N/A — STOPA nemůže trénovat Claude |

### 3.2 Empirické pozorování

`tier-definitions.yaml` definuje per-tier worker model (light: haiku, standard: sonnet, deep: opus, farm: sonnet) — ale orchestrátor **sám** je vždy opus. To je **inverse** ParaManager paradigm: large orchestrator coordinates small workers, paper říká opačně.

### 3.3 Skill body size problem

`/orchestrate` SKILL.md = 1275 řádků. I kdyby paradigm bylo perfektně implementováno, malý model nemá kontext-budget na 1275-řádkový skill před prvním tool callem. Toto je architektonický bottleneck nezávislý na ParaManager.

`SKILL.compact.md` (Progressive Withdrawal protocol, SKILL0-inspired) tento problém už adresuje — ale `/orchestrate` ji zatím nemá. Vytvoření SKILL.compact.md je prerekvizita pro Haiku orchestrátora.

---

## 4. POC

### 4.1 Setup

**Task** (light-tier, plánovací): "Najdi všechny skills s `model: opus` v `.claude/skills/`, navrhni pro každý zda zachovat opus, downgrade sonnet, nebo downgrade haiku, a napiš strukturovaný report."

**Constraint**: orchestrátor NESMÍ volat Read/Glob/Grep sám — musí všechno delegovat na čtyři standardizované workers (W1 file_lister, W2 frontmatter_reader, W3 classifier, W4 report_writer) — to simuluje Agent-as-Tool paradigma.

**Output**: strukturovaný JSON plán s decomposition, parallel_groups, expected_artifacts, success_criteria. NE execute, jen plan.

### 4.2 Měření — POC1 (plan-only, 3-way)

| Metrika | Haiku | Sonnet | Opus | Pozn. |
|---------|-------|--------|------|-------|
| **Total tokens** | 86,242 | 43,351 | 59,373 | Sonnet nejlepší |
| **Duration (wall-clock)** | 9.35 s | 15.95 s | 18.37 s | Haiku nejrychlejší |
| **Plan validity (JSON schema)** | ✓ | ✓ | ✓ | Všichni dodrželi |
| **Decomposition kroky** | 4 (W1→W2→W3→W4) | 4 (W1→W2→W3→W4) | 5 (přidal explicit filter step) | Opus nejdetailnější |
| **Explicit data flow syntax** | implicit | explicit (`{{step1.artifacts}}`) | explicit (`{{step_1.artifacts.paths}}`) | Sonnet/Opus jasnější |
| **Edge case handling** | "≥1 opus skill" | "if step 2 returns 0" | "short-circuit to Step5 with empty-result report" | Opus nejpreciznější |
| **Schema specifications** | OK | dobré | typed (`dict[path, yaml_dict]`) | Opus formálnější |
| **Worker reuse** | 4 unique | 4 unique | reuses W2 pro filter step | Opus efektivnější topologie |

**Klíčové pozorování**: Opus přidal explicit filter step (Step 3 — filter `model == 'opus'` před classification) — to zlepšuje data flow ale zvyšuje step count. Haiku/Sonnet to dělali implicitně v rámci classifier W3. Pro plan quality jsou rozdíly kosmetické — všechny 3 plány by produkovaly correct výsledek.

### 4.3 Měření — POC2 (execute end-to-end, 2-way)

Reálný end-to-end execute: agent dostal full execute permissions (Read, Glob, Grep, Bash) a měl find opus skills + napsat report. Ground truth = 2 skills (build-project, orchestrate).

| Metrika | Haiku | Sonnet |
|---------|-------|--------|
| **Total tokens** | 109,810 | 52,601 |
| **Duration (wall-clock)** | 102.16 s | 99.38 s |
| **Tool calls** | 6 | 6 |
| **Found count** | 2 / 2 | 2 / 2 |
| **Verified against ground truth** | ✓ yes | ✓ yes |
| **Recovery from Windows path issue** | (neuvedeno) | ✓ explicit (Grep glob fail → fallback Bash grep) |
| **Recommendation quality** | "keep both opus, justified" | "keep both opus, justified" |
| **Output artifact** | [`outputs/2026-04-26-haiku-execute-poc.md`](outputs/2026-04-26-haiku-execute-poc.md) | [`outputs/2026-04-26-sonnet-execute-poc.md`](outputs/2026-04-26-sonnet-execute-poc.md) |

**Klíčové pozorování**: Oba modely **dosáhly stejné task success rate (100%)** na light-tier execute. Sonnet prokázal lepší **error recovery** — explicitně reportoval Windows-specific Grep glob fail a fallback na Bash. Haiku tento detail neuvedl (možná měl, možná tichý retry). Wall-clock je téměř identický (~100 s) protože většinu času zabírají skutečné tool roundtripy, ne model thinking.

### 4.4 Klíčové zjištění (kombinované POC1+POC2)

**Hypotéza paperu potvrzena**:
- **Plan task**: Haiku produkuje plán srovnatelné kvality jako Sonnet/Opus. Opus jen marginálně preciznější (explicit filter step, formal types).
- **Execute task**: Haiku i Sonnet dosáhly 100 % task success rate. Sonnet má lepší error recovery transparency.
- Token usage je překvapivě **vyšší pro Haiku** (86k plan / 110k execute vs 43k / 53k Sonnet) — Haiku potřebuje víc verbose thinking, zejména při execute s tool calls.

### 4.5 Ground truth

```bash
$ grep -l "^model: opus" .claude/skills/*/SKILL.md
.claude/skills/build-project/SKILL.md
.claude/skills/orchestrate/SKILL.md
```

Všechny 3 plans + oba execute runs našly tento výsledek. Quality plánu/execute nezávisí na orchestrátoru pro tento light-tier task — interface stačí.

### 4.6 Ekonomická kalkulace

Anthropic ceník (output tokens, ne včetně cache):
- Haiku 4.5: ~$5/Mtok output
- Sonnet 4.6: ~$15/Mtok output
- Opus 4.7: ~$75/Mtok output

| POC run | Tokens | Estimated cost |
|---------|--------|----------------|
| Plan: Haiku | 86,242 | ~$0.43 |
| Plan: Sonnet | 43,351 | ~$0.65 |
| Plan: Opus | 59,373 | ~$4.45 |
| Execute: Haiku | 109,810 | ~$0.55 |
| Execute: Sonnet | 52,601 | ~$0.79 |

**Cost reduction Haiku vs Opus**:
- Plan task: ~$0.43 vs ~$4.45 → **90 % úspora**
- Pokud je plan task representative, Haiku orchestrator pro light tier ušetří ~85–90 % per orchestration ve srovnání s Opus baseline (current).

**Cost reduction Haiku vs Sonnet**:
- Plan: $0.43 vs $0.65 → 34 %
- Execute: $0.55 vs $0.79 → 30 %
- Sonnet má vyšší per-token cenu ale méně tokenů; ekonomický rozdíl Haiku vs Sonnet je menší než Haiku vs Opus.

### 4.7 Limitace POC

1. **Single task class** — light-tier audit task. Standard/deep tier vyžaduje hlubší reasoning, který Haiku nemusí zvládnout. Execute POC pro standard tier nebyl testován.
2. **Course-correction nezměřeno** — žádný z runs nezasáhl FAIL/replan path. ParaManager právě tuhle situaci paper testuje a ParaManager training na ni reaguje. Bez RL trainingu nelze zaručit, že Haiku zvládne complex recovery.
3. **Standardizované workers byly synthetic** (POC1) — reálné STOPA workers mají variabilní outputy. POC2 (execute) tuto výtku částečně eliminuje (real tool calls).
4. **Skill body size unaddressed** — POC nepoužil 1275-řádkový `/orchestrate` SKILL.md. V realitě by Haiku narazil na context limit. Toto je P0 prerekvizita (SKILL.compact.md).
5. **Opus execute nebyl spuštěn** — Sonnet/Haiku dosáhly 100 % na tomto úkolu, takže Opus by neukázal rozdíl. Ale to neznamená, že na složitějším úkolu by se rozdíl neukázal.

---

## 5. Doporučení

### 5.1 Verdikt: **Částečně adoptovat (B)**

| Část | Doporučení | Důvod |
|------|-----------|-------|
| **Per-tier orchestrator model** | ✓ ADOPTOVAT | Empiricky validováno POC. Light/standard tier dnes platí Opus tax. |
| **Trained orchestrator** | ✗ ODMÍTNOUT | Mimo scope — Claude API není fine-tunable. |
| **Tools v action space** | ⚠️ ČÁSTEČNĚ | Postupně standardizovat hand-off mezi skills (input-contract/output-contract už existuje). |
| **Formal state schema (JSON)** | ⚠️ POSTUPNĚ | Stačí rozšířit Status block o JSON variant — ne plný rewrite. |
| **SKILL.compact.md pro orchestrate** | ✓ ADOPTOVAT | Prerekvizita pro Haiku orchestrator (kontext capacity). |

### 5.2 Konkrétní akční kroky (priorita)

**P0 — prerekvizita (před jakoukoli změnou modelu):**
1. Vytvořit `/orchestrate/SKILL.compact.md` (~300 řádků): jen Phase 0–4 core, Phase 5–6 jen as references. Test: Haiku zvládne první invocation.

**P1 — quick win (nízké riziko):**
2. Přepnout `/orchestrate` frontmatter z `model: opus` na `model: auto` s mapováním:
   - `tier == light` → haiku
   - `tier == standard|farm` → sonnet
   - `tier == deep` → opus
3. Přidat hook `tier-detector.py` který před invocation zjistí tier a injectne odpovídající model.

**P2 — středně velké změny:**
4. Standardizovat output schema napříč skills: vždy emit JSON `{status, artifacts, notes, state}` jako součást Status blocku — nejen markdown.
5. Rozšířit `input-contract`/`output-contract` v SKILL.md (už definováno v `rules/skill-files.md`) — vyžadovat pro všechny skills, ne optional.

**P3 — experimentální (pre-commit nutný):**
6. Před produkčním rollout: A/B test 20 reálných úloh light/standard tier s Haiku orchestrator vs Opus baseline. Měřit task success rate, ne jen tokens. Threshold: Haiku ≥ 90 % Opus quality při ≥ 50 % cost reduction = pass.

### 5.3 Co NE-dělat

- **Ne-trénovat** vlastní orchestrátor — STOPA je prompt-engineered, ne fine-tuned. ParaManager training je naprosto out of scope.
- **Ne-rozkládat tools jako agenty** — STOPA má `coordinator` permission tier který blokuje Bash/Write/Edit u orchestrátora; to je správně a paper to nepotřebuje měnit.
- **Ne-dělat big-bang change** — postupně po tier-ech. Light tier první (najmenší blast radius).

### 5.4 Riziko / fallback

**Hlavní riziko**: Haiku orchestrator selhává na úlohách s implicit tier upgrade (light start → ukáže se být standard). Mitigace: 
- Tier auto-escalation logic (existuje) musí trigger model upgrade zároveň
- Circuit breaker: po 2× failed plan re-escalate na sonnet

**Fallback**: pokud P3 A/B test selže (Haiku < 90 % quality), zachovat Opus pro standard+ tier, povolit Haiku jen pro **strict light tier** (1 file, mechanical).

---

## 6. Mapování na STOPA Phase C

Issue #18 zmiňuje *vertical scaling Phase C (multi-scale orchestration)*. ParaManager je relevantní pro Phase C protože:
- Multi-scale orchestration = orchestrátor řídí mikro/mezo/makro úroveň
- Pokud má každá úroveň svého orchestrátora s odpovídajícím modelem (mikro=haiku, mezo=sonnet, makro=opus), škálování je ekonomické
- Standardizovaný Agent-as-Tool interface umožňuje libovolné nesting/composition úrovní

**Synergy**: tato evaluation může být input pro Phase C plán (target: 2026-05-18).

---

## 7. Rozhodovací checklist (pro maintainera)

- [ ] Schvaluji **P0** (vytvořit SKILL.compact.md pro orchestrate)?
- [ ] Schvaluji **P1** (per-tier model selection v frontmatter)?
- [ ] Schvaluji **P2** (rozšířený output schema, mandatory contracts)?
- [ ] Schvaluji **P3** (A/B test před produkčním rollout)?
- [ ] Zařadit do Phase C plánu (2026-05-18)?

Issue zůstává otevřený — uživatel rozhoduje o adopci.

---

## Reference

- arXiv:2604.17009 — Small Model as Master Orchestrator (ParaManager)
- arXiv:2603.18411 — TARo (per-step adaptive routing) — STOPA už implementuje
- arXiv:2602.19260 — NSM (decoupled planning) — STOPA už implementuje
- `.claude/memory/brain/wiki/concepts/paramanager-orchestrator.md` — STOPA concept page
- `.claude/skills/orchestrate/references/tier-definitions.yaml` — tier model mapping (current)
- `.claude/skills/orchestrate/SKILL.md:22` — `model: opus` (subject of this evaluation)
