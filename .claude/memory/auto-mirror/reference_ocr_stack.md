---
name: OCR Stack Decision
description: GLM-OCR evaluated and skipped (no Czech); recommended OCR stack per project — Tesseract, Marker, Claude Vision, PaddleOCR
type: reference
---

## GLM-OCR Radar (2026-04-07): SKIP

- 0.9B model, #1 OmniDocBench (94.62) ale jen 75.2 na olmOCR-bench
- **Bez češtiny** (pouze ZH, EN, FR, ES, RU, DE, JA, KO)
- Alpha (v0.1.4), broken layout detector v transformers 5.4.0, pomalé na T4
- MaaS API = data do Číny (GDPR problém)
- Sledovat — až přidají CZ a stabilizují (v1.0+), přehodnotit

## Doporučený OCR stack pro projekty

| Projekt | Potřeba | Řešení | Kdy |
|---------|---------|--------|-----|
| DANE | Reverse-parsing českých daňových PDF | Claude Vision API (už máme klíč) | Až bude potřeba |
| NG-ROBOT | Skenované články, taxonomické tabulky | Marker (Surya, `pip install marker-pdf`) | Až přibydou skeny do pipeline |
| MONITOR | PDF zprávy, úřední dokumenty | Claude Vision API jako fallback | Až bude PDF ingestion |
| GRAFIK | Text detection pro T2L fáze 3 | PaddleOCR (lightweight, CPU) | Fáze 3 implementace |
| KARTOGRAF | Textové popisky z map | Tesseract (`ces`) + OpenCV | Pokud bude potřeba |

## OCR alternativy — quick reference

| Nástroj | Čeština | Self-host | Cena | Nejlepší pro |
|---------|---------|-----------|------|-------------|
| Tesseract | Ano (`ces`) | Ano | Free | Jednoduché dokumenty |
| Claude Vision | Ano | Ne (API) | Anthropic kredit | Layout-aware, tabulky |
| Marker (Surya) | Ano (90+ lang) | Ano | Free | Komplexní PDF, formule, tabulky |
| PaddleOCR | Omezená | Ano | Free | Lightweight text detection |
| Azure Document AI | Ano | Ne (cloud) | $1.5/1K stránek | Enterprise, SLA |
