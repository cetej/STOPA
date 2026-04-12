---
name: Optimizer reference for fine-tuning
description: Modern optimizer recommendations for LoRA/fine-tuning and model training — Prodigy, Schedule-Free, SAM, AdamW
type: reference
---

Referenční přehled optimizérů pro budoucí fine-tuning úkoly (z deep research arXiv:1609.04747, 2026-04-04).

## Doporučení podle use-case

| Use-case | Optimizer | Proč | Paper |
|----------|-----------|------|-------|
| LoRA / DreamBooth fine-tuning | **Prodigy** | LR-free, standard v HF Diffusers | arXiv:2306.06101 |
| Obecný trénink (safe default) | **AdamW** | Decoupled weight decay, de facto standard pro transformery | arXiv:1711.05101 |
| Když nechceš ladit LR schedule | **Schedule-Free AdamW** | Žádný schedule, vyhrál MLCommons AlgoPerf 2024 | arXiv:2405.15682 |
| Malý dataset, lepší generalizace | **SAM** | Sharpness-aware, flat minima = lepší generalizace | arXiv:2010.01412 |
| Velký batch (distribuovaný trénink) | **LAMB** | Layer-wise scaling, BERT za 76 min | arXiv:1904.00962 |
| Paměťově omezené (GPU) | **Lion** | Sign-only update, 2x méně paměti než Adam | arXiv:2302.06675 |
| SOTA pre-training (2024) | **SOAP** | Adam v Shampoo eigenbázi, 40% méně iterací | arXiv:2409.11321 |

## Relevance pro naše projekty

- **ORAKULUM** (Chronos-2, STUMPY): AdamW default, SAM pro malé datasety predikčních trhů
- **LoRA fine-tuning** (pokud): Prodigy jako první volba
- **Ostatní projekty** (STOPA, MONITOR, GRAFIK...): netrénují, volají API — irrelevantní

## Plný research brief

`STOPA/outputs/gradient-descent-research.md` — 28 zdrojů, 20 post-2017 optimizérů
