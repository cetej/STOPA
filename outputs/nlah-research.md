# Natural-Language Agent Harnesses — Research Brief

**Date:** 2026-04-05
**Question:** Co říká paper arXiv:2603.25723 o natural-language agent harnesses?
**Scope:** narrow (single paper)
**Sources consulted:** 2 (arxiv abstract + full PDF via Jina Reader)

---

## Executive Summary

Paper zavádí **Natural-Language Agent Harnesses (NLAHs)** — přístup, kde je logika orchestrace agentů
vyjádřena jako explicitní, přenositelný artefakt v přirozeném jazyce místo toho, aby byla rozptýlena
v controller kódu [VERIFIED][1]. Autoři z Tsinghua a Harbin IT tím formalizují designový vzor, který
STOPA implementuje empiricky přes SKILL.md soubory.

Klíčový výsledek: **migrace kódu na text může výkon *zvýšit*** [VERIFIED][1] — na OSWorld 30.4% (nativní
kód) → 47.2% (NLAH). To odpovídá ne zlepšení modelu, ale "behaviorálnímu přemístění": NLAH upřednostňuje
file-backed state a artefaktovou verifikaci před screen-grounded repair. Modul self-evolution přidává
+4.8% na SWE-bench Verified [VERIFIED][1] — nejsilnější jednotlivý modul.

Hlavní varování: extra struktura automaticky nezlepšuje výkon. Verifier modul způsobil -0.8% na SWE-bench,
dynamic orchestration byl neutrální — přidaná komplexita tvoří "solved-set replacer", ne uniformní
zlepšení [VERIFIED][1].

---

## Detailed Findings

### 1. Klíčová teze: harness jako první třídy artefakt

Harness logika (role, kontrakty, workflow, failure handling) bývá "scattered across controller code,
hidden framework defaults, tool adapters, verifier scripts" [VERIFIED][1]. NLAH ji externalizuje jako
editovatelný objekt. To umožňuje:

- Fair comparison a ablaci jednotlivých designových rozhodnutí [VERIFIED][1]
- Přenos harness mezi projekty a modely [VERIFIED][1]
- Systematický výzkum ("harness representation science") [SINGLE-SOURCE][1]

### 2. NLAH Komponenty (6)

| Komponenta | Popis |
|------------|-------|
| **Contracts** | Required inputs/outputs, format constraints, retry rules |
| **Roles** | Non-overlapping role prompts (solver, verifier, researcher, orchestrator) |
| **Stage structure** | Explicit topology: plan → execute → verify → repair |
| **Adapters/scripts** | Deterministické hooky (tests, verifiers, retrieval) |
| **State semantics** | Perzistentní elementy přes kroky a delegaci |
| **Failure taxonomy** | Pojmenované failure mody pro recovery |

### 3. Intelligent Harness Runtime (IHR)

Tři komponenty [VERIFIED][1]:
1. **In-loop LLM** — interpretuje harness logiku přímo (ne jen prompt decoration)
2. **Backend** — terminálové nástroje a multi-agent interface
3. **Runtime charter** — sdílená sémantika kontraktů a state managementu

Kritické pozorování: "90% prompt tokenů, completion tokenů, tool calls a LLM volání se děje v
delegovaných child agentech, ne v parent threadu" [VERIFIED][1]. IHR je koordinátor, ne vykonavatel.

### 4. File-Backed State Module

Externalizes durable state přes 3 vlastnosti [VERIFIED][1]:
- **Externalized** — artefakty vs. transient kontext
- **Path-addressable** — znovuotevření objektů přes cestu
- **Compaction-stable** — přežívá truncation a restart

Na SWE-bench: +1.6%. Na OSWorld: **+5.5%** (nejsilnější modul pro computer-use) [VERIFIED][1].

### 5. Kanonická workspace struktura

```
TASK.md          — run-local task statement
SKILL.md         — harness control logic
task_history.jsonl — append-only invocation record
artifacts/       — benchmark-facing deliverables
children/        — child agent workspaces
```

Tato struktura je identická s STOPA konvencemi [INFERRED][1,2].

### 6. Module Ablation Results (SWE-bench Verified, baseline 75.2%)

