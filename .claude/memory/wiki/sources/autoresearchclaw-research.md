---
title: "AutoResearchClaw — Architecture Research Brief"
slug: autoresearchclaw-research
source_type: research_output
date_ingested: 2026-04-07
entities_extracted: 7
claims_extracted: 5
---
# AutoResearchClaw — Architecture Research Brief

> **TL;DR**: AutoResearchClaw je plně autonomní research pipeline v 23 fázích a 8 fázích, která bere NL-idea a produkuje conference-ready paper. Klíčové inovace: VerifiedRegistry (numerický whitelist zabraňující fabricaci dat), MetaClaw (cross-run JSONL learning s SKILL.md injection), multi-agent debate pro hypothesis generation a self-healing execution loop (max 10 iterací). 9194 stars, vytvořeno 2026-03-15.

## Key Claims

1. VerifiedRegistry je architektonický (ne post-hoc) přístup k anti-fabricaci: číselný whitelist se buduje z experimentálních dat PŘED psaním paperu; paper verifier odmítá neregistrovaná čísla v Results/Experiments/Tables — `[verified]`
2. MetaClaw cross-run learning: EvolutionStore ukládá lekce ve formátu JSONL, build_overlay() je injektuje jako prompt overlay do všech subsequent pipeline stages — `[verified]`
3. Stage 15 PROCEED/REFINE/PIVOT decision logic: REFINE rollbackuje na stage 13, PIVOT na stage 8; _promote_best_stage14() zajistí, že paper writing vždy používá nejlepší (ne nejnovější) experimentální data — `[verified]`
4. Multi-agent debate je scopován výlučně na hypothesis generation (Stage 7), ne na celý pipeline; top-level orchestrátor je single agent — `[verified]`
5. README claim "18.3% composite robustness improvement" není přítomný v evolution.py zdrojovém kódu — jde o marketing copy — `[verified]`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| AutoResearchClaw | tool | new |
| VerifiedRegistry | concept | new |
| MetaClaw | concept | new |
| EvolutionStore | concept | new |
| PROCEED/REFINE/PIVOT | concept | new |
| aiming-lab | company | new |
| experiment_diagnosis | concept | new |

## Relations

- AutoResearchClaw `implements` VerifiedRegistry `for anti-fabrication`
- MetaClaw `uses` EvolutionStore `for cross-run JSONL learning`
- MetaClaw `injects` SKILL.md `as prompt overlay`
- AutoResearchClaw `uses` PROCEED/REFINE/PIVOT `at Stage 15`
- VerifiedRegistry `gates` paper_verifier `section-level enforcement`
