---
title: Multi-agentní systém s pamětí pro automatické generování příznaků
url: https://arxiv.org/abs/2604.20261
date: 2026-04-26
concepts: ["Multi-agentní systém", "Automatické generování příznaků", "Paměťové mechanismy pro LLM", "Feature engineering", "Routování agentů", "Iterativní učení se zpětnou vazbou"]
entities: ["Fengxian Dong", "University of Science and Technology of China", "ACL 2026"]
source: brain-ingest-local
---

# Multi-agentní systém s pamětí pro automatické generování příznaků

**URL**: https://arxiv.org/abs/2604.20261

## Key Idea

MALMAS je systém založený na velkých jazykových modelech a více agentech, který automaticky generuje informativní příznaky z tabulkových dat. Využívá routovací agent k aktivaci specializovaných agentů a tři typy paměti (procedurální, zpětnovazební, konceptuální) k iterativnímu zlepšování kvality a diverzity generovaných příznaků.

## Claims

- Tradiční metody automatického generování příznaků jsou omezeny pevně definovanými knihovnami operátorů a nemohou využít sémantiku úlohy
- MALMAS dekomponuje proces generování na agenty s odlišnými odpovědnostmi a Router Agent aktivuje vhodnou podmnožinu agentů v každé iteraci
- Integrace tří typů paměti (procedurální, zpětnovazební, konceptuální) umožňuje iterativní zlepšování kvality a diverzity generovaných příznaků
- Experimenty na více veřejných datasetech prokázaly efektivitu přístupu oproti nejmodernějším baseline metodám

## Relevance for STOPA

MALMAS demonstruje pokročilou orchestraci specializovaných agentů s routovacím mechanismem a sdílenými paměťovými moduly. Tento přístup k dynamické koordinaci agentů a využití různých typů paměti pro iterativní zlepšování je přímo relevantní pro design STOPA orchestrace komplexních úloh.
