---
title: Carbon-Taxed Transformers: komprese LLM s ohledem na emise CO2
url: http://arxiv.org/abs/2604.25903v1
date: 2026-04-29
concepts: ["komprese LLM", "green AI", "carbon taxation", "model efficiency", "software engineering", "pruning", "quantization", "knowledge distillation"]
entities: ["Ajmain Inqiad Alam", "Palash Roy", "Chanchal K. Roy", "Banani Roy", "Kevin A. Schneider", "ACM FSE 2026"]
source: brain-ingest-local
---

# Carbon-Taxed Transformers: komprese LLM s ohledem na emise CO2

**URL**: http://arxiv.org/abs/2604.25903v1

## Key Idea

Výzkumný článek představuje CTT (Carbon-Taxed Transformers) – systematickou pipeline pro kompresi velkých jazykových modelů v software engineeringu, která redukuje paměť až 49×, čas inference 3-10× a emise CO2 až 81% při zachování 89-98% přesnosti.

## Claims

- CTT dosahuje až 49× redukci paměti a 3-10× zrychlení inference při minimální ztrátě přesnosti
- Pipeline snižuje emise CO2 až o 81% při zachování 98% přesnosti u detekce klonů kódu
- Ablační studie potvrzují, že pořadí kroků v pipeline i jednotlivé komponenty jsou zásadní pro efektivitu
- Metoda funguje napříč encoder-only, encoder-decoder i decoder-only architekturami

## Relevance for STOPA

Pro STOPA orchestraci kritické zjištění, že LLM modely lze dramaticky zefektivnit bez ztráty výkonu – umožňuje deployment menších, rychlejších a ekologičtějších modelů pro SE úlohy jako generování/analýza kódu.
