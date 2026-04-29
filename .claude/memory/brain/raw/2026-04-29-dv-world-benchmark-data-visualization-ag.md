---
title: DV-World: Benchmark pro agenty vizualizující data v reálných scénářích
url: http://arxiv.org/abs/2604.25914v1
date: 2026-04-29
concepts: ["data visualization agents", "benchmark", "spreadsheet manipulation", "cross-platform visualization", "intent alignment", "MLLM evaluation", "enterprise workflows"]
entities: ["Jinxiang Meng", "Shaoping Huang", "DV-World", "arXiv"]
source: brain-ingest-local
---

# DV-World: Benchmark pro agenty vizualizující data v reálných scénářích

**URL**: http://arxiv.org/abs/2604.25914v1

## Key Idea

DV-World je nový benchmark s 260 úlohami pro testování AI agentů v reálných scénářích datové vizualizace, zahrnující práci se spreadsheety, adaptaci vizualizací napříč platformami a interakci s uživateli. Současné top modely dosahují méně než 50% úspěšnosti.

## Claims

- Existující benchmarky trpí omezením na code-sandbox prostředí a jednoduchými úlohami založenými na jednom jazyce
- DV-World obsahuje tři domény: DV-Sheet pro práci se spreadshety, DV-Evolution pro adaptaci vizualizací a DV-Interact pro proaktivní alignment záměrů
- State-of-the-art modely dosahují méně než 50% celkového výkonu na DV-World benchmarku
- Hybridní evaluační framework kombinuje Table-value Alignment pro numerickou přesnost a MLLM-as-a-Judge pro sémantické hodnocení

## Relevance for STOPA

STOPA orchestrace by mohla integrovat agenty pro datovou vizualizaci jako specializované nástroje. Benchmark odhaluje, že současné modely selhávají v reálných komplexních scénářích, což je relevantní pro design robustní orchestrace.
