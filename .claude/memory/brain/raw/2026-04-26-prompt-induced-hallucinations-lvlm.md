---
title: Halucinace v multimodálních modelech způsobené textem, ne vizuálními vstupy
url: http://arxiv.org/abs/2604.21911v1
date: 2026-04-26
concepts: ["Halucinace v AI", "Large Vision-Language Models (LVLM)", "Preference optimization", "Vizuální grounding", "Textové priory vs. vizuální vstupy"]
entities: ["Pegah Khayatan", "Jayneel Parekh", "Matthieu Cord", "HalluScope benchmark", "HalluVL-DPO framework"]
source: brain-ingest-local
---

# Halucinace v multimodálních modelech způsobené textem, ne vizuálními vstupy

**URL**: http://arxiv.org/abs/2604.21911v1

## Key Idea

Výzkum ukazuje, že halucinace ve velkých vision-language modelech (LVLM) vznikají primárně kvůli nadměrnému spoléhání na textové instrukce a jazykové znalosti, nikoliv kvůli omezením vizuální komponenty. Navrhují benchmark HalluScope a optimalizační framework HalluVL-DPO pro snížení těchto halucinací.

## Claims

- Halucinace v LVLM modelech vznikají především kvůli nadměrnému spoléhání na textové instrukce a poznatky z jazykového modelu, ne kvůli slabostem vizuální komponenty
- HalluScope benchmark umožňuje systematicky měřit, do jaké míry různé faktory způsobují halucinace
- HalluVL-DPO framework dokáže efektivně redukovat halucinace způsobené textem pomocí preference optimalizace, přičemž zachovává nebo zlepšuje výkon na jiných benchmarcích

## Relevance for STOPA

Pro STOPA orchestraci multimodálních AI systémů je klíčové pochopit, že textové instrukce mohou převážit vizuální vstupy a způsobit halucinace. Orchestrace musí zohledňovat balancování mezi jazykovými a vizuálními modalitami a implementovat strategie pro ověřování grounding odpovědí.
