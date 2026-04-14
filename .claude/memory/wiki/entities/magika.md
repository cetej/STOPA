---
name: Magika
type: tool
first_seen: 2026-04-13
last_updated: 2026-04-13
sources: [magika-ai-file-detection]
tags: [ai-tools, file-detection, pipeline, google]
---

# Magika

> Google open-source AI file type detector — deep learning model (~99% accuracy, 200+ typů, ~5ms/soubor). Produkčně v Gmail, Drive, Safe Browsing.

## Key Facts

- 200+ content types (binární + textové), ~99% accuracy, trénováno na ~100M vzorcích (ref: sources/magika-ai-file-detection.md)
- ~5ms inference na CPU, model pár MB, near-constant speed nezávisle na velikosti souboru (ref: sources/magika-ai-file-detection.md)
- Multi-platform: `pip install magika`, `brew install magika`, `cargo install magika-cli`, `npm install magika` (ref: sources/magika-ai-file-detection.md)
- Lepší než libmagic na textové typy (kód, config, markup) kde magic numbers neexistují (ref: sources/magika-ai-file-detection.md)
- 11.2K GitHub stars, Apache 2.0, Rust+Python+TS+Go (ref: sources/magika-ai-file-detection.md)
- Per-type confidence thresholds — vrací generic label když si není jistý (ref: sources/magika-ai-file-detection.md)

## Relevance to STOPA

Použitelný v pipeline zpracovávajícím smíšený vstup (inbox s PDF, markdown, kódem, obrázky) pro automatický routing na správný processor. Aktuálně nízká priorita — STOPA zpracovává známé typy explicitně. Relevantní pokud se rozšíří ingest pipeline o automatickou detekci neznámých formátů.

## Mentioned In

- [Magika: AI File Detection](../sources/magika-ai-file-detection.md)