| Modul | Delta |
|-------|-------|
| Self-evolution | **+4.8%** |
| File-backed state | +1.6% |
| Evidence-backed answering | +1.6% |
| Dynamic orchestration | 0.0% |
| Verifier | **-0.8%** |
| Multi-candidate search | -2.4% |

### 7. Module Ablation Results (OSWorld, baseline 41.7%)

| Modul | Delta |
|-------|-------|
| File-backed state | **+5.5%** |
| Multi-candidate search | +2.7% |
| Dynamic orchestration | +2.7% |

### 8. Migrace kód → text (RQ3)

OS-Symphony harness [VERIFIED][1]:
- Nativní kód: 30.4%
- Migrovaný NLAH: **47.2%**

Přičina není "lepší model" ale topologický shift: native kód používá screenshot-grounded repair,
NLAH přechází na file-backed state a artefaktovou verifikaci. Výsledek: "observability plus recovery
scaffolding" místo prostého násobení akcí [VERIFIED][1].

### 9. Hlavní varování

- Extra struktura neimplicitně nezlepšuje výkon — Verifier diverguje od benchmark acceptance criteria [VERIFIED][1]
- Runtime contamination risk: silný sdílený runtime může absorbovat harness-specifické chování [SINGLE-SOURCE][1]
- NL má nižší preciznost než kód pro deterministické operace [VERIFIED][1]
- Evaluace na subsetech benchmark (125 SWE-bench, 36 OSWorld), ne plných suitách [VERIFIED][1]

---

## Relevance pro STOPA

Přímá korespondence mezi NLAH koncepty a STOPA implementací:

| Paper Koncept | STOPA Ekvivalent |
|---------------|-----------------|
| NLAH (Natural-Language Agent Harness) | `.claude/skills/<name>/SKILL.md` |
| IHR Runtime Charter | `.claude/settings.json` hooks + hook skripty |
| File-backed state module | `.claude/memory/` systém |
| Stage structure | PLAN → WORK → ASSESS → COMPOUND loop |
| Failure taxonomy | 3-fix escalation + circuit breakers v CLAUDE.md |
| Roles (solver/verifier/orchestrator) | Sub-agenti s explicit model choice |
| task_history.jsonl | `.claude/memory/state.md` + checkpoint.md |
| children/ workspaces | Sub-agent worktrees |
| Contracts | `allowed-tools`, `permission-tier`, `constrained-tools` v SKILL.md frontmatter |

STOPA SKILL.md soubory jsou v podstatě NLAHs — paper poskytuje akademické zdůvodnění přístupu,
který STOPA empiricky vyvinula [INFERRED][1,2].

---

## Disagreements & Open Questions

- Paper evaluuje na GPT-5.4 (model neexistující v dnešní době → pravděpodobně vnitřní název nebo
  experimentální model). Přenositelnost výsledků na Claude je nepotvrzena [UNVERIFIED].
- Verifier modul škodí na SWE-bench ale paper neukázal výsledky na OSWorld pro verifier —
  doménová závislost výkonu není plně vysvětlena [SINGLE-SOURCE][1].
- "Self-evolution" modul (+4.8%) není detailně popsán v dostupném extraktu — mechanismus
  zůstává nejasný [UNVERIFIED].

---

## Evidence Table

| # | Source | URL | Key Claim | Type | Confidence |
|---|--------|-----|-----------|------|------------|
| 1 | Pan et al., "Natural-Language Agent Harnesses" (2026) | https://arxiv.org/pdf/2603.25723 | NLAH+IHR stack, experimental results | primary | high |
| 2 | arXiv abstract | https://arxiv.org/abs/2603.25723 | Title, authors, abstract | primary | high |

---

## Sources

1. Pan et al. — "Natural-Language Agent Harnesses" — https://arxiv.org/pdf/2603.25723
2. arXiv abstract — https://arxiv.org/abs/2603.25723

---

## Coverage Status

- **[VERIFIED]:** Všechny klíčové technické claims — přímo z PDF via Jina Reader
- **[INFERRED]:** STOPA-NLAH korespondence (z obou zdrojů, ne explicitně v paperu)
- **[SINGLE-SOURCE]:** "Harness representation science" termín; verifier OSWorld výsledky
- **[UNVERIFIED]:** GPT-5.4 model identita; self-evolution mechanismus detail
