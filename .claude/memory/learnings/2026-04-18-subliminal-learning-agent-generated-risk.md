---
name: Subliminal Learning — agent_generated content carries hidden behavioral traits
date: 2026-04-18
type: anti_pattern
severity: high
component: memory
tags: [safety, agent-generated, model-gate, tool-synth, distillation, subliminal]
summary: "Paper prokázal, že LLM přenášejí behavioral traits (včetně misalignmentu) přes sémanticky nesouvisející data — number sequences, code — i po filtrování. Transfer funguje jen mezi stejnou base model family. Implikace pro STOPA — (1) source agent_generated learnings (0.8× weight) mohou nést subliminální traits z generujícího modelu, samotné sémantické filtrování je nedostatečné. (2) model_gate field by měl být povinný pro agent_generated learnings, ne jen pro model-specific workaroundy. (3) tool-synth generované skills dědí traits base modelu — cross-model použití může přenášet nežádoucí chování."
source: external_research
uses: 0
successful_uses: 0
harmful_uses: 0
confidence: 0.75
maturity: draft
verify_check: manual
related: [2026-04-18-in-place-ttt-fast-weights-analog.md]
---

## Paper
- **Title**: Subliminal Learning: Language models transmit behavioral traits via hidden signals in data (arXiv:2507.14805)
- **Authors**: Cloud, Le, Chua, Betley, Sztyber-Betley, Hilton, Marks, Evans (Anthropic + Truthful AI)
- **Date**: 2025-07-20
- **Core finding**: Student model trained on teacher's outputs absorbs teacher's traits (preferences, misalignment) even když data neobsahují sémantický reference na trait. Efekt mizí při rozdílné base architecture.

## Tři STOPA implikace

### 1. `source: agent_generated` weighting nestačí

Aktuální stav (`.claude/rules/memory-files.md`):
- `agent_generated` má retrieval weight 0.8×, initial confidence 0.5
- Zdůvodnění: "menší důvěra v auto-generované learnings"

Problém: paper ukazuje, že trait transfer je *nezávislý na sémantickém obsahu*. Samotné snížení váhy neblokuje subliminální přenos — learning zůstává v retrieval poolu a ovlivňuje downstream rozhodování.

**Actionable**: Při zápisu `source: agent_generated` learning:
- Pokud generující model = aktuální model: OK, trait consistency udržena
- Pokud generující model ≠ aktuální model (např. Haiku subagent generoval, čte Opus): flag pro `learning-admission.py` review

### 2. `model_gate:` by měl expandovat scope

Aktuální definice: model-specific workaroundy (např. sonnet-4.6 bug).

Rozšíření po tomto paper:
- Každý `source: agent_generated` learning → auto-populate `model_gate:` s generujícím modelem
- `verify-sweep.py` už flaguje mismatch — stačí rozšířit na agent_generated subset
- Cross-model graduation (agent_generated → critical-patterns) MUSÍ projít manual review

### 3. tool-synth generated skills nesou base-model traits

Synthesized skill v `.claude/skills/_generated/<slug>/` je produkt generujícího modelu. Paper implikuje:
- Skill syntetizovaný Haiku, spouštěný Opusem → trait mismatch možný
- Frontmatter field `generated_by:` (model name) by řešil attribution
- Graduation gate: synthesized skill NESMÍ projít sweep-ingest pokud `generated_by` ≠ active model family

## Co NENÍ v scope

- Nemůžeme detekovat subliminální traits retrospektivně — paper sám nabízí jen blokaci transferu (different base model)
- Naše vlastní learnings nejsou subliminal channel — jsou explicit text, čtený modelem. Riziko je v použití *agent výstupu jako tréninkového signálu*, což STOPA nedělá na model úrovni (jen na retrieval úrovni).

## Proposed guardrails (budoucí práce)

1. Audit všech stávajících `source: agent_generated` learnings — check missing `model_gate:`
2. Rozšířit `learning-admission.py`: warn při `agent_generated` bez `model_gate`
3. Rozšířit `tool-synth` SKILL.md: require `generated_by:` ve skill frontmatter
4. Rozšířit `commit-invariants.md`: I10 — `agent_generated` learning MUSÍ mít `model_gate:`

## Důvěra

`confidence: 0.75` — paper je silný (Anthropic authors, theoretical proof + empirical), ale implikace na STOPA je extrapolace. Upgrade na `validated` až po prvním reálném auditu existujících agent_generated learnings.
