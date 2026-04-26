---
title: CrossCommitVuln-Bench: Dataset zranitelností neviditelných pro statickou analýzu
url: http://arxiv.org/abs/2604.21917v1
date: 2026-04-26
concepts: ["Multi-commit vulnerabilities", "Per-commit static analysis", "SAST detection gaps", "CVE dataset", "Cross-commit vulnerability detection"]
entities: ["Arunabh Majumdar", "AIware 2026", "Semgrep", "Bandit"]
source: brain-ingest-local
---

# CrossCommitVuln-Bench: Dataset zranitelností neviditelných pro statickou analýzu

**URL**: http://arxiv.org/abs/2604.21917v1

## Key Idea

Výzkumný dataset 15 reálných Python CVE zranitelností, které vznikly postupně napříč více commity - každý jednotlivý commit je neškodný pro per-commit statickou analýzu, ale společně vytváří kritickou zranitelnost.

## Claims

- Per-commit detection rate (CCDR) je pouze 13% - 87% řetězců commitů je neviditelných pro per-commit SAST
- I v kumulativním módu (celá kódová báze) je detekční míra pouze 27%
- Oba případy per-commit detekce jsou kvalitativně slabé - jeden se vyskytuje u commitů označených jako bezpečnostní opravy, druhý detekuje pouze vedlejší komponentu a minuje primární zranitelnost (200+ nechráněných API endpointů)
- Snapshot-based SAST nástroje často přehlédnou zranitelnosti, jejichž vznik se táhne přes více commitů

## Relevance for STOPA

Pro STOPA orchestraci je klíčové pochopení, že bezpečnostní analýza izolovaných změn (commitů) není dostatečná - orchestrace bezpečnostního testování musí zahrnovat analýzu kumulativních efektů změn v čase a napříč komponentami systému.
