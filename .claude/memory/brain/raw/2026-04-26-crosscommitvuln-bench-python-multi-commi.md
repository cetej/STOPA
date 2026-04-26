---
title: CrossCommitVuln-Bench: Dataset zranitelností v Pythonu neviditelných pro analýzu jednotlivých commitů
url: http://arxiv.org/abs/2604.21917v1
date: 2026-04-26
concepts: ["multi-commit zranitelnosti", "statická analýza kódu (SAST)", "per-commit vs cumulative scanning", "neviditelné bezpečnostní hrozby", "CVE dataset pro Python"]
entities: ["Arunabh Majumdar", "AIware 2026", "Semgrep", "Bandit"]
source: brain-ingest-local
---

# CrossCommitVuln-Bench: Dataset zranitelností v Pythonu neviditelných pro analýzu jednotlivých commitů

**URL**: http://arxiv.org/abs/2604.21917v1

## Key Idea

Benchmark 15 reálných Python zranitelností (CVE), kde každá vznikla postupně přes více commitů - každý jednotlivý commit je neškodný pro statickou analýzu, ale společně tvoří kritickou chybu. Per-commit detekce dosahuje pouze 13% úspěšnosti.

## Claims

- 87% zranitelností v datasetu je neviditelných pro per-commit statickou analýzu (CCDR = 13%)
- Dva detekované případy jsou kvalitativně nedostatečné - jeden u security fixů (kde vývojáři alert ignorují), druhý detekuje jen vedlejší problém místo hlavní zranitelnosti
- I v kumulativním módu (celá kódová báze) je úspěšnost detekce pouze 27%, což potvrzuje, že snapshot-based SAST nástroje často přehlédnou zranitelnosti rozprostřené přes více commitů

## Relevance for STOPA

Pro STOPA orchestraci kritické zjištění, že bezpečnostní analýza musí sledovat historii změn a souvislosti mezi commity, ne jen aktuální stav. Ukazuje potřebu cross-commit analýzy v CI/CD pipeline a při orchestraci bezpečnostních nástrojů.
