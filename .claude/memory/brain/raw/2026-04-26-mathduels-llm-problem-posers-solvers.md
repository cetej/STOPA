---
title: MathDuels: Hodnocení LLM jako tvůrců i řešitelů matematických problémů
url: http://arxiv.org/abs/2604.21916v1
date: 2026-04-26
concepts: ["self-play benchmark", "adversarial problem generation", "Rasch model pro společné hodnocení", "decoupling authoring a solving schopností", "co-evolving difficulty"]
entities: ["Zhiqiu Xu", "Shibo Jin", "Shreya Arya", "Mayur Naik", "Rasch (1993)"]
source: brain-ingest-local
---

# MathDuels: Hodnocení LLM jako tvůrců i řešitelů matematických problémů

**URL**: http://arxiv.org/abs/2604.21916v1

## Key Idea

MathDuels je benchmark, kde jazykové modely současně vytvářejí matematické úlohy (jako autoři) i řeší úlohy vytvořené jinými modely, což umožňuje odlišit schopnosti modelů, které dosahují stropu na statických benchmarcích. Obtížnost benchmarku se vyvíjí s příchodem nových modelů místo saturace na fixní úrovni.

## Claims

- Stávající statické matematické benchmarky dosahují stropu a nedokážou rozlišit schopnosti frontierových modelů
- Schopnosti autorství a řešení matematických problémů jsou částečně oddělené (decoupled)
- Dual-role evaluace odhaluje rozdíly ve schopnostech neviditelné v single-role benchmarcích
- Novější modely vytvářejí problémy, které poráží dříve dominantní řešitele, čímž benchmark koevolvuje s účastníky
- Tříetapový generační pipeline (meta-prompting, problem generation, difficulty amplification) s nezávislou validací zajišťuje kvalitu problémů

## Relevance for STOPA

Demonstruje pokročilý přístup k evaluaci AI systémů skrze adversariální koevoluci a vícenásobné role, což je relevantní pro orchestraci komplexních multi-agent systémů v STOPA, kde agenti mohou hrát různé komplementární role a dynamicky se adaptovat.
