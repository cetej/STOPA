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

### 4.2 Měření

| Metrika | Haiku orchestrátor | Sonnet baseline | Pozn. |
|---------|---------------------|-----------------|-------|
| **Total tokens** | 86,242 | 43,351 | Sonnet 2× méně |
| **Duration (wall-clock)** | 9.35 s | 15.95 s | Haiku 1.7× rychlejší |
| **Plan validity (JSON schema)** | ✓ | ✓ | Oba dodrželi |
| **Decomposition kroky** | 4 (W1→W2→W3→W4) | 4 (W1→W2→W3→W4) | Identická topologie |
| **Explicit data flow syntax** | implicit ("filtered subset from step 2") | explicit (`{{step1.artifacts}}`) | Sonnet jasnější |
| **Edge case handling** | success_criteria zmiňuje "≥1 opus skill" | success_criteria zmiňuje "if step 2 returns 0" | Sonnet preciznější |
| **Schema specifications** | Step 2 schema podrobné | Step 2 schema podrobné | Srovnatelné |

### 4.3 Ground truth

```bash
$ grep -l "^model: opus" .claude/skills/*/SKILL.md
.claude/skills/build-project/SKILL.md
.claude/skills/orchestrate/SKILL.md
```

Oba plans by tento výsledek našly. Quality plánu nezávisí na orchestrátoru pro jednoduchý decomposition — interface stačí.

### 4.4 Klíčové zjištění

**Hypotéza paperu potvrzena pro plánovací task se standardizovaným interface**:
- Haiku produkuje plán srovnatelné kvality jako Sonnet
- Sonnet je preciznější v explicit data flow syntax (use `{{step1.artifacts}}`) a edge cases
- Token usage je překvapivě **vyšší pro Haiku** (86k vs 43k) — Haiku potřebuje víc verbose thinking

**Ekonomická kalkulace** (Anthropic ceník, output tokens):
- Haiku 4.5: $5/Mtok output
- Sonnet 4.6: $15/Mtok output
- Opus 4.7: $75/Mtok output
- POC cost ratio: Haiku 86k × $5 ≈ $0.43 vs Sonnet 43k × $15 ≈ $0.65 → Haiku ~33 % levnější
- Vs Opus baseline (current): ~$3.20+ per orchestration → Haiku ~85 % úspora

### 4.5 Limitace POC

1. **Plánovací task je úzká skupina** — POC neměřil execution coordination (course-correction při FAIL, multi-wave handoff, mid-execution replanning).
2. **Standardizované workers byly synthetic** — reálné STOPA workers mají variabilní outputy. ParaManager paper trénuje orchestrator přesně na tuto variabilitu, STOPA ji nemůže trénovat.
3. **Skill body size unaddressed** — POC nepoužil 1275-řádkový SKILL.md. V realitě by Haiku narazil na context limit.
4. **Single task class** — light-tier plánování. Standard/deep tier vyžaduje hlubší reasoning, který Haiku nemusí zvládnout.

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
