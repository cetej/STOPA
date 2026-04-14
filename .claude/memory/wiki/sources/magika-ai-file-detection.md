---
title: "Magika: AI-Powered File Type Detection"
slug: magika-ai-file-detection
source_type: url
url: "https://github.com/google/magika"
date_ingested: 2026-04-13
date_published: "2024"
entities_extracted: 1
claims_extracted: 4
---

# Magika: AI-Powered File Type Detection

> **TL;DR**: Google open-source deep learning file type detector. 200+ typů, ~99% accuracy, ~5ms/soubor, pár MB model. Produkčně nasazen v Gmail, Drive, Safe Browsing (miliardy souborů/týden). Multi-platform: Rust CLI, Python, JS/TS, Go.

## Key Claims

1. ~99% precision i recall přes 200+ content types — trénováno na ~100M vzorcích — `[verified]`
2. ~5ms inference per soubor na CPU, nezávislé na velikosti souboru — `[verified]`
3. Výrazně lepší než libmagic/file na textové typy (kód, config, markup) kde magic numbers neexistují — `[argued]`
4. Produkční nasazení v Google (Gmail, Drive, Safe Browsing) — miliardy souborů týdně — `[verified]`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| [Magika](../entities/magika.md) | tool | new |

## Relations

- Magika `created_by` Google
- Magika `competes_with` libmagic/file — AI approach vs magic number heuristics

## Cross-References

- Related learnings: none directly matched
- Related wiki sources: none
- Contradictions: none
