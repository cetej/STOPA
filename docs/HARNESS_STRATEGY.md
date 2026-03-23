# Harness Strategy — Integrace do STOPA a projektů

> **STATUS: SPLNĚNO** (2026-03-22). Fáze A (rules, skill audit, critic) i Fáze B (engine, /harness skill, skill-audit harness) implementovány. Tento dokument slouží jako historická reference.

Jak využít principy harness engineering (deterministické řízení AI agentů) pro upgrade orchestračního systému STOPA a cílových projektů.

---

## 1. Co máme vs co chybí

### STOPA dnes (skills-based orchestrace)

```
User → /orchestrate → [Scout] → [Plan] → [Execute: Agent/Skill] → [Critic] → [Scribe]
                                              ↑ dynamický plán
                                              ↑ LLM rozhoduje co a jak
                                              ↑ validace = critic (LLM review)
```

**Silné stránky:**
- Budget tiers (light/standard/deep) — cost control
- Circuit breakers — hard stops proti loops
- Shared memory — state, decisions, learnings přežívají sessions
- Checkpoints — session continuity
- Sub-agenti s izolovaným kontextem

**Slabiny (gap analýza):**

| Gap | Dopad | Severity |
|-----|-------|----------|
| Žádné deterministické fáze | LLM může přeskočit/změnit pořadí kroků | High |
| Validace = LLM review (critic) | Subjektivní, ne programatická | High |
| Žádné path-specific rules | CLAUDE.md loaded celý vždy | Medium |
| Žádné šablonové výstupy | Formát reportů závisí na náladě LLM | Medium |
| Chybí forced tool_choice | Agent může zvolit špatný tool | Medium |
| Žádné mezivýsledky na disk | Při pádu session = ztráta práce | Medium |
| Jeden model pro vše v rámci skillu | Plýtvání tokeny na jednoduché subtasky | Low |

### Harness přístup (cílový stav)

```
User → /harness:contract-review → Phase 1 [Extract] → validate ✓
                                 → Phase 2 [Classify] → validate ✓
                                 → Phase 3 [Human input] → collect
                                 → Phase 4 [Research: N sub-agents ∥] → validate ✓
                                 → Phase 5 [Analysis: N sub-agents ∥] → validate ✓
                                 → Phase 6 [Generate: template] → validate ✓
                                 → Output: deterministic Word/MD document
```

**Klíčové rozdíly:**
- Fáze jsou **fixní a sekvenční** — LLM je nemůže přeskočit
- Každá fáze má **programatickou validaci** (ne LLM review)
- Mezivýsledky se **ukládají na disk** (resilience)
- Výstup je **šablonový** (template, ne LLM-generated formát)
- Sub-agenti běží **paralelně** s **levnějším modelem**

---

## 2. Strategie: Hybrid — Skills + Harness

Nenahrazujeme skills harnessy. Přidáváme harness jako **vyšší úroveň** pro opakované, kritické procesy.

```
Rozhodovací strom:
├── Ad-hoc úkol (jednorázový, neznámý scope)
│   └── → /orchestrate (skills-based, dynamický plán)
│
├── Opakovaný proces (známé kroky, potřeba spolehlivosti)
│   └── → /harness:<název> (deterministické fáze)
│
└── Hybridní (známá struktura, ale variabilní kroky uvnitř)
    └── → /harness s dynamickými sub-fázemi uvnitř fixního rámce
```

### Architektura harness v STOPA

```
.claude/
├── skills/
│   ├── orchestrate/           # Stávající — pro ad-hoc úkoly
│   └── harness/               # NOVÝ meta-skill
│       └── SKILL.md           # Dispatcher: vybere správný harness
│
├── harnesses/                  # NOVÝ adresář
│   ├── _engine.md             # Sdílená logika (fáze, validace, reporting)
│   ├── pipeline-audit/        # Harness: audit pipeline projektu
│   │   ├── HARNESS.md         # Definice fází + validačních kritérií
│   │   └── template.md        # Šablona výstupního reportu
│   ├── article-review/        # Harness: review článku
│   │   ├── HARNESS.md
│   │   └── template.md
│   └── codebase-migration/    # Harness: migrace kódu
│       ├── HARNESS.md
│       └── template.md
│
└── rules/                      # NOVÝ — path-specific pravidla
    ├── python-files.md         # Pravidla pro *.py
    ├── skill-files.md          # Pravidla pro skills/
    └── memory-files.md         # Pravidla pro memory/
```

### HARNESS.md formát

```yaml
---
name: pipeline-audit
description: Audit end-to-end pipeline for reliability, performance, and correctness
phases: 6
estimated_tokens: 150K-300K
output_template: template.md
---

# Pipeline Audit Harness

## Phase 1: Inventory (deterministic)
- **Action**: Glob + Grep pro všechny entry pointy pipeline
- **Validation**: ≥1 entry point nalezen
- **Output file**: `.harness/phase1_inventory.json`
- **Model**: haiku (levný, stačí na file listing)

## Phase 2: Dependency Map (deterministic)
- **Action**: Pro každý modul: import analysis + call graph
- **Validation**: JSON schema validace, no circular deps
- **Output file**: `.harness/phase2_deps.json`
- **Model**: haiku

## Phase 3: Risk Assessment (LLM, parallel sub-agents)
- **Action**: Pro každý modul: spawn sub-agent s kontextem z Phase 1+2
- **Validation**: Každý sub-agent vrátí structured JSON {risk_level, issues[], recommendations[]}
- **Output file**: `.harness/phase3_risks.json`
- **Model**: sonnet pro sub-agenty (narrow task = levnější model stačí)
- **Parallelism**: max 3 současně (budget control)

## Phase 4: Integration Test (deterministic)
- **Action**: Spustit pipeline na testovacích datech
- **Validation**: Exit code 0, output matches expected schema
- **Output file**: `.harness/phase4_test_results.json`
- **Model**: N/A (pure code execution)

## Phase 5: Report Generation (template-based)
- **Action**: Naplnit template.md daty z Phase 1-4
- **Validation**: Všechny placeholder vyplněny, no {{MISSING}}
- **Output file**: `audit_report.md`
- **Model**: haiku (fill template, cheap)

## Phase 6: Executive Summary (LLM)
- **Action**: Shrnout findings do 5 bullet pointů
- **Validation**: ≤5 bullets, ≤200 slov
- **Output file**: prepend to audit_report.md
- **Model**: sonnet (needs reasoning for synthesis)
```

---

## 3. Konkrétní harnessy pro projekty

### 3.1 ZÁCHVĚV — Pipeline Harness

Záchvěv má 8-krokový pipeline (ingest → sentiment → embeddings → UMAP → HDBSCAN → EWS → CRI → interpretace). Kandidát na deterministický harness.

```
Harness: zachvev-pipeline
Fáze:
1. Ingest       → validate: ≥100 postů, has [title, body, created_utc, score]
2. Sentiment    → validate: sentiment_score ∈ [1,5], no NaN
3. Embeddings   → validate: shape = (N, 256), no NaN rows
4. Topics       → validate: ≥2 clusters, noise < 80%
5. EWS          → validate: JSON schema, all metrics finite
6. CRI          → validate: CRI ∈ [0,1], components sum correct
7. Interpret    → validate: české texty, ≤500 slov per topic
8. Report       → template: dashboard data structure
```

**Přínos:** Dnes pipeline selže tiše (NaN propagace, prázdné clustery). S harness = fail-fast na konkrétní fázi + jasná diagnostika.

### 3.2 NG-ROBOT — Content Pipeline Harness

```
Harness: content-pipeline
Fáze:
1. Source       → fetch článek/zdroj
2. Extract      → validate: title, body ≥100 chars, metadata
3. Enrich       → terminologie, entity extraction
4. Correct      → CzechCorrector (morfologie + pravopis)
5. Format       → validate: markdown structure, no broken links
6. Publish      → template: output format per channel
```

### 3.3 STOPA — Skill Audit Harness

```
Harness: skill-audit
Fáze:
1. Inventory    → list all skills, extract metadata
2. Description  → audit: je description dostatečně specifická? Říká kdy NE-použít?
3. Tools        → audit: least privilege? Zbytečné tools?
4. Integration  → audit: používá shared memory? Zapisuje learnings?
5. Report       → template: tabulka skills × audit dimensions
```

### 3.4 Univerzální — Code Review Harness

```
Harness: code-review
Fáze:
1. Diff extract    → git diff, classify changed files
2. Static check    → lint, type check, import validation
3. Security scan   → OWASP patterns, secrets detection
4. Logic review    → LLM sub-agents per changed file (parallel)
5. Integration     → dependency impact analysis
6. Report          → template: findings table + recommendations
```

---

## 4. Implementační plán

### Fáze A: Foundations (effort: nízký)

| # | Úkol | Soubory | Přínos |
|---|------|---------|--------|
| A1 | Vytvořit `.claude/rules/` s path-specific pravidly | 3 nové .md soubory | Méně tokenů v kontextu, přesnější chování |
| A2 | Audit skill descriptions — přidat "kdy NEpoužít" | 13 SKILL.md souborů | Lepší tool routing, méně mis-invocations |
| A3 | Přidat do `/critic`: instrukce pro separate session | critic/SKILL.md | Nezaujatý review |
| A4 | Přidat do learnings.md zápis z video analýzy | learnings.md | ✅ DONE |

### Fáze B: Harness Engine (effort: střední)

| # | Úkol | Soubory | Přínos |
|---|------|---------|--------|
| B1 | Vytvořit `.claude/harnesses/` adresář + `_engine.md` | Nový adresář + soubor | Sdílená logika pro všechny harnessy |
| B2 | Implementovat `/harness` meta-skill (dispatcher) | harness/SKILL.md | Entry point pro deterministické procesy |
| B3 | Vytvořit `zachvev-pipeline` harness | HARNESS.md + template | První produkční harness |
| B4 | `.harness/` working directory pro mezivýsledky | Konvence | Resilience — restart od libovolné fáze |

### Fáze C: Advanced (effort: vyšší)

| # | Úkol | Soubory | Přínos |
|---|------|---------|--------|
| C1 | Model routing v harness fázích (haiku/sonnet/opus per phase) | _engine.md | Token efficiency |
| C2 | Programatická validace (JSON schema, assertions) místo LLM critic | Validátory per harness | Deterministic quality gates |
| C3 | Template-based output generování | template.md per harness | Konzistentní formát výstupů |
| C4 | Parallel sub-agent batching s budget control | _engine.md | Scale + cost control |

### Fáze D: Distribution (effort: nízký po B)

| # | Úkol | Přínos |
|---|------|--------|
| D1 | Přidat harnesses do stopa-orchestration pluginu | Distribuce do cílových projektů |
| D2 | Projekt-specifické harnessy v cílových repech | Customizace per projekt |
| D3 | Harness pro onboarding nového projektu | Standardizovaný project-init |

---

## 5. Rozdíl: Skill vs Harness — rozhodovací tabulka

| Kritérium | Skill | Harness |
|-----------|-------|---------|
| Kroky jsou vždy stejné? | Ne (LLM rozhoduje) | Ano (fixní fáze) |
| Potřeba 100% spolehlivosti? | Ne (best effort OK) | Ano (produkční proces) |
| Opakuje se pravidelně? | Ne (ad-hoc) | Ano (denně/týdně) |
| Výstup musí mít fixní formát? | Ne | Ano (šablona) |
| Mezivýsledky důležité? | Ne | Ano (restart od fáze) |
| Validace programatická? | Ne (LLM critic) | Ano (assertions, schema) |
| Paralelní sub-agenti? | Možné ale ad-hoc | Strukturované (batch, budget) |

**Příklad rozhodnutí:**
- "Zrecenzuj tento PR" → **Skill** (scope se liší PR od PR)
- "Spusť Záchvěv pipeline na nových datech" → **Harness** (8 fixních kroků, validace po každém)
- "Optimalizuj výkon API" → **Skill** (neznámý scope, explorace)
- "Proveď weekly skill audit" → **Harness** (známé kroky, opakuje se)

---

## 6. Quick Wins — co implementovat hned

1. **`.claude/rules/`** — 3 soubory, okamžitý efekt na token efficiency
2. **Skill description audit** — "kdy NE-použít" do všech 13 skills
3. **Záchvěv pipeline validátory** — `np.isfinite()`, schema checks po každém kroku (už částečně v Session 8 úkolech)
4. **`.harness/` konvence pro mezivýsledky** — mkdir + save JSON po každé fázi pipeline

Tyto 4 věci nevyžadují nový skill ani engine — jdou udělat v rámci stávající architektury a přinášejí okamžitý benefit.

---

## Reference

- Video: "Harness Engineering" (YouTube I2K81s0OQto) — contract review demo, 12 principů
- Video: "Claude Certified Architect" (YouTube vizgFWixquE) — 5 domén, prompts vs hooks, tool descriptions
- Anthropic Legal Plugin — inspirace pro HARNESS.md formát
- Stripe Minions — scaffold kolem Claude Code, 3M testů, 1300 PR/týden
- SkillsBench — evaluace 84 skills, ukazuje limity prompt-only přístupu
